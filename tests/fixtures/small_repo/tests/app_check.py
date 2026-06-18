from src.app import add


def check_add() -> None:
    assert add(2, 3) == 5
