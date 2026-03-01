#include "../include/mpi_core.hpp"
#include <mpi.h>

namespace mpi_wrapper {
    MpiManager::MpiManager() {
        int initialized = 0;
        MPI_Initialized(&initialized);
        if (!initialized) {
            // Inicialização mais segura para o OpenMPI
            int argc = 0;
            char** argv = nullptr;
            MPI_Init(&argc, &argv);
        }
    }

    MpiManager::~MpiManager() {
        int finalized = 0;
        MPI_Finalized(&finalized);
        if (!finalized) {
            MPI_Finalize();
        }
    }

    int MpiManager::get_rank() {
        int rank = -1; // Inicializa com -1 para indicar erro caso falhe
        if (MPI_Comm_rank(MPI_COMM_WORLD, &rank) != MPI_SUCCESS) {
            return -1;
        }
        return rank;
    }

    std::string MpiManager::get_processor_name() {
        char name[MPI_MAX_PROCESSOR_NAME] = {0}; // Zera o array
        int len = 0; 
        
        if (MPI_Get_processor_name(name, &len) != MPI_SUCCESS) {
            return std::string("Erro_MPI");
        }
        
        // Trava de segurança: impede que tente alocar memória absurda
        if (len < 0 || len > MPI_MAX_PROCESSOR_NAME) {
            return std::string("Nome_Invalido");
        }
        
        return std::string(name, len);
    }
}