from typing import TypeVar, Generic
from .payload import Message, Record
from .streams import RedisProducer
from .utils import SerializeUtils
import json


T = TypeVar("T")


class __Port:

    # 初始化数据，生成需要的相关配置
    def __init__(self, name: str = "", actor_name: str = ""):
        self.name = name
        self.actor = actor_name


class _InputPort(Generic[T], __Port):

    def __init__(self, port_name: str = "", actor_name: str = ""):
        self.channel = actor_name.replace(' ', '_') + '&' + port_name.replace(' ', '_')
        super(_InputPort, self).__init__(port_name, actor_name)


class BinaryInputPort(_InputPort[bytes]):

    pass


class TextInputPort(_InputPort[str]):

    pass


class FloatInputPort(_InputPort[float]):

    pass


class JsonInputPort(_InputPort[dict]):

    pass


class RecordInputPort(_InputPort[Record]):

    pass


class _OutputPort(Generic[T], __Port):

    def __init__(self, producer: RedisProducer = None, name: str = None, actor_name: str = None):
        if name and actor_name:
            self.channel = actor_name.replace(' ', '_') + '&' + name.replace(' ', '_')
        self.producer = producer
        super(_OutputPort, self).__init__(name, actor_name)

    def emit(self, data: T):
        self._emit(data)

    def _emit(self, payload: T):
        message_object = Message(payload, "0", type(payload).__name__)
        print(json.dumps(message_object.__dict__))
        encode_msg = SerializeUtils.encode(message_object)
        self.producer.produce(self.channel, encode_msg)


class TextOutputPort(_OutputPort[str]):

    pass


class BinaryOutputPort(_OutputPort[bytes]):

    pass


class IntOutputPort(_OutputPort[int]):

    pass


class FloatOutputPort(_OutputPort[float]):

    pass


class JsonOutputPort(_OutputPort[dict]):

    pass


class RecordOutputPort(_OutputPort[Record]):

    pass


