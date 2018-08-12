import threading
import queue
import os
import time

buffer_size = 5
lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0
flag = 0

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue
    try:
        global flag
        if flag == 0:
            queue_buffer.put(top_dir,timeout=1)
            flag = 1
        files=os.listdir(top_dir)
        for i in files:
            p1=os.path.join(top_dir,i)
            if os.path.isdir(p1):
                queue_buffer.put(p1,timeout=1)
                producer(p1,queue_buffer)
    except:
        pass


def consumer(queue_buffer):
    # search file in directory
    global file_count
    start = time.time()
    try:
        while True:
            path=queue_buffer.get(timeout=1)
            files=os.listdir(path)
            for i in files:
                p1=os.path.join(path,i)
                if os.path.isfile(p1):
                    lock.acquire()
                    file_count = file_count+1
                    lock.release()
        
            end = time.time()
            interval=end-start
            if interval>1:
                break
    except:
        pass
        


def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 10
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.') 
    # win計算為114,mac計算為115
    # mac會多一個.DS_Store的檔案,是apple為OSX作業系統創的隱藏文件
    # .DS_Store目的在於存貯目錄的自定義屬性

if __name__ == "__main__":
    main()
