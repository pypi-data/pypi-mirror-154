from actors import ParallelComputeActor
from ports import TextInputPort
from ports import TextOutputPort


class MyParallelComputeActor(ParallelComputeActor):
    title = "My Parallel Compute Actor"
    name = "Parallel"

    intake = TextInputPort()
    success = TextOutputPort()
    parameter_overrides = {
        "parallelism": 2,
    }

    ss = ""

    def begin(self):
        self.sss = ""

    def process(self, item, port):

        self.success.emit(item)
