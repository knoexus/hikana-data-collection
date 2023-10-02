class StaticClass:
    def __new__(cls) -> None:
        raise TypeError('This is a static class and cannot be instantiated.')