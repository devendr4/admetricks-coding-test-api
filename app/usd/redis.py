import pickle

import pandas as pd
import pyarrow as pa
import redis

from app.usd.config import get_settings


class CacheService:
    def __init__(self, url: str):
        self.redis = redis.Redis(host=url, port=6379, db=0)

    def set(self, key: str, df: pd.DataFrame, expire=300):
        return self.redis.set(key, pickle.dumps(df), expire)

    def get(self, key: str):
        buffer = self.redis.get(key)
        if not buffer:
            return None
        print("cont")
        df = pickle.loads(buffer)
        return df


redis_service = CacheService(get_settings().redis_url)
