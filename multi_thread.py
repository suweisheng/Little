#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import traceback
import multiprocessing
import multiprocessing.sharedctypes
import ctypes

ENCODING = 'utf8'
if sys.platform == 'win32':
    ENCODING = 'gbk'
reload(sys)
sys.setdefaultencoding(ENCODING)

def task1(num):
    try:
        num = str(num)
        print "child: {}, pro: {} start".format(num, os.getpid())
        # sys.stdout.write("child: {}, pro: {} start\n".format(num, os.getpid()))
        if int(num) % 2 == 0:
            time.sleep(3)
        else:
            time.sleep(1)
        print "child: {}, pro: {} end".format(num, os.getpid())
        # sys.stdout.write("child: {}, pro: {} end\n".format(num, os.getpid()))
        return num
    except Exception as e:
        print traceback.format_exc()
        # raise Exception("".join(traceback.format_exception(*sys.exc_info())))

def callback(num):
    num = str(num)
    print "%s -> in callback" % num

def error_callback(msg):
    print msg



def task2(num):
    try:
        num = str(num)
        sys.stdout.write("child: {}, pro: {} start\n".format(num, os.getpid()))
        if int(num) % 2 == 0:
            time.sleep(3)
        else:
            time.sleep(1)
        sys.stdout.write("child: {}, pro: {} end\n".format(num, os.getpid()))
        return num
    except Exception as e:
        print traceback.format_exc()
        # raise Exception("".join(traceback.format_exception(*sys.exc_info())))

class MockOut(object):
    # 构造一个模拟输出的类，输出内容到 qu
    def __init__(self, qu):
        self.qu = qu
        self.cache = []
    def write(self, content):
        if content.endswith("\n"):
            if self.cache:
                self.cache.append(content)
                self.qu.put(['p', ''.join(self.cache)])
                self.cache = []
            else:
                self.qu.put(['p', content])
        else:
            self.cache.append(content)

    def error(self, content):
        self.write(content)
        self.flush()
        self.qu.put(['e'])

    def flush(self):
        self.qu.put(['f'])

def init_stdout(qu):
    # 修改每个进程的标准输出，让每个进程的输出放入统一放到同一个队列
    import sys
    reload(sys)
    sys.setdefaultencoding(ENCODING)
    sys.stdout = MockOut(qu)

def print_out(qu):
    # 最好单独开一进程循环检查 队列(get内容输出)，队列内容是从多个进程put进来的
    is_error = False
    while True:
        try:
            obj = qu.get()
        except Exception, e:
            print e
            break
        if is_error:
            continue
        cmd = obj[0]
        if cmd == "p":
            content = obj[1]
            sys.stdout.write(content)
        elif cmd == "f":
            sys.stdout.flush()
        elif cmd == "e":
            is_error = True


def task3(data, shared_values, shared_arrays,
            single_value, single_array, d_proxy, l_proxy, g_namespace):
    # 多进程锁，拿锁，block：是否阻塞（默认true）,timeout：阻塞拿锁最多等待时间（block为true该值才有意义）
    # 返回值：true or flase 是否拿到锁
    try:
        data["lock"].acquire(block=True, timeout=None)
        # print data["s1"] # 不共享
        # print shared_values[0].value # 共享值
        # print shared_arrays[0][1] # 共享数组
        # print single_value.value
        # print single_array[2]
        # print d_proxy
        # print l_proxy
        # print g_namespace.x

        for i in xrange(2):
            print os.getpid(), data["content"]

        # data["s1"] = None
        # shared_values[0].value = 100000
        # shared_arrays[0][1] = 1000000
        # single_value.value = 100000
        # single_array[2] = 100000
        # d_proxy['a'] = 100000
        # g_namespace.x = 100000

        # 多进程锁，释放锁
        data["lock"].release()
    except Exception as e:
        print traceback.format_exc()


def task4(num, msg_queue, msg_list, msg_dict):
    try:
        if num == 2:
            time.sleep(2)
        else:
            time.sleep(1)
        msg_queue.put("num:"+str(num) + ", "+str(os.getpid()))
        # msg_list[num] = "sss"
        msg_dict[num] = "num:"+str(num) + ", "+str(os.getpid())
    except Exception as e:
        print traceback.format_exc()

task5_g_queue = None
def init_pool(qu):
    global task5_g_queue
    task5_g_queue = qu

def task5(data):
    num = data[0]
    mgr_queue = data[1]
    try:
        if num == 0:
            time.sleep(2)
        else:
            time.sleep(1)
        task5_g_queue.put("num:{}, pid:{}".format(num, os.getpid()))
        mgr_queue.put("num:{}, pid:{}".format(num, os.getpid()))
    except Exception as e:
        print traceback.format_exc()


