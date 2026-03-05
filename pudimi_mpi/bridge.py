import numpy as np
import numpy.typing as npt

class PyMpiManager:
    def __init__(self) -> None: ...
    def get_rank(self) -> int:
        """
        Retorna o rank do processo atual no comunicador global.
        """
        ...

    def get_info(self) -> str:
        """
        Retorna uma string formatada com o rank e o nome do host (processador).
        """
        ...

    def calculate_mean(self, data: npt.NDArray[np.float64]) -> float:
        """
        Recebe um array NumPy (float64) e retorna a média global de todos os
        processos combinados usando MPI Allreduce.

        O array deve ser preferencialmente contíguo na memória. Se o array for
        vazio (shape[0] == 0), retorna 0.0.
        """
        ...
