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
    };
}

#endif