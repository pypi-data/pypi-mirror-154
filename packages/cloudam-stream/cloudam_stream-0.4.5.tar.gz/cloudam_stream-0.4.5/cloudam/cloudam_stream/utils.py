from loguru import logger
from lz4 import frame
import base64
import json
import pickle


class FlowStateUtils:

    def __init__(self, redis_client):
        self.redis_client = redis_client

    """
    查询某一actor的整体状态
    """
    def get_actor_final_state(self, redis_key: str, actor_name: str):
        # 查询算子整体状态
        state = self.redis_client.hget(redis_key, actor_name)
        if state:
            state = state.decode()
        logger.info('【core----get_pre_actors_state】actor_name:{},redis_key:{}------>state:{}', actor_name, redis_key,
                    state)
        return state


class Base64Utils:

    """
    base64 编码
    """
    @staticmethod
    def encode(source, encoding='utf-8'):
        source_bytes = source.encode(encoding)
        base64_bytes = base64.b64encode(source_bytes)
        base64_string = base64_bytes.decode(encoding)
        base64_string = base64_string.replace('=', '_')
        return base64_string

    """
    base64 解码
    """
    @staticmethod
    def decode(source, encoding='utf-8'):
        source = source.replace('_', '=')
        base64_bytes = source.encode(encoding)
        string_bytes = base64.b64decode(base64_bytes)
        string = string_bytes.decode(encoding)
        return string


class DictUtils:

    """
    根据属性名查询属性值
    """
    @staticmethod
    def get_property_value(object_desc, property_name, default=None):
        property_value = default
        if type(object_desc) == str:
            object_desc = json.loads(object_desc)
        if type(object_desc) == dict:
            property_value = object_desc.get(property_name, default)
        return property_value


class SerializeUtils:
    """
    序列化
    """
    @staticmethod
    def encode(obj):
        return pickle.dumps(obj)

    """
    反序列化
    """
    @staticmethod
    def decode(obj):
        return pickle.loads(obj)

    """
    序列化、压缩
    """
    @staticmethod
    def encode_lz4(obj):
        msg = pickle.dumps(obj)
        return frame.compress(msg)

    """
    反序列化、解压
    """
    @staticmethod
    def decode_lz4(obj):
        uncompress_obj = frame.decompress(obj)
        return pickle.loads(uncompress_obj)
