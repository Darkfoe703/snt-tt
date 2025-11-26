import time
import functools
from typing import Any, Callable, Dict, Optional


class InMemoryCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryCache, cls).__new__(cls)
            cls._instance.store = {}
        return cls._instance

    def get(self, key: str) -> Optional[Any]:
        if key in self.store:
            data, expiry = self.store[key]
            if time.time() < expiry:
                return data
            else:
                del self.store[key]
        return None

    def set(self, key: str, value: Any, ttl: int):
        self.store[key] = (value, time.time() + ttl)

    def clear(self):
        self.store = {}


def cache_response(ttl: int = 60):
    """
    Decorador para cachear respuestas de endpoints.
    Usa la ruta y los argumentos como clave.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Crear una clave única basada en la función y los argumentos
            # Nota: Esto es una implementación simple. Para producción, considerar algo más robusto.
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            cache = InMemoryCache()
            cached_result = cache.get(cache_key)

            if cached_result is not None:
                return cached_result

            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator
