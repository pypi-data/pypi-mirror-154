import datetime
import os
import subprocess

import coolname

from deque.rest_connect import RestConnect
from deque.deque_environment import AGENT_API_SERVICE_URL
from deque.redis_services import RedisServices
import pickle
import multiprocessing
from deque.parsing_service import ParsingService
from deque.datatypes import Image, Audio, Histogram, BoundingBox2D


def decode_datetime(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj


class Run:
    _step = 1

    def __init__(self):
        self.user_name = None

        self._workload_type = None
        self._submission_id = None

        self.project_id = None

        self.params = dict()
        self._history = dict()

        self._rest = RestConnect()
        self._redis = RedisServices.get_redis_connection()

    def init(self, user_name=None, project_name=None):
        self.user_name = user_name

        if project_name is None:
            self.project_id = coolname.generate_slug(2)
        else:
            self.project_id = project_name

        self._submission_id = os.getenv("submission_id")
        self._workload_type = os.getenv("workload_type")
        self.workload_id = os.getenv("workload_id")
        if self._submission_id is None or self._workload_type is None:
            self._submission_id = "test_submission"
            self._workload_type = "notebook"
            # raise Exception("Experiment Tracking is only supported with Deque AI tools. Get yours at https://deque.app")

        #p2 = multiprocessing.Process(target=self.start_parser)
        #p2.start()

        self._redis.sadd("submission_ids:", self._submission_id)
        while True:
            submission_ids = self._redis.smembers("submission_ids:")
            print("submission ids")
            print(submission_ids)

            for s in submission_ids:
                s = str(s.decode("utf-8"))
                steps = self._redis.smembers("submission_id:steps:"+s)
                print("steps")
                print(steps)

                for step in steps:
                    step = str(step.decode("utf-8"))
                    #print("Step")
                    #print(step)
                    key = "submission_id:step:data:"+s+step
                    pickled_data = self._redis.get(key)
                    #print("pickled data")
                    #print(pickle.loads(pickled_data))



                    if pickled_data is None:
                        continue
                    print("pickled data")
                    print(pickle.loads(pickled_data))
                    #self._rest.post_binary(url=self.tracking_endpoint,data=pickled_data)
                    self._redis.delete(key)
                    self._redis.srem("submission_id:steps:"+s,step)


    def start_parser(self):
        parser = ParsingService()
        parser.receive()

    def send_data_to_redis(self, step, data):

        key = "submission_id:step:data:" + self._submission_id + str(step)

        self._redis.sadd("submission_id:steps:" + self._submission_id, str(step))

        data_pickled = pickle.dumps(data)

        self._redis.set(key, data_pickled)

    def log(self, data, step=None, commit=True):
        #self._validate_data(data=data)
        data.update(
            {"user_name": self.user_name, "submission_id": self._submission_id, "workload_type": self._workload_type,
             "workload_id": self.workload_id,
             "project_id": self.project_id, "deque_log_time": datetime.datetime.now(), "step": Run._step})

        self.send_data_to_redis(step=self._step, data=data)
        if commit:
            Run._step += 1

    def _validate_data(self, data):
        for key, value in data.items():
            if type(value) is dict:
                self._validate_data(value)
            else:
                #print(type(value))
                if type(value) in [Audio, BoundingBox2D, Histogram,
                                   Image] or value.__class__.__module__ == '__builtin__':
                    pass
                else:
                    raise ValueError(
                        "Invalid type in dictionary. Allowed values include builtin types and Deque data types "+ str(type(value)) + " "+ str(value.__class__.__module__ ))

    def send_upstream(self):
        self._rest.post(url=AGENT_API_SERVICE_URL + "/fex/python/track/", json=self._history)
        self._history = dict()


if __name__ == "__main__":
    deque = Run()
    #deque.init(user_name="riju@deque.app", project_name="awesome-dude")
    #for i in range(100):
        #deque.log(data={"train": {"accuracy": i, "loss": i - 100}, "image": deque.im})

    # deque.log(data={"image":deque.im})
