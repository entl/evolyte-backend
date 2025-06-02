import redis
from typing import Iterator, Optional, Union


class RedisBaseRepository:
    def __init__(self, client: redis.Redis, namespace: str = ""):
        """
        :param client: an instance of redis.Redis
        :param namespace: prefix for all keys (no trailing colon needed)
        """
        self.client = client
        self.namespace = f"{namespace}:" if namespace else ""

    def _format_key(self, key: str) -> str:
        return f"{self.namespace}{key}"

    def create(
        self,
        key: str,
        value: Union[str, bytes],
        ex: Optional[int] = None
    ) -> bool:
        """
        Set the key to value only if it does not already exist (NX).
        :param ex: expiration in seconds
        :returns: True if key was set, False if it already existed
        """
        return self.client.set(self._format_key(key), value, ex=ex, nx=True)

    def read(self, key: str) -> Optional[bytes]:
        """
        Get the raw bytes stored at the key, or None if missing.
        """
        return self.client.get(self._format_key(key))

    def update(
        self,
        key: str,
        value: Union[str, bytes],
        ex: Optional[int] = None
    ) -> bool:
        """
        Unconditionally set the key to value (overwrite).
        :returns: True if successful
        """
        return self.client.set(self._format_key(key), value, ex=ex)

    def delete(self, key: str) -> int:
        """
        Delete the given key.
        :returns: number of keys deleted (0 or 1)
        """
        return self.client.delete(self._format_key(key))

    def exists(self, key: str) -> bool:
        """
        Check if the key exists.
        """
        return self.client.exists(self._format_key(key)) == 1

    def scan(
        self,
        pattern: str = "*",
        count: int = 100
    ) -> Iterator[str]:
        """
        Iterate all keys matching the pattern within this namespace.
        Yields the un-prefixed key names.
        """
        cursor: Union[int, bytes] = 0
        full_pattern = f"{self.namespace}{pattern}"
        while True:
            cursor, keys = self.client.scan(cursor=cursor, match=full_pattern, count=count)
            for raw in keys:
                key = raw.decode() if isinstance(raw, bytes) else raw
                # strip namespace prefix
                yield key[len(self.namespace) :]
            if cursor == 0:
                break

    def incr(
        self,
        key: str,
        amount: int = 1
    ) -> int:
        """
        Increment the integer value stored at key by amount.
        :returns: new value after increment
        """
        return self.client.incr(self._format_key(key), amount)
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Set the expiration time for a key.
        :param seconds: expiration time in seconds
        :returns: True if the timeout was set, False if the key does not exist
        """
        return self.client.expire(self._format_key(key), seconds)
    
    def ttl(self, key: str) -> Optional[int]:
        """
        Get the time to live for a key.
        :returns: time to live in seconds, or None if the key does not exist or has no expiration
        """
        return self.client.ttl(self._format_key(key))
