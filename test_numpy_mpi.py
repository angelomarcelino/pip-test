from pudimi_mpi.bridge import PyMpiManager
import numpy as np


def main():
    manager = PyMpiManager()
    rank = manager.get_rank()

    # Cada rank cria um array diferente: Rank 0: [0,0], Rank 1: [1,1], etc.
    local_data = np.array([rank, rank], dtype=np.float64)

    mean = manager.calculate_mean(local_data)

    if rank == 0:
        print("--- Validação NumPy + MPI ---")
        print(f"Média Global calculada: {mean}")
        # Para 2 processos (Rank 0 e 1), a média de [0,0,1,1] deve ser 0.5


if __name__ == "__main__":
    main()
