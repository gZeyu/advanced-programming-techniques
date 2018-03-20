from concurrent.futures import ThreadPoolExecutor
import time
import random
import queue
import threading


def return_future_result(message):

    print(threading.current_thread().name)
    time.sleep(2)
    return message


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2)
    future1 = pool.submit(return_future_result, ("hello"))  # 往线程池里面加入一个task
    future2 = pool.submit(return_future_result, ("world"))  # 往线程池里面加入一个task
    print(future1.done())  # 判断task1是否结束
    time.sleep(3)
    print(future2.done())  # 判断task2是否结束
    print(future1.result())  # 查看task1返回的结果
    print(future2.result())  # 查看task2返回的结果
