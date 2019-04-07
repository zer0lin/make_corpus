import threading
import time


def do_download():
    global l1
    my_key = None
    while True:
        num = 0
        lock.acquire()
        for key, value in l1.items():
            # print(key, value)
            if not value:
                my_key = key
                break
            else:
                num += 1
        if num == len(l1):
            lock.release()
            return
        else:
            l1[my_key] = True
            lock.release()
            if my_key:
                print("{0} --- download --- {1}".format(threading.currentThread(), my_key))
                time.sleep(3)

            fail = False
            if fail:
                lock.acquire()
                l1[my_key] = False
                lock.release()


thread_list = []
lock = threading.Lock()
l1 = {"aaa": False, "bbb": False, "ccc": False, "ddd": False, "eee": False, "fff": False, "ggg": False, "hhh": False}


for i in range(3):
    t = threading.Thread(target=do_download)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()
