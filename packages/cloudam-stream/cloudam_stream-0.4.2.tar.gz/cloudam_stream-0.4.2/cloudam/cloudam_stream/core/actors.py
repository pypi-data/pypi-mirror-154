from typing import TypeVar, Generic, List
from cloudam_stream.core.ports.outputports import OutputPort
from cloudam_stream.core.ports.inputports import InputPort
T = TypeVar('T')


class Args(object):
    pass


class Actor(Generic[T], object):

    def __init__(self, name: str = None, actor_id: str = None):
        self.__name = name
        self.__id = actor_id
        self.__output_ports = []
        self.__input_ports = []
        self.__parameters = {}
        self.__parameter_overrides = {}
        self.args = Args()

    def begin(self):
        pass

    def end(self):
        pass

    def emit(self, data: T):
        for port in self.__output_ports:
            port.emit(data)

    def set_input_ports(self, input_ports: list[InputPort]):
        self.__input_ports = input_ports

    def get_input_ports(self):
        return self.__input_ports

    def set_output_ports(self, output_ports: list[OutputPort]):
        self.__output_ports = output_ports

    def get_output_ports(self):
        return self.__output_ports

    def set_parameters(self, parameters: {}):
        self.__parameters = parameters

    def get_parameters(self):
        return self.__parameters

    def set_parameter_overrides(self, parameter_overrides: {}):
        self.__parameter_overrides = parameter_overrides

    def get_parameter_overrides(self):
        return self.__parameter_overrides


class ComputeActor(Actor):

    def process(self, item: [T], port=None):
        pass


class ParallelComputeActor(ComputeActor):

    def process(self, item, port=None):
        pass


class SinkActor(Actor):

    def write(self, data, port):
        pass


class SourceActor(Actor):

    def __iter__(self):

        pass

