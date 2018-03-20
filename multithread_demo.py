# -*- coding: utf-8 -*-
import time
import threading
import random
import queue


def read(q):
    while True:
        if q.empty():
            break
        value = q.get()
        print('Get %s from queue.' % value + threading.current_thread().name)
        time.sleep(random.random())


def main():
    q = queue.Queue()
    pw1 = threading.Thread(target=read, args=(q, ))
    pw2 = threading.Thread(target=read, args=(q, ))
    pw1.daemon = True
    pw2.daemon = True
    for c in [chr(ord('A') + i) for i in range(26)]:
        q.put(c)
    pw1.start()
    pw2.start()


if __name__ == '__main__':
    main()
    print("end")
