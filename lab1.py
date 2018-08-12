import threading
import random
import numpy as np
import multiprocessing
import time

#multi-thread

def thread_func(i, matA,matB,result):
    
    result[i] = np.matmul(matA[i], matB)

def main():
    # How many thread you want to use

    matA = np.random.randint(10, size = (10, 10))
    matB = np.random.randint(10, size = (10, 10))
    result = np.zeros((matA.shape[0],matB.shape[1]),dtype=np.int)
    print ("matA")
    print(matA)
    print ("matB")
    print(matB)

    
    thread_num = 10
    threads = []

    start_time = time.time()

    # Assign job to threads
    for i in range(0,matA.shape[0]):
        # Pass argument to function with tuple
            thread = threading.Thread(target = thread_func, args = (i,matA,matB,result))
            threads.append(thread)

    # run all threads
    for thread in threads:
        thread.start()

    # Wait for threads finish
    for thread in threads:
        thread.join()

    print("Result")
    print(result)

    # compared with result of numpy
    print('Answer is correct:', np.all(np.matmul(matA, matB) == result))

    # time elapsed
    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)


if __name__ == "__main__":
    main()


#multi-process

def process_func(i,matA,matB,result_queue):

    ss = np.matmul(matA[i], matB)
    result_queue.put((i,ss))
    

def main_proc():
    # Generate queue for communication

    result_queue = multiprocessing.Manager().Queue()

    matA = np.random.randint(10, size = (10, 10))
    matB = np.random.randint(10, size = (10, 10))
    result = np.zeros((matA.shape[0],matB.shape[1]),dtype=np.int)
    print ("matA")
    print(matA)
    print ("matB")
    print(matB)

    processes = 10
    jobs = []

    start_time = time.time()

    for i in range(0,matA.shape[0]):
        process = multiprocessing.Process(target = process_func, args = (i,matA,matB,result_queue))
        jobs.append(process)

    for process in jobs:
        process.start()

    for process in jobs:
        process.join()

    while not result_queue.empty():
        res = result_queue.get()
        result[res[0]] = res[1]
        
    print(result)
    
    # compared with result of numpy
    print('Answer is correct:', np.all(np.matmul(matA, matB) == result))
    
    # time elapsed
    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)

if __name__ == "__main__":
    main_proc()


# numpy

def np_main():
    # Generate random matrix and result matrix
    matA = np.random.randint(10, size = (10, 10))
    matB = np.random.randint(10, size = (10, 10))
    result = np.zeros((matA.shape[0], matB.shape[1]))
    start_time = time.time()
    for row in range(0, matA.shape[0]):
        result[row] = np.matmul(matA[row], matB)

    # time elapsed
    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)

    
if __name__ == "__main__":
    np_main()