from typing import List, Union, Optional
import platform
from subprocess import Popen, PIPE


def call(cmd: Union[str, List[str]], timeout: Optional[Union[int, float]] = None):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    if timeout:
        out, err = p.communicate(timeout=timeout)
    else:
        out, err = p.communicate()
    return out.decode("utf-8").strip(), err.decode("utf-8").strip()


def which(cmd: str):
    """Return the full path of a program if it exists on system.

    System can be a windows or unix like sytem

    Args:
        cmd: Name of the program

    """
    sys_name = platform.system().lower()
    if sys_name == "linux":
        cmd = "which"
    elif sys_name == "windows":
        cmd = "where"
    else:
        raise ValueError(f"Unknown system {sys_name}")
    return call(cmd)[0]
