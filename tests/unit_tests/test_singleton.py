from src.singleton import Singleton


class TestSingleton:
    class OnlySingleClass(metaclass=Singleton):
        y: int

        def __init__(self, y: int) -> None:
            self.y = y

    def test_singleton(self) -> None:
        cls = self.OnlySingleClass(2)
        assert cls.y == 2
        cls = self.OnlySingleClass(3)
        assert cls.y == 2
