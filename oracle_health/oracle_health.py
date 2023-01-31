import gc
import os
import time
import codecs
import random

import urllib3
import traceback
from io import BytesIO

max_speed_mbs = 1  # 最大下载速度 mb/s
max_memory_mb = 1024 * 3  # 内存占用上限
large_file_list_path = 'large_file_list.txt'
large_file_list_url_path = 'https://raw.githubusercontent.com/akiiya/Shell/master/oracle_health/large_file_list.txt'

mem_file = BytesIO()

manager = urllib3.PoolManager()


def read_url_list():
    url_list = []
    if not os.path.exists(large_file_list_path):
        response = manager.request('GET', large_file_list_url_path)
        response_text = response.data
        response.release_conn()
        line_list = response_text.decode('utf-8').split('\n')
    else:
        with codecs.open(large_file_list_path, 'rb') as f:
            line_list = f.readlines()

    for line in line_list:
        line = str(line)
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if not line.startswith('http'):
            continue
        url_list.append(line)

    return url_list


# 消耗内存资源
def mem_consume():
    while True:
        # 消耗内存
        if mem_file.tell() < max_memory_mb * 1024 * 1024:
            mem_file.write(b'0' * 1024)
        else:
            break


# 消耗cpu资源,计算斐波那契数列
def cpu_consume(s_m):
    if s_m == 's':
        num = 2000000
    else:
        num = 250000
    n1, n2 = 0, 1
    count = 0
    while count < num:
        n3 = n1 + n2
        n1 = n2
        n2 = n3
        count += 1
    return 1


def res_consume(url_list):
    url = url_list[random.randint(0, len(url_list))]

    response = manager.urlopen('GET', url, preload_content=False)
    download_size = 0
    last_timestamp = time.time()

    while True:
        chunk = response.read(max_speed_mbs * 1000 * 1000)

        if not chunk:
            break

        while True:  # 多余的时间去消耗cpu
            cpu_consume('m')
            shape_time = time.time() - last_timestamp
            if shape_time < 1:
                continue
            else:
                break

        # 降低下载速度
        # if shape_time < 1:
        #    time.sleep(1 - shape_time)

        download_size += len(chunk)
        del chunk
        gc.collect()
        last_timestamp = time.time()
        print('[{t}] - 已完成: {x}mb'.format(
            t=last_timestamp,
            x=download_size / 1000 / 1000
        ))

    response.release_conn()


def run_process():
    # mem_consume()
    url_list = read_url_list()
    while True:
        try:
            res_consume(url_list)
        except:
            traceback.print_exc()
            time.sleep(30)


run_process()
