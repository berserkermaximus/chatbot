from redis import Redis
from rq import Queue

redis_connection = Redis()
queue = Queue(name="gpu_queue", connection=redis_connection)