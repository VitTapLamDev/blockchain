import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

from backend.config import STARTING_BALANCE

class Wallet:
    def __init__(self) -> None:
        self.address = str(uuid.uuid64())[0:8]