import redis
from python_dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT')) 

class RedisConfig:
    def __init__(self, host: str = 'localhost', port: int = 6379, decode_responses: bool = True):
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self._connection = None

    def get_redis_connection(self):
        if self._connection is None:
            self._connection = redis.Redis(
                host=self.host,
                port=self.port,
                decode_responses=self.decode_responses
            )
        return self._connection