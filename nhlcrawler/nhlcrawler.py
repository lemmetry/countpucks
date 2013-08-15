import queue
import threading
from time import time
from nhldotcom import *


class TaskProcessorThread(threading.Thread):
    def __init__(self, context):
        threading.Thread.__init__(self)
        self.context = context

    def run(self):
        while not self.context.stop_flag:
            thread_id = self.getName()
            task = self.context.getTask()
            if task is None:
                if thread_id not in self.context.waiting_threads:
                    self.context.waiting_threads.append(thread_id)
                continue

            if thread_id in self.context.waiting_threads:
                self.context.waiting_threads.remove(thread_id)

            result = task.processTask(self.context)
            # print(self.getName(), result)

            self.context.submitTask([result])


class CrawlerContext():
    queue = queue.Queue()
    queue_condition = threading.Condition(threading.RLock())
    queue.put(ABCTask('http://www.nhl.com/ice/playersearch.htm'))
    # queue.put(LetterTask('http://www.nhl.com/ice/playersearch.htm?letter=Z'))

    stop_flag = False
    waiting_threads = []

    def getTask(self):
        self.queue_condition.acquire()
        try:
            if not self.queue.empty():
                task = self.queue.get()
                self.queue.task_done()
            else:
                return
        finally:
            self.queue_condition.notify_all()
            self.queue_condition.release()
        return task

    def submitTask(self, tasks):
        for task in tasks:
            self.queue_condition.acquire()
            self.queue.put(task)
            self.queue_condition.notify_all()
            self.queue_condition.release()


def main():
    print('main started')
    t1 = time()

    context = CrawlerContext()

    threads = [TaskProcessorThread(context) for _ in range(50)]
    for t in threads:
        t.daemon = True
    [t.start() for t in threads]

    while len(context.waiting_threads) < 50:
        continue

    for t in threads:
        t.context.stop_flag = True
    [t.join() for t in threads]

    print('main finished, total time: ', time() - t1)

main()