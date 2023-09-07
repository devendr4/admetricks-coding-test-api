import pandas as pd
import pyarrow as pa
import redis

from app.usd.config import get_settings


class CacheService:
    def __init__(self, url: str):
        self.redis = redis.Redis(host=url, port=6379, db=0)

    def set(self, key: str, df: pd.DataFrame, expire=300):
        table = pa.Table.from_pandas(df)
        print(table)
        buffer = pa.serialize(table).to_buffer()
        print(buffer)
        return self.redis.set(key, buffer, expire)

    def get(self, key: str):
        buffer = self.redis.get(key)
        if not buffer:
            return None
        print("cont")
        table = pa.deserialize(buffer)
        print(table)
        return table


redis_service = CacheService(get_settings().redis_url)