def test_apply(pool):
    # pool = multiprocessing.Pool(processes = 2)
    # apply 和 apply_async 单次只执行一个任务，但 apply_async 可以异步执行
    # 将其作为单独的任务提交到进程池
    for i in xrange(6):
        # apply 同步，阻塞主进程，子进程间也阻塞，进程池一次只能一个进程在运行
        # pool.apply(task1, [i])
    
        # apply_async 异步, 不阻塞主进程，但如果主进程结束，全部子进程也会退出，进程池一次可以有多个进程运行，进程间并行运行
        ret = pool.apply_async(func=task1, args=(i,), callback=callback)
        # ret = ret.get(timeout=999999) # 延迟获取结果，会阻塞 unless your computer is *very* slow
        # print ret

def test_map(pool):
    # pool = multiprocessing.Pool(processes = 2)
    # map 和 map_async 单次执行多个任务，任务开始按照迭代器迭代顺序运行, 但任务完成顺序不能保证
    # 将其作为多个任务提交到进程池，任务参数只能一个

    # map 同步, 阻塞主进程，任务列表中所有任务完成才继续主进程，进程池一次可以有多个进程运行，进程间并行运行
    # ret = pool.map(func=task1, iterable=[0,1,2,3,4,5,6])
    # ret = pool.map(func=task1, iterable=range(7))
    # print ret

    # map_async 异步, 不阻塞主进程，但如果主进程结束，全部子进程也会退出，进程池一次可以有多个进程运行，进程间并行运行
    ret = pool.map_async(func=task1, iterable=range(10), callback=callback)
    ret = ret.get(timeout=99999) # 延迟获取结果，会阻塞，结果的顺序跟迭代器任务的顺序一致
    print ret

def test_start(pool):
    # 注意：python2.x 没有该函数
    # pool = multiprocessing.Pool(processes = 2)
    # starmap、starmap_async 功能与 map 和 map_async 相同，差别是任务可以传入多个参数
    # 将其作为多个任务提交到进程池，任务参数可以多个 ）

    # starmap 同步, 阻塞主进程，任务列表中所有任务完成才继续主进程，进程池一次可以有多个进程运行，进程间并行运行
    # ret = pool.starmap(func=task1, iterable=[(0,), (1,), (2,), (3,), (4,), (5,), (6,)])

    # 异步, 不阻塞主进程，但如果主进程结束，全部子进程也会退出，进程池一次可以有多个进程运行，进程间并行运行
    ret = pool.starmap_async(func=task1, iterable=[(0,), (1,), (2,), (3,), (4,), (5,), (6,)])

def test_imap(pool):
    # pool = multiprocessing.Pool(processes = 2)
    # imap、imap_unordered 功能与 map_async 相同，差别是获取任务结果
    # 在获取进程池中的结果时，map_async、imap、imap_unordered三个方法都会阻塞
    # map_async需要等待所有Task执行结束后返回list
    # imap 和 imap_unordered 可以尽快返回一个Iterable的结果

    # 异步, 不阻塞主进程，但如果主进程结束，全部子进程也会退出，进程池一次可以有多个进程运行，进程间并行运行
    ret = pool.imap(func=task1, iterable=range(3))
    for i in ret: print "ret:",i

    # 异步, 不阻塞主进程，但如果主进程结束，全部子进程也会退出，进程池一次可以有多个进程运行，进程间并行运行
    # ret = pool.imap_unordered(func=task1, iterable=range(3))
    # for i in ret: print "ret:",i
        
def test_process():
    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = cpu_count) # 创建进程池，进程最大数量为指定值，但不会超过cpu核数

    # test_apply(pool)
    test_map(pool)
    # test_start(pool)
    # test_imap(pool)
        
    pool.close() # 进程池关闭，防止任何其他任务提交到池。一旦所有任务完成，工作进程将退出。
    pool.join() # 等待工作进程退出,使用前必须调用 close

def test_queue():
    queue = multiprocessing.Queue() # 多进程的队列
    # queue.qsize() # 当前队列对象数量
    # queue.empty(); queue.full(); # 判断队列是否空/满，在多进程下不可靠

    # obj：放入队列的对象；block：是否阻塞(默认True)；timeout：最多阻塞时间（默认None,block为True时值才有效）
    queue.put(obj=[1,], block=True, timeout=None)

    obj = queue.get(block=True, timeout=None)
    print obj

    queue.close() # 指示当前进程不会在此队列上放置更多数据
    queue.join_thread() # 阻塞直到后台线程退出,确保缓冲区中的所有数据都已刷新到管道。
    queue.cancel_join_thread() # 需要当前的进程立即退出,而不等待刷新排队的数据到底层的管道，你不在乎丢失的数据。

def test_process_queue():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=print_out, args=(queue,))
    p.daemon = True
    p.start()

    init_stdout(queue)

    pool = multiprocessing.Pool(processes=4, initializer=init_stdout, initargs=(queue,))

    ret = pool.map_async(func=task2, iterable=range(10))
    print ret.get(99999)

    pool.close()
    pool.join()

