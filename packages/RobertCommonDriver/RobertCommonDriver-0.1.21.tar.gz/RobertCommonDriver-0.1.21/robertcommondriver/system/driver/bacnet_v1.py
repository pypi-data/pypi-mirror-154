import time
import psutil
import logging
import re
from threading import Lock
from typing import Callable, Optional, List
from collections import deque
from datetime import datetime
from ipaddress import ip_network, ip_address
from .base import BaseCommon
from queue import Queue

# bacnet
from bacpypes.apdu import AbortReason, RejectReason, ReadAccessSpecification, ConfirmedRequestSequence, ConfirmedCOVNotificationRequest, PropertyReference, ReadPropertyMultipleRequest, ReadPropertyMultipleACK, ReadPropertyRequest, ReadPropertyACK, WritePropertyRequest, SimpleAckPDU, WhoIsRequest, IAmRequest, AbortPDU, RejectPDU, SubscribeCOVRequest
from bacpypes.app import BIPSimpleApplication
from bacpypes.basetypes import ServicesSupported, StatusFlags
from bacpypes.constructeddata import Array, Any, Choice
from bacpypes.core import run, stop, deferred, enable_sleeping
from bacpypes.iocb import IOCB
from bacpypes.local.device import LocalDeviceObject
from bacpypes.npdu import WhoIsRouterToNetwork, WhatIsNetworkNumber
from bacpypes.object import get_datatype, AnalogInputObject, AnalogOutputObject, AnalogValueObject, MultiStateInputObject, MultiStateOutputObject, MultiStateValueObject, OctetStringValueObject, BinaryInputObject, BinaryOutputObject, BinaryValueObject, BitStringValueObject, CharacterStringValueObject
from bacpypes.pdu import GlobalBroadcast, Address, LocalBroadcast
from bacpypes.primitivedata import Null, Atomic, Integer, Unsigned, Real, Enumerated, CharacterString
from bacpypes.task import RecurringTask


class SubscriptionContext(object):

    def __init__(self, target_address: str, object_type: str, instance_number: int, sub_process_id: int, lifetime: Optional[int] = None, confirmed: bool = True):
        self.target_address = target_address
        self.sub_process_id = sub_process_id
        self.object_type = object_type
        self.instance_number = instance_number
        self.lifetime = lifetime
        self.confirmed = confirmed


class IOCBContext:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def update(self, **kwargs):
        self.kwargs.update(kwargs)


class SimulateObject:

    def __init__(self, object_type: str, instance_number: int, present_value, **kwargs):
        self.kwargs = {'object_type': object_type, 'instance_number': instance_number, 'present_value': present_value}
        self.kwargs.update(kwargs)

    def update(self, **kwargs):
        self.kwargs.update(kwargs)

    def get(self, key: str, default = None):
        return self.kwargs.get(key, default)

    def set(self, key: str, value):
        self.kwargs[key] = value

    def has_key(self, key: str) -> bool:
        return True if key in self.kwargs.keys() else False


