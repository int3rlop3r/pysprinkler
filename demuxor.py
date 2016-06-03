
class TaskDispatcher:

    def __init__(self, tasks=None):
        self._started = False
        self._started_jobs = []

        if tasks:
            self._tasks = tasks
        else:
            self._tasks = []

    def add(self, task):
        if self._started:
            raise RuntimeError("Task loop already started, can't add more tasks")
        self._tasks.append(task)

    def run(self):
        if not self._tasks:
            raise RuntimeError("Can't start the task loop, no tasks added")

        self._started = True

        # start all generators
        for task in self._tasks:
            co_obj = task._start()
            next(co_obj)
            self._started_jobs.append(co_obj)

        try:
            while True:
                data = (yield)
                for job in self._started_jobs:
                    job.send(data)
        except GeneratorExit, e:
            for job in self._started_jobs:
                job.close()

class Demultiplexer:

    def __init__(self, tasks=None):
        self.task_dispatcher = TaskDispatcher(tasks)

    def add(self, task):
        self.task_dispatcher.add(task)

    def start(self):
        self.task_loop = self.task_dispatcher.run()
        next(self.task_loop)
        return self

    def send(self, data):
        self.task_loop.send(data)

    def close(self):
        self.task_loop.close()

class Task:
    def _start(self):
        try:
            while True:
                data = (yield)
                self.on_data(data)
        except GeneratorExit, e:
            self.on_end()

if __name__ == '__main__':
    pass


