from libcpp.string cimport string

cdef extern from "mpi_core.hpp" namespace "mpi_wrapper":
    cdef cppclass MpiManager:
        MpiManager() except +
        string get_processor_name()
        int get_rank()
        double global_mean(const double* data, int size)