class BacnetApplication(BIPSimpleApplication, RecurringTask):

    def __init__(self, local_device, local_address: str, **kwargs):
        self.kwargs = kwargs
        BIPSimpleApplication.__init__(self, local_device, local_address)
        RecurringTask.__init__(self, self.kwargs.get('request_check_interval', 100))

        self.exit_flag: bool = False    # 退出事件
        self.next_invoke_id: int = 0    # invoke id
        self.request_queue = Queue()
        self.iocbs: dict = {}     # 现有iocb
        self.callbacks: dict = self.kwargs.get('callbacks', {})   # 回调函数
        self.sub_cov_contexts = {}  # COV 订阅
        self.cov_sub_process_id = 1 # COV 请求ID
        self.address_network_dict = {}  # 网络地址
        self.read_write_lock = Lock()

        # self.install_task()

    def __del__(self):
        self.exit()

    def __str__(self):
        return f"{self.bacnet_local_address}"

    def exit(self):
        self.exit_flag = True

    def indication(self, apdu):
        if isinstance(apdu, IAmRequest):
            device_type, device_instance = apdu.iAmDeviceIdentifier
            if device_type != 'device':
                return

            i_am = self.callbacks.get('i_am')
            if i_am is not None:
                i_am(str(apdu.pduSource), device_instance, apdu.maxAPDULengthAccepted, str(apdu.segmentationSupported), apdu.vendorID)

        elif isinstance(apdu, ConfirmedCOVNotificationRequest):
            # Handling for ConfirmedCOVNotificationRequests. These requests are sent by the device when a point with a COV subscription updates past the covIncrement threshold(See COV_Detection class in
            # Bacpypes: https://bacpypes.readthedocs.io/en/latest/modules/service/cov.html)
            
            result_dict = {}
            for element in apdu.listOfValues:
                property_id = element.propertyIdentifier
                if not property_id == "statusFlags":
                    values = []
                    for tag in element.value.tagList:
                        values.append(tag.app_to_object().value)
                    if len(values) == 1:
                        result_dict[property_id] = values[0]
                    else:
                        result_dict[property_id] = values

        # forward it along
        BIPSimpleApplication.indication(self, apdu)

    def process_task(self):
        while self.exit_flag is False:
            if not self.request_queue.empty():
                self.handle_request(self.request_queue.get())

    def get_next_invoke_id(self, addr) -> int:
        """Called to get an unused invoke ID."""

        initial_id = self.next_invoke_id
        while 1:
            invoke_id = self.next_invoke_id
            self.next_invoke_id = (self.next_invoke_id + 1) % 256

            # see if we've checked for them all
            if initial_id == self.next_invoke_id:
                raise RuntimeError("no available invoke ID")

            # see if this one is used
            if (addr, invoke_id) not in self.iocbs:
                break

        return invoke_id

    def handle_request(self, iocb):
        apdu = iocb.ioRequest

        if isinstance(apdu, ConfirmedRequestSequence):

            # assign an invoke identifier
            apdu.apduInvokeID = self.get_next_invoke_id(apdu.pduDestination)

            # build a key to reference the IOCB when the response comes back
            invoke_key = (apdu.pduDestination, apdu.apduInvokeID)

            # keep track of the request
            self.iocbs[invoke_key] = iocb

        try:
            self.request(apdu)
        except Exception as e:
            iocb.set_exception(e)

    def send_request(self, request, wait: bool = True, context: Optional[IOCBContext] = None):
        with self.read_write_lock:
            iocb = IOCB(request)
            iocb.set_timeout(self.kwargs.get('time_out', 3000))
            request.apduInvokeID = self.get_next_invoke_id(request.pduDestination)
            if context is None:
                context = IOCBContext(invoke_id=request.apduInvokeID)
            else:
                context.update(invoke_id=request.apduInvokeID)
            iocb.context = context
            deferred(self.request_io, iocb)
            if wait is True:
                iocb.wait()
            return iocb

    # Add network routing for access across network segments(6:2)
    def add_router(self, target_address: str, network: int):
        networks = self.address_network_dict.get(target_address, [])
        if network not in networks:
            networks.append(network)
        self.nsap.update_router_references(None, Address(target_address), networks)

    def do_ConfirmedCOVNotificationRequest(self, apdu):
        cov = self.callbacks.get('cov')
        if cov is not None:
            cov(str(apdu.pduSource), apdu.monitoredObjectIdentifier[0], apdu.monitoredObjectIdentifier[1], apdu.timeRemaining, [(str(element.propertyIdentifier), str(element.value.tagList[0].app_to_object().value)) for element in apdu.listOfValues], True)

        # success
        response = SimpleAckPDU(context=apdu)

        # return the result
        self.response(response)

    def do_UnconfirmedCOVNotificationRequest(self, apdu):
        cov = self.callbacks.get('cov')
        if cov is not None:
            cov(str(apdu.pduSource), apdu.monitoredObjectIdentifier[0], apdu.monitoredObjectIdentifier[1], apdu.timeRemaining, [(str(element.propertyIdentifier), str(element.value.tagList[0].app_to_object().value)) for element in apdu.listOfValues], False)


