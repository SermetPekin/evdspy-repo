import json
from abc import ABC


# ....................................................................... Serialize
class Serialize(ABC):
    """To check whether two Config Requests are perfect substitutes """

    def serialize(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    @property
    def hash(self) -> str:
        import hashlib
        return str(int(hashlib.sha256(self.serialize().encode('utf-8')).hexdigest(), 16) % 10 ** 8)

    def __eq__(self, other):
        return self.hash == other.hash

