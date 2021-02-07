import time
from multiprocessing import Pool, Process, Manager
from queue import Empty, Full


list_numbers = list(range(1,41))

def recur_fibo(n):
   if n <= 1:
       return n
   else:
       return(recur_fibo(n-1) + recur_fibo(n-2))


def lulu(q_in, q_out):
    try:
        item = q_in.get(block=True, timeout=5)
    except Empty:
        return None
    fib_item = recur_fibo(item)
    try:
        q_out.put(fib_item, timeout=5)
    except Full:
        print("q_out is full")


# def insert_numbers():
#     for i in range(1,40):
#         queue_in.put


if __name__ == '__main__':
    m = Manager()
    queue_in = m.Queue()
    queue_out = m.Queue()
    pool = Pool(processes=5)
    #result = pool.map(lulu, range(1,21))

    results = pool.apply_async(lulu, (queue_in, queue_out))
    pool.close()
    print(result)
    # for i in range(1,6):
    #     p = Process(lulu, args=(i,))
    #     p.start()
    #     l_p.append(p)
    # for _p in l_p:
    #     _p.join()

