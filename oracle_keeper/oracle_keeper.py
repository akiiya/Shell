import gc
import os
import random
import time
import codecs

import urllib3
import traceback
from io import BytesIO

max_speed_mbs = 1  # 最大下载速度 mb/s
max_memory_mb = 1024 * 3  # 内存占用上限
pid_file_path = '/var/run/oracle_keeper.pid'
download_url_path = 'http://cachefly.cachefly.net/100mb.test'

mem_file = BytesIO()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
timeout = urllib3.Timeout(connect=20, read=30)
manager = urllib3.PoolManager(timeout=timeout, headers=headers)


def save_pid():
    with codecs.open(pid_file_path, 'wb', encoding='utf-8') as f:
        f.write(str(os.getpid()))


def read_pid():
    if os.path.exists(pid_file_path):
        with codecs.open(pid_file_path, 'rb', encoding='utf-8') as f:
            return f.read()
    else:
        return None


# 消耗内存资源
def mem_consume():
    print(f'开始填充内存: {max_memory_mb}MB')
    while True:
        # 消耗内存
        if mem_file.tell() < max_memory_mb * 1024 * 1024:
            mem_file.write(b'0' * 1024)
        else:
            break
    print(f'内存填充完成: {max_memory_mb}MB')


# 消耗cpu资源,计算斐波那契数列
def cpu_consume():
    num = random.randint(100000, 250000)
    n1, n2 = 0, 1
    count = 0
    while count < num:
        n3 = n1 + n2
        n1 = n2
        n2 = n3
        count += 1
    return 1


def res_consume():
    print(f'开始下载url : {download_url_path}')

    response = manager.request('GET', download_url_path, preload_content=False)
    last_timestamp = time.time()
    download_size = 0

    while True:
        chunk = response.read(max_speed_mbs * 1000 * 1000)

        if not chunk:
            break

        cpu_consume()

        shape_time = time.time() - last_timestamp

        if shape_time < 1:
            time.sleep(1 - shape_time)

        download_size += len(chunk)
        del chunk
        gc.collect()

        last_timestamp = time.time()

    response.release_conn()
    print(f'url下载完成 : {download_url_path}')


def run_process():
    old_pid = read_pid()
    if old_pid:
        os.system("kill -9 " + old_pid)
    save_pid()

    mem_consume()

    while True:
        try:
            res_consume()
        except:
            traceback.print_exc()
            time.sleep(10)
        else:
            time.sleep(3)


if __name__ == '__main__':
    run_process()
