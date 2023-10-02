import os
from .classes import StaticClass


class IO(StaticClass):
    def save_file(file: bytes, path: str) -> None:
        head, _ = os.path.split(path)
        os.makedirs(head, exist_ok=True)
        with open(path, "wb") as f:
            f.write(file)
    
    def load_file(path: str):
        with open(path, 'r') as f:
            return f.read()