from __future__ import annotations

from typing import Optional


class PyMpiManager:
    """
    Python interface to the C++ MPI manager backend.
    """

    def __init__(self) -> None: ...
    
    def get_info(self) -> Optional[str]: ...