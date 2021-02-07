import time
from multiprocessing import Pool, Process, Manager,Queue
from queue import Empty, Full


list_numbers = list(range(1,36))


def get_results(q_out):
    while True:
        try:
            item = q_out.get(block=True, timeout=1)
        except Empty:
            print("get results - q out is empty")
            time.sleep(3)
        else:
            print(item)


def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return(recur_fibo(n-1) + recur_fibo(n-2))


class MyProcess(Process):
    def __init__(self, name, q_in, q_out):
        super().__init__(name=name)
        self.q_in = q_in
        self.q_out = q_out

    def run(self):
        print("--- {} Started ---".format(self.name))
        while True:
            try:
                item = self.q_in.get(block=True, timeout=1)
            except Empty:
                print(f"{self.name} - execute_task - q in is empty")
                time.sleep(2)
                return

            item = recur_fibo(item)
            try:
                self.q_out.put(item, timeout=1)
            except Full:
                print(f"{self.name} execute_task - q_out is full")


def insert_input():
    for i in list_numbers:
        try:
            queue_in.put(i, timeout=1)
        except Full:
            print("insert_numbers - q_out is full")
    # queue_in.put(None, timeout=1)


if __name__ == '__main__':
   # m = Manager()
    queue_in = Queue()
    queue_out = Queue()
    insert_input()
    l_p = []
    l_finished = {}

    # pool = Pool(processes=5)
    #result = pool.map(lulu, range(1,21))
    for i in range(1,6):
        p = MyProcess(name=f"Process {i}", q_in=queue_in, q_out=queue_out)
        p.start()
        l_p.append(p)
    # [pool.apply_async(execute_task, (i,)) for i in range(10)]
    # async_results = pool.apply_async(execute_task, (queue_in, queue_out))
    p_results = Process(target=get_results, args=(queue_out,))
    p_results.start()
    # results = [res.get() for res in async_results]
    print([p.name for p in l_p])
    try:
        while(True):
            for p in l_p:
                if p.exitcode is None:
                    print(f"{p.name} - still running")
                else:
                    l_finished[p.name] = p.exitcode
                    print(l_finished)
                time.sleep(2)
                if len(l_finished) == len(l_p):
                    raise  Exception

    except Exception:
        print("all process finished")
        p_results.terminate()
        for p in l_p:
            p.join()
