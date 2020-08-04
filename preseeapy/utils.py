import types
from multiprocessing import Process, Queue


class ProcessHandler():
    """A ProcessHandler object gets a function to attach to a
       subprocess.
    """
    def __init__(self, attach_function: types.FunctionType):
        # It is necessary for later usability that the function
        # object contains a magic function __call__
        if not hasattr(attach_function, '__call__'):
            raise ValueError("Attach function object to ProcessHandler!")

        self._queue = Queue()
        self._process = self._start_process(attach_function)

    def _start_process(self, function) -> Process:
        """Start a parallel thread to run the twisted reactor in.

        Args:
            queue (multiprocessing.Queue): [description]

        Returns:
            multiprocessing.Process: [description]
        """
        p = Process(target=function,
                    args=(self._queue,))
        p.start()

        return p

    def get_queue_content(self):
        content = self._queue.get()

        return content

    def close(self):
        self._process.join()
