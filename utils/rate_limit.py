class FixedWindowRateLimiter:
    def __inti__(self, redis_client, max_requests, window_size):
        self.redis_client = redis_client
        self.max_requests = max_requests
        self.window_size = window_size

    def is_allowed(self, key):
        redis_key = f"rate_limit:{key}"
        current_window = int(time.time() // self.window_size) * self.window_size

        with self.redis_client.pipeline() as redis_pipe:s
            try:
                redis_pipe.get(redis_key + ":window")
                redis_pipe.get(redis_key + ":count")

                window, count = redis_pipe.execute()

                if window is None or int(window) != current_window:
                    redis_pipe.set(redis_key + ":window", current_window)
                    redis_pipe.set(redis_key + ":count", 1)
                    redis_pipe.expire(redis_key + ":window", self.window_size)
                    redis_pipe.expire(redis_key + ":count", self.max_requests)
                    redis_pipe.execute()

                    return True

                count = int(count)
                if count < self.max_requests:
                    redis_pipe.incr(redis_key + ":count")
                    redis_pipe.expire(redis_key + ":count", self.max_requests)
                    redis_pipe.execute()

                    return True
                else:
                    return False
            except redis.RedisError as e:
                print(f"Redis error: {e}")
                return False



    