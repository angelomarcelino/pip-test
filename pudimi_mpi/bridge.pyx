import numpy as np
cimport numpy as cnp

cnp.import_array()

from .bridge cimport MpiManager


cdef class PyMpiManager:
    cdef MpiManager* cpp_obj

    def __cinit__(self):
        self.cpp_obj = new MpiManager()

    def __dealloc__(self):
        del self.cpp_obj

    def get_rank(self):
        return self.cpp_obj.get_rank()

    def get_info(self):
        rank = self.cpp_obj.get_rank()
        name = self.cpp_obj.get_processor_name().decode("utf-8")
        return f"Rank {rank} executando em {name}"

    def calculate_mean(self, double[:] data):
        if data.shape[0] == 0:
            return 0.0
        return self.cpp_obj.global_mean(&data[0], data.shape[0])