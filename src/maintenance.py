from threading import Thread
import time

class Maintenance(Thread):
    def __init__(self, worker, sleep_time=3):
        super().__init__()
        self.worker = worker
        self.sleep_time = sleep_time  # do maintenance every @sleep_time seconds

    def run(self):
        while True:
            # print("I am maintenance thread.", flush=True)
            self.worker.stabilize()
            self.worker.fix_finger()
            self.worker.check_predecessor()
            time.sleep(self.sleep_time)
