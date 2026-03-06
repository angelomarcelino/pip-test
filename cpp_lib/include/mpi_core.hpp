#ifndef MPI_CORE_HPP
#define MPI_CORE_HPP

#include <string>

namespace mpi_wrapper {

class MpiManager {
   public:
	MpiManager();
	~MpiManager();

	int get_rank();
	std::string get_processor_name();

	double global_mean(const double* data, int size);
};

}  // namespace mpi_wrapper

#endif