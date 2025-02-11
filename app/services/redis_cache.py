# import redis
# import json
# from typing import Optional

# class RedisCache:
#     def __init__(self, host='localhost', port=6379, db=0):
#         self.client = redis.StrictRedis(host=host, port=port, db=db)

#     def set_cache(self, key: str, value: dict, ex: Optional[int] = None):
#         # Store the value as a JSON string
#         self.client.set(key, json.dumps(value), ex=ex)

#     def get_cache(self, key: str) -> Optional[dict]:
#         cached_value = self.client.get(key)
#         if cached_value:
#             return json.loads(cached_value)
#         return None

#     def delete_cache(self, key: str):
#         self.client.delete(key)

#     def exists(self, key: str) -> bool:
#         return self.client.exists(key)
