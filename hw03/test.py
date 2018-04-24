import time
from queue import Queue
import threading
from threading import Thread
# 创建队列实例， 用于存储任务
queue = Queue()


# 定义需要线程池执行的任务
def do_job():
    while True:
        i = queue.get()
        time.sleep(1)
        print('index %s, curent: %s' % (i, threading.current_thread()))
        queue.task_done()


def work_fun(task_queue):
    while True:
        i = task_queue.get()
        print('index %s, curent: %s' % (i, threading.current_thread()))
        task_queue.task_done()


def Multithread_download(total_page_number=10, max_workers=1):
    task_queue = Queue()
    for i in range(1, total_page_number + 1):
        task_queue.put(i)
    for i in range(max_workers):
        thread = threading.Thread(target=work_fun, args=(task_queue, ))
        thread.daemon = True
        thread.start()
    task_queue.join()


if __name__ == '__main__':
    # 模拟创建线程池3秒后塞进10个任务到队列

    # time.sleep(3)
    # for i in range(10):
    #     queue.put(i)
    # # 创建包括3个线程的线程池
    # for i in range(3):
    #     t = Thread(target=do_job)
    #     t.daemon = True  # 设置线程daemon  主线程退出，daemon线程也会推出，即时正在运行
    #     t.start()

    # queue.join()
    Multithread_download(total_page_number=1000, max_workers=3)