def test_lock_and_share_cache():
    lock = multiprocessing.Lock()
    # not share_data
    not_share_data = [1,2,3] # 数据不会共享，在每个进程修改也不会影响其他进程，数据只是个副本

    # shared_values
    values = [('i', 10), ('h', -2), ('d', 1.25)] # i:integer; h;short; d:double
    shared_values = [multiprocessing.Value(id, v) for id, v in values] # 列表里的数据是共享的
    # shared_arrays
    arrays = [('i', range(3)),]
    shared_arrays = [multiprocessing.Array(id, a) for id, a in arrays]
    # single shared_value shared_array
    single_value = multiprocessing.sharedctypes.Value('i', 7)
    single_array = multiprocessing.sharedctypes.Array('i', [1,2,3])
    # share manager
    manager = multiprocessing.Manager()
    d_proxy = manager.dict()
    # d_proxy = manager.dict({'a':1, 'b':2})
    # d_proxy = manager.dict([('a', 1), ('b', 2)])
    # d_proxy = manager.dict(a=1, b=2)
    d_proxy['a'] = 1
    d_proxy['b'] = 2
    # l_proxy = manager.list()
    # l_proxy = manager.list([1,2])
    l_proxy = manager.list((1, 2))
    # l_proxy.append(3)
    # l_proxy.append(4)
    g_namespace = manager.Namespace()
    g_namespace.x = 10


    data1 = dict(lock=lock, content=1, s1=not_share_data)
    p1 = multiprocessing.Process(target=task3, args=(data1, shared_values,shared_arrays,
                                single_value, single_array, d_proxy, l_proxy, g_namespace))

    data2 = dict(lock=lock, content=2, s1=not_share_data)
    p2 = multiprocessing.Process(target=task3, args=(data2, shared_values, shared_arrays,
                                single_value, single_array, d_proxy, l_proxy, g_namespace))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

def test_process_share():
    # 不同于 multiprocessing.Pool, multiprocessing.Process 没有返回任务执行结果，返回的是进程对象
    # 如需要接收任务结果，可以传递 multiprocessing.Queue
    # 多进程queue 必须在工作进程初始化就传入，共享内存必须在工作进程初始化时就传入
    # multiprocessing.Process() 调用就是工作进程的初始化，并开始任务执行
    # multiprocessing.Pool() 调用就是工作进程的初始化（可以设置参数(initializer=init_stdout, initargs=(queue,)
    # 但 Pool.map_async(), Pool.apply_async 调用工作进程开始热瓦卢无，此时工作进程早已初始化，所以任务接收的参数不能共享
    msg_list = multiprocessing.sharedctypes.Array(ctypes.c_char_p, 7)
    msg_dict = multiprocessing.Manager().dict()
    msg_queue = multiprocessing.Queue()
    for i in xrange(6):
        # print i
        # pool.apply_async(func=task4, args=(i, msg_queue,))
        p = multiprocessing.Process(target=task4, args=(i, msg_queue, msg_list, msg_dict, ))
        p.start()

    try:
        while True: print msg_queue.get(True, 3)
    except:
        pass

    for x in msg_list:
        print x
    for k, v in msg_dict.items():
        print k, v

def test_process_share2():
    # multiprocessing.Pool 已经具有共享的结果队列，不需要另外包含 Manager.Queue。
    # Manager.Queue 是位于内部的queue.Queue(多线程队列)，位于单独的服务器进程上，并通过代理公开。
    # 与Pool的内部队列相比，这增加了额外的开销。
    # 与依赖Pool的本地结果处理相反，Manager.Queue中的结果也不能保证被排序。
    # https://www.codenong.com/9908781/ 参考
    mgr = multiprocessing.Manager()
    mgr_queue = mgr.Queue() # 可以作为共享内存出入 map_async 的任务参数

    init_queue = multiprocessing.Queue()

    pool = multiprocessing.Pool(processes=4, initializer=init_pool, initargs=(init_queue, ))

    # ret = pool.map_async(func=task5, iterable=range(5))

    param_list = list()
    for i in xrange(5):
        param_list.append((i, mgr_queue))
    ret = pool.map_async(func=task5, iterable=param_list)
    ret = ret.get(timeout=99999) # 阻塞

    while not init_queue.empty():
        print "init_queue", init_queue.get(True, 4)

    while not mgr_queue.empty():
        print "mgr_queue", mgr_queue.get(True, 4)

    pool.close()
    pool.join()


def mul_thread():
    test_process_share2()
    # time.sleep(10)

    # start_time = time.time()
    # end_time = time.time()
    # print "start_time:{}, end_time:{}, diff_time:{}".format(start_time, end_time, end_time-start_time)


if __name__ == "__main__":
    mul_thread()