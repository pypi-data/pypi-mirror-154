import hashlib
from datetime import timedelta
from typing import List, Optional, Any

from diskcache import Cache

from gpd.models.dependent import Dependent
from gpd.models.dependent_key import DependentKey


class DependentCache:
    cache: Cache
    default_expiry: Optional[timedelta]

    def __init__(self, cache: Cache, default_expiry: timedelta = None):
        self.cache = cache
        self.default_expiry = default_expiry

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def set_dependents(self, key: DependentKey, dependents: List[Dependent]) -> None:
        digest = self.digest(key)
        if self.default_expiry:
            self.cache.set(
                digest, dependents, expire=self.default_expiry.total_seconds()
            )
        else:
            self.cache.set(digest, dependents)

    def get_dependents(self, key: DependentKey) -> List[Dependent]:
        digest = self.digest(key)
        return self.cache.get(digest, default=[])

    def is_exists(self, key: DependentKey):
        digest = self.digest(key)
        return digest in self.cache

    def construct_key(self, owner: str, project: str, max_page: int) -> DependentKey:
        return DependentKey(
            **{"owner": owner, "project": project, "max_page": max_page}
        )

    def digest(self, data: Any) -> str:
        return hashlib.sha512(str(data).encode()).hexdigest()

    def clear(self) -> None:
        self.cache.clear()

    def close(self) -> None:
        self.cache.close()
