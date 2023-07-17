from typing import Union, List, Optional, Any, Dict


def foo(x: int) -> int:
    return x + 5


def bar(x: List[str]) -> Optional[Dict[str, int]]:
    """

    :param x: ["bar1", "bar2", "bar3"]
    :return: {"a": 1, "b": 2, } or None
    """
    return {"a": 1}


foo(5)
foo("5")

bar(x=["a", "b"])
bar(5)
