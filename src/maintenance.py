from threading import Thread
import time

class Maintenance(Thread):
    def __init__(self, worker, sleep_time=3):
        super().__init__()
        self.worker = worker
        self.sleep_time = sleep_time  # do maintenance every @sleep_time seconds
        print("Maintenance.__init()__")

        # for debugging
        self.num_maintenance_done = 0

    def run(self):
        while True:
            # call stabilize()
            # call fix_finger()
            # call check_predecessor()
            print("I am maintenance thread.", self.num_maintenance_done, flush=True)
            self.num_maintenance_done += 1
            time.sleep(self.sleep_time)
