#ifndef MPI_CORE_HPP
#define MPI_CORE_HPP

#include <string>

namespace mpi_wrapper {
    class MpiManager {
    public:
        MpiManager();
        ~MpiManager();
        std::string get_processor_name();
        int get_rank();
        // Recebe dados locais e retorna a média de todos os ranks combinados
        double global_mean(const double* data, int size);
    };
}

#endif