class BacnetClient:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.bacnet_server_ip = kwargs.get('address')
        self.bacnet_application = None
        self.bacnet_devices = {}
        self.cov_update_buffer = kwargs.get('cov_update_buffer', 3)
        self.bacnet_cov_subs = {}   # 订阅请求
        self.bacnet_cov_sub_process_id = 1
        self.bacnet_max_per_request = kwargs.get('multi_read', 25)
        self.bacnet_objects = {}

        self._get_application()

    def __str__(self):
        return f"BacnetClient({self.bacnet_server_ip})"

    def __del__(self):
        self.exit()

    def exit(self):
        self._release_application(self.bacnet_application)

    def device(self, **kwargs):
        bacnet_device = LocalDeviceObject(
            objectName=kwargs.get('name', 'Robert BACnet driver'),
            objectIdentifier=('device', kwargs.get('identifier', 599)),
            numberOfApduRetries=kwargs.get('retry', 0),
            apduTimeout=kwargs.get('time_out', 3000),
            maxApduLengthAccepted=kwargs.get('max_apdu', 1024),
            segmentationSupported=kwargs.get('segmentation', 'segmentedBoth'),
            vendorIdentifier=kwargs.get('vendor_identifier', 15),
        )

        # build a bit string that knows about the bit names.
        pss = ServicesSupported()
        pss['whoIs'] = 1
        pss['iAm'] = 1
        pss['readProperty'] = 1
        pss['readPropertyMultiple'] = 1

        # set the property value to be just the bits
        try:
            bacnet_device.protocolServicesSupported = pss.value
        except:
            pass
        return bacnet_device

    def _get_application(self, bacnet_app_class=BacnetApplication, bacnet_device = None):
        if self.bacnet_application is None:
            if bacnet_device is None:
                bacnet_device = self.device(**self.kwargs)

            bacnet_application = bacnet_app_class(bacnet_device, self.bacnet_server_ip, callbacks={'i_am': self._call_back_i_am, 'cov': self._call_back_cov})
            if bacnet_application is not None:
                BaseCommon.function_thread(self.control, False).start()
                time.sleep(1)
                self.bacnet_application = bacnet_application
        return self.bacnet_application

    def _release_application(self, bacnet_application):
        try:
            if bacnet_application:
                self.control(False)
                time.sleep(1)
                if hasattr(bacnet_application, 'mux'):
                    bacnet_application.close_socket()
        except Exception as e:
            logging.error(f'bacnet({self}) release {self.bacnet_server_ip} fail {e.__str__()}')
        finally:
            if bacnet_application:
                del bacnet_application
            bacnet_application = None

    def control(self, status: bool = True):
        self.logging(f"control({status})")
        if status is True:
            enable_sleeping()
            run(sigterm=None, sigusr1=None)
        else:
            stop()

    def _send_request(self, request, wait_result: bool = True, context: Optional[IOCBContext] = None):
        return self._get_application().send_request(request, wait_result, context) if self._get_application() else None

    def _find_reason(self, apdu) -> str:
        try:
            if apdu == TimeoutError:
                return "Timeout"
            elif apdu.pduType == RejectPDU.pduType:
                reasons = RejectReason.enumerations
            elif apdu.pduType == AbortPDU.pduType:
                reasons = AbortReason.enumerations
            else:
                if apdu.errorCode and apdu.errorClass:
                    return f"{apdu.errorCode}"
                else:
                    raise ValueError(f"Cannot find reason({apdu.errorCode})...")
            code = apdu.apduAbortRejectReason
            try:
                return [k for k, v in reasons.items() if v == code][0]
            except IndexError:
                return code
        except Exception as err:
            return f"Unknown error: {err.__str__()}"

    def _gen_key(self, target_address: str, object_type: str, instance_number: int, property_name: Optional[str] = None, property_index: Optional[int] = None) -> str:
        values = f"{target_address}_{object_type}_{instance_number}"
        if property_name is not None:
            values = f"{values}_{property_name}"
        if property_index is not None:
            values = f"{values}_{property_index}"
        return values

    def _get_value_from_read_property_request(self, apdu):
        datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
        if not datatype:
            raise Exception("unknown datatype")
        # special case for array parts, others are managed by cast_out
        if issubclass(datatype, Array) and apdu.propertyArrayIndex is not None:
            if apdu.propertyArrayIndex == 0:
                value = apdu.propertyValue.cast_out(Unsigned)
            else:
                value = apdu.propertyValue.cast_out(datatype.subtype)
        else:
            value = apdu.propertyValue.cast_out(datatype)
            if issubclass(datatype, Enumerated):
                value = datatype(value).get_long()
        return value

    def _get_value_from_property_value(self, property_value, datatype):
        value = property_value.cast_out(datatype)
        if issubclass(datatype, Enumerated):
            value = datatype(value).get_long()
        try:
            if issubclass(datatype, Array) and issubclass(datatype.subtype, Choice):
                new_value = []
                for item in value.value[1:]:
                    result = list(item.dict_contents().values())
                    if result[0] != ():
                        new_value.append(result[0])
                    else:
                        new_value.append(None)
                value = new_value
        except Exception as e:
            raise e
        return value

    def _parse_response(self, request, iocb):
        if iocb.ioError:
            raise Exception(f"{request.apduInvokeID}({self._find_reason(iocb.ioError)})")
        else:
            if isinstance(request, ReadPropertyRequest) and isinstance(iocb.ioResponse, ReadPropertyACK):
                # key = self.gen_key(str(request.pduDestination), request.objectIdentifier[0], request.objectIdentifier[1], request.propertyIdentifier, request.propertyArrayIndex)
                return self._get_value_from_read_property_request(iocb.ioResponse)
            elif isinstance(request, WritePropertyRequest) and isinstance(iocb.ioResponse, SimpleAckPDU):
                return iocb.ioResponse
            elif isinstance(request, SubscribeCOVRequest) and isinstance(iocb.ioResponse, SimpleAckPDU):
                return iocb.ioResponse
            elif isinstance(request, SubscribeCOVRequest) and not isinstance(iocb.ioResponse, SimpleAckPDU):
                return None
            elif isinstance(request, ReadPropertyMultipleRequest) and isinstance(iocb.ioResponse, ReadPropertyMultipleACK):
                result_dict = {}
                for result in iocb.ioResponse.listOfReadAccessResults:
                    object_identifier = result.objectIdentifier
                    for element in result.listOfResults:
                        property_identifier = element.propertyIdentifier
                        property_array_index = element.propertyArrayIndex
                        read_result = element.readResult
                        value = ['Good', '']
                        if read_result.propertyAccessError is not None:
                            value = ['Bad', f"{request.apduInvokeID}({read_result.propertyAccessError.errorCode})"]
                        else:
                            property_value = read_result.propertyValue
                            datatype = get_datatype(object_identifier[0], property_identifier)
                            if datatype:
                                if issubclass(datatype, Array) and property_array_index is not None:
                                    if property_array_index == 0:
                                        value[1] = property_value.cast_out(Unsigned)
                                    else:
                                        value[1] = property_value.cast_out(datatype.subtype)
                                else:
                                    value[1] = self._get_value_from_property_value(property_value, datatype)
                        result_dict[self._gen_key(str(request.pduDestination), object_identifier[0], object_identifier[1], property_identifier, property_array_index)] = value
                        if value[0] == 'Good':
                            self._update_device(str(request.pduDestination), **{'object_type': object_identifier[0], 'instance_number': object_identifier[1], property_identifier: value[1]})
                return result_dict
            else:
                raise Exception('Unsupported Request Type')

    #callback#################
    def _call_back_i_am(self, target_address: str, device_id: int, max_apdu_len: int, seg_supported: str, vendor_id: int):
        self.logging(f"i-am({target_address}-{device_id}-{max_apdu_len}-{seg_supported}-{vendor_id})")
        if target_address not in self.bacnet_devices.keys():
            self.bacnet_devices[target_address] = {'objects': {}}
        self.bacnet_devices[target_address].update({'device_id': device_id, 'max_apdu_len': max_apdu_len, 'seg_supported': seg_supported, 'vendor_id': vendor_id, 'update': BaseCommon.get_datetime_str()})

    def _call_back_cov(self, target_address: str, object_type: str, instance_number: int, time_remaining: str, elements: list, confirm: bool = True):
        kwargs = {'object_type': object_type, 'instance_number': instance_number, 'time_remaining': time_remaining}
        for property, value in elements:
            kwargs[property] = value
            self.logging(f"cov_({target_address}-{object_type}-{instance_number}-{time_remaining}-{property}-{value})")
        self._update_device(target_address, **kwargs)

    def discover(self, low_device_id: Optional[int] = None, high_device_id: Optional[int] = None, target_address: Optional[str] = None):
        request = WhoIsRequest()
        if low_device_id is not None:
            request.deviceInstanceRangeLowLimit = low_device_id
        if high_device_id is not None:
            request.deviceInstanceRangeHighLimit = high_device_id
        if target_address is not None:
            request.pduDestination = Address(target_address)
        else:
            request.pduDestination = GlobalBroadcast()
        self.logging(f"discover({request.pduDestination} {low_device_id}-{high_device_id})")
        iocb = self._send_request(request, False)

    def whois_router_to_network(self, network: Optional[int] = None, target_address: Optional[str] = None):
        request = WhoIsRouterToNetwork()
        if network is not None:
            request.wirtnNetwork = network
        if target_address is not None:
            request.pduDestination = Address(target_address)
        else:
            request.pduDestination = LocalBroadcast()
        iocb = self._send_request(request, True)

    def what_is_network_number(self, target_address: Optional[str] = None):
        request = WhatIsNetworkNumber()
        if target_address is not None:
            request.pduDestination = Address(target_address)
        else:
            request.pduDestination = LocalBroadcast()
        iocb = self._send_request(request, True)

    def ping(self, target_address: str, device_id: Optional[int] = None, device_address: Optional[str] = None) -> dict:
        self.logging(f"ping({target_address}-{device_id}-{device_address})")
        if re.match(r"^\d+:\d+$", target_address):
            if device_address is None:
                raise Exception(f"device_address is null")
            self.route(device_address, int(target_address.split(':')[0]))

        now = BaseCommon.get_datetime_str()
        self.discover(device_id, device_id, target_address)
        time.sleep(3)
        bacnet_device = self.bacnet_devices.get(target_address, {})
        if bacnet_device.get('update', now) > now:
            return bacnet_device
        return {}

    def read_property(self, target_address: str, object_type: str, instance_number: int, property_name: str, property_index: Optional[int] = None):
        self.logging(f"read property({target_address}-{object_type}-{instance_number}-{property_name}-{property_index})")
        value = ['Good', '']
        try:
            request = ReadPropertyRequest(objectIdentifier=(object_type, instance_number), propertyIdentifier=property_name, propertyArrayIndex=property_index)
            request.pduDestination = Address(target_address)
            iocb = self._send_request(request, True)
            value[1] = self._parse_response(request, iocb)
        except Exception as e:
            value = ['Bad', e.__str__()]
        return value

    def read_properties(self, target_address: str, object_type: str, instance_number: int, properties: Optional[list] = None, use_read_multiple: bool = True) -> dict:
        self.logging(f"read properties({target_address}-{object_type}-{instance_number}-{properties}-{use_read_multiple})")
        results = {}
        if properties is None:
            properties = ['objectName', 'description', 'presentValue']

        if use_read_multiple is True:
            property_reference_list = []
            for property_identifier in properties:
                prop_reference = PropertyReference(propertyIdentifier=property_identifier,)
                property_reference_list.append(prop_reference)

            read_access_spec = ReadAccessSpecification(objectIdentifier=(object_type, instance_number), listOfPropertyReferences=property_reference_list,)

            request = ReadPropertyMultipleRequest(listOfReadAccessSpecs=[read_access_spec])
            request.pduDestination = Address(target_address)
            iocb = self._send_request(request)
            results.update(self._parse_response(request, iocb))
        else:
            for property_identifier in properties:
                value = self.read_property(target_address, object_type, instance_number, property_identifier)
                results[self._gen_key(target_address, object_type, instance_number, property_identifier)] = value
                if value[0] == 'Good':
                    self._update_device(target_address, **{'object_type': object_type, 'instance_number': instance_number, property_identifier: value[1]})
        return results

    def read(self, target_address: str, objct_propertys: list, device_address: Optional[str] = None, max_per_request: Optional[int] = None, use_read_multiple: bool = True):
        self.logging(f"read({target_address}-{len(objct_propertys)}-{device_address}-{max_per_request}-{use_read_multiple})")
        results = {}
        bacnet_device = self.ping(target_address, None, device_address)  # 测试设备
        if len(bacnet_device) == 0:
            raise Exception(f"device({target_address}) not find")
        if use_read_multiple is True:
            read_access_specs = []
            for object_type, instance_number, property_identifier in objct_propertys:
                read_access_specs.append(ReadAccessSpecification(objectIdentifier=(object_type, instance_number), listOfPropertyReferences=[PropertyReference(propertyIdentifier=property_identifier)]))

            read_access_specs = BaseCommon.chunk_list(read_access_specs, max_per_request if max_per_request is not None else self.bacnet_max_per_request)
            for read_access_spec in read_access_specs:
                request = ReadPropertyMultipleRequest(listOfReadAccessSpecs=read_access_spec)
                request.pduDestination = Address(target_address)
                iocb = self._send_request(request)
                results.update(self._parse_response(request, iocb))
        else:
            for object_type, instance_number, property_identifier in objct_propertys:
                value = self.read_property(target_address, object_type, instance_number, property_identifier)
                results[self._gen_key(target_address, object_type, instance_number, property_identifier)] = value
                if value[0] == 'Good':
                    self._update_device(target_address, **{'object_type': object_type, 'instance_number': instance_number, property_identifier: value[1]})
        return results

    def _cast_value(self, value, datatype):
        if isinstance(datatype, Integer):
            value = int(value)
        elif isinstance(datatype, Real):
            value = float(value)
        elif isinstance(datatype, Unsigned):
            value = int(value)
        return datatype(value)

    def _convert_value_to_set(self, value, datatype, index):
        bac_value = None
        if value is None or value == 'null':
            bac_value = Null()
        elif issubclass(datatype, Atomic):
            bac_value = self._cast_value(value, datatype)
        elif issubclass(datatype, Array) and (index is not None):
            if index == 0:
                bac_value = Integer(value)
            elif issubclass(datatype.subtype, Atomic):
                bac_value = datatype.subtype(value)
            elif not isinstance(value, datatype.subtype):
                raise TypeError(f"invalid result datatype, expecting {datatype.subtype.__name__}")
        elif not isinstance(value, datatype):
            raise TypeError(f"invalid result datatype, expecting {datatype.__name__}")
        return bac_value

    def write(self, target_address: str, object_type: str, instance_number: int, property_name: str, value, priority: Optional[int] = None, index: Optional[int] = None):
        self.logging(f"write({target_address}-{object_type}-{instance_number}-{property_name}-{value}-{priority}-{index})")
        request = WritePropertyRequest(objectIdentifier=(object_type, instance_number), propertyIdentifier=property_name)
        bac_value = self._convert_value_to_set(value, get_datatype(object_type, property_name), index)
        request.propertyValue = Any()
        request.propertyValue.cast_in(bac_value)
        request.pduDestination = Address(target_address)
        if index is not None:
            request.propertyArrayIndex = index
        if priority is not None:
            request.priority = priority

        iocb = self._send_request(request)
        result = self._parse_response(request, iocb)
        if isinstance(result, SimpleAckPDU):
            return value
        raise RuntimeError(f"fail to set value: {result}")

    def _create_cov_subscription(self, target_address: str, object_type: str, instance_number: int, lifetime: Optional[int] = None, confirmed: bool = True):
        if self._get_application():
            subscription = None
            for sub in self._get_application().sub_cov_contexts.values():
                if sub.target_address == target_address and sub.object_type == object_type and sub.instance_number == instance_number:
                    subscription = sub
                    break
            if subscription is None:
                subscription = SubscriptionContext(target_address, object_type, instance_number, self._get_application().cov_sub_process_id, lifetime, confirmed)
                self._get_application().sub_cov_contexts[self._get_application().cov_sub_process_id] = subscription
                self._get_application().cov_sub_process_id += 1
            if subscription:
                self._send_cov_subscription(subscription.target_address, subscription.sub_process_id, subscription.object_type, subscription.instance_number, lifetime, confirmed)

    def _send_cov_subscription(self, target_address: str, sub_process_id: int, object_type: str, instance_number: int, lifetime: Optional[int] = None, confirmed: bool = True):
        request = SubscribeCOVRequest(subscriberProcessIdentifier=sub_process_id, monitoredObjectIdentifier=(object_type, instance_number), issueConfirmedNotifications=confirmed, lifetime=lifetime)
        request.pduDestination = Address(target_address)
        iocb = self._send_request(request)
        return self._parse_response(request, iocb)

    def cov(self, target_address: str, object_type: str, instance_number: int, lifetime: int = 180, renew: bool = False):
        try:
            self.logging(f"cov({target_address}-{object_type}-{instance_number}-{lifetime}-{renew})")
            self._create_cov_subscription(target_address, object_type, instance_number, lifetime)
        except Exception as e:
            pass
        if renew and lifetime > self.cov_update_buffer:
            # 定时触发
            BaseCommon.SimpleTimer().run(lifetime - self.cov_update_buffer, self.cov, kwargs={'target_address': target_address, 'object_type': object_type, 'instance_number': instance_number, 'lifetime': lifetime, 'renew': renew})

    def route(self, target_address: str, network: int):
        self.logging(f"route({target_address}-{network})")
        if self._get_application():
            self._get_application().add_router(target_address, network)

    # 6:2
    def scan(self, target_address: str, device_address: Optional[str] = None, use_read_multiple: bool = True):
        bacnet_device = self.ping(target_address, None, device_address)  # 测试设备
        if len(bacnet_device) == 0:
            raise Exception(f"device({target_address}) not find")

        device_id = bacnet_device.get('device_id')

        # 读取数量
        objects = {}
        self.logging(f"scan({target_address}-{device_address}-{use_read_multiple})")
        quality, object_count = self.read_property(target_address, 'device', device_id, 'objectList', 0)
        if quality == 'Good':
            for array_index in range(1, object_count + 1):
                try:
                    # self.logging(f"scan {target_address} current object({array_index}/{object_count})")
                    quality, object_instance = self.read_property(target_address, 'device', device_id, 'objectList', array_index)
                    if quality == 'Good':
                        self._update_device(target_address, object_type=object_instance[0], instance_number=object_instance[1], property_index=array_index)
                        # self.logging(f"scan {target_address} current object({array_index}/{object_count}) property")
                        objects[self._gen_key(target_address, object_instance[0], object_instance[1])] = self.read_properties(target_address, object_instance[0], object_instance[1], None, use_read_multiple)
                except Exception as e:
                    print(e.__str__())
        return objects

    def _update_device(self, target_address: str, **kwargs):
        if target_address not in self.bacnet_devices.keys():
            self.bacnet_devices[target_address] = {'objects': {}}

        if 'object_type' in kwargs.keys() and 'instance_number' in kwargs.keys():
            key = f"{kwargs.get('object_type')}_{kwargs.get('instance_number')}"
            if key not in self.bacnet_devices[target_address]['objects']:
                self.bacnet_devices[target_address]['objects'][key] = {}
            if 'presentValue' in kwargs.keys():
                kwargs['update'] = BaseCommon.get_datetime_str()
            self.bacnet_devices[target_address]['objects'][key].update(kwargs)

    def devices(self, target_address: Optional[str] = None):
        if target_address is not None:
            return self.bacnet_devices.get(target_address)
        return self.bacnet_devices

    def simluate(self, objects: List[SimulateObject]):
        for object in objects:
            self._create_object(object)

    def _make_mutable(self, object, identifier="presentValue", mutable=True):
        for prop in object.properties:
            if prop.identifier == identifier:
                prop.mutable = mutable
        return object

    def _create_object(self, object: SimulateObject):
        if self._get_application() is not None:
            object_type = object.get('object_type')
            instance_number = object.get('instance_number')
            if object_type is not None and instance_number is not None:
                key = f"{object_type}_{instance_number}"
                if key not in self.bacnet_objects.keys():
                    object_classs = {
                        'analogInput': AnalogInputObject,
                        'analogOutput': AnalogOutputObject,
                        'analogValue': AnalogValueObject,
                        'binaryInput': BinaryInputObject,
                        'binaryOutput': BinaryOutputObject,
                        'binaryValue': BinaryValueObject,
                        'multiStateInput': MultiStateInputObject,
                        'multiStateOutput': MultiStateOutputObject,
                        'multiStateValue': MultiStateValueObject,
                        'bitstringValue': BitStringValueObject,
                        'characterstringValue': CharacterStringValueObject,
                        'octetstringValue': OctetStringValueObject,
                    }
                    object_class = object_classs.get(object_type)
                    if object_class is not None:
                        new_object = object_class(
                            objectIdentifier=(object_type, instance_number),
                            objectName=object.get('object_name', key),
                            presentValue=object.get('present_value', ''),
                            description=CharacterString(object.get('description', '')),
                            statusFlags=StatusFlags(),
                        )
                        new_object = self._make_mutable(new_object, mutable=object.get('mutable', False))
                        self._get_application().add_object(new_object)
                        self.bacnet_objects[key] = new_object

    def update_object(self, object_type: str, instance_number: int, value = None, flags = [0, 0, 0, 0]):
        self.logging(f"update object({object_type}-{instance_number}-{value})")
        key = f"{object_type}_{instance_number}"
        if key in self.bacnet_objects.keys():
            self.bacnet_objects[key].presentValue = value
            self.bacnet_objects[key].statusFlags = flags

    def logging(self, content: str):
        print(content)
