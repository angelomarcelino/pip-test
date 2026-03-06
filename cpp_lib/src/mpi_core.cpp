#include "../include/mpi_core.hpp"

#include <mpi.h>

#include <numeric>

namespace mpi_wrapper {

MpiManager::MpiManager() {
	int initialized = 0;
	MPI_Initialized(&initialized);

	if (!initialized) {
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
	int rank = -1;

	if (MPI_Comm_rank(MPI_COMM_WORLD, &rank) != MPI_SUCCESS) {
		return -1;
	}

	return rank;
}

std::string MpiManager::get_processor_name() {
	char name[MPI_MAX_PROCESSOR_NAME];
	int len = 0;

	if (MPI_Get_processor_name(name, &len) != MPI_SUCCESS) {
		return "MPI_ERROR";
	}

	return std::string(name, len);
}

double MpiManager::global_mean(const double* data, int size) {
	double local_sum = std::accumulate(data, data + size, 0.0);

	double global_sum = 0.0;
	int global_count = 0;

	MPI_Allreduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
	MPI_Allreduce(&size, &global_count, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

	if (global_count == 0)
		return 0.0;

	return global_sum / global_count;
}

}  // namespace mpi_wrapper