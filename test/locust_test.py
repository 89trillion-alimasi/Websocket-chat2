import os
import queue
import random
import time

import websocket
from locust import events, TaskSet, task, User, constant_pacing

import connect_pb2


class WebSocketClient(object):

    def __init__(self, host):
        self.host = host
        self.ws = websocket.WebSocket()
        self.name = "wsTest"

    def record_result(self, response_time, response_length=0, exception_msg=None):
        self.name = "wsTest"
        if exception_msg:
            events.request_failure.fire(request_type="ws", name=self.name, response_time=response_time,
                                        exception=exception_msg,
                                        response_length=response_length)
        else:
            events.request_success.fire(request_type="ws", name=self.name, response_time=response_time,
                                        response_length=response_length)

    def connect(self, burl, request_name='ws'):
        self.name = request_name
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url=burl)
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time, exception_msg=e)
        except BrokenPipeError as e:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time, exception_msg=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time)
        return self.conn

    def recv(self):
        global rec
        start_time = time.time()
        try:
            rec = self.ws.recv()
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time, exception_msg=e)
        except BrokenPipeError as e:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time, exception_msg=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time)
        return rec

    def send(self, msg):
        start_time = time.time()
        try:
            self.ws.send(msg)
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time, exception_msg=e)
        except BrokenPipeError as e:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time, exception_msg=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            self.record_result(response_time=total_time)

    def rec_msg(self, expect_str=None, time_out=500, forever=False, time_out_per=60, run_user=None):
        pass


def generate_message():
    return "test_msg" + ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 9))


def get_message_talk():
    conn=connect_pb2.Communication()
    conn.Type="1"
    conn.Msg="hhhhhh"
    return conn.SerializeToString()


# def get_message_userlist():
#     conn=connect_pb2.Communication()
#     conn.Userlist="userlist"
#     conn.Type="1"
#     return conn.SerializeToString()


class SupperSC(TaskSet):

    def on_start(self):
        data = self.user.queueData.get()  # 获取队列里的数据
        self.username = data.get('username')
        # 建立ws连接
        host = self.client.host
        self.url = 'ws://{}/ws?username={}'.format(host, self.username)
        self.client.connect(self.url, self.username)

    @task(1)
    def test_send_talk(self):
        while True:
            msg = get_message_talk()
            self.client.send(msg)
            time.sleep(1)

    # @task(1)
    # def test_send_user_list(self):
    #     while True:
    #         self.client.send(get_message_userlist())
    #         time.sleep(1)

    @task(1)
    def test_recv(self):
        while True:
            self.client.recv()
            time.sleep(1)


class WSUser(User):
    host = '127.0.0.1:8080'  # 待测主机
    wait_time = constant_pacing(1)  # 单个用户执行间隔时间
    tasks = [SupperSC]

    queueData = queue.Queue()  # 队列实例化
    for count in range(3000):  # 循环数据生成
        data = {
            "username": f'tst_user_{count}'
        }
        queueData.put_nowait(data)

    def __init__(self, *args, **kwargs):
        super(WSUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)


if __name__ == "__main__":
    os.system("locust -f locust_test.py")
