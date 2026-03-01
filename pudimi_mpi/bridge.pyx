from .bridge cimport MpiManager

cdef class PyMpiManager:
    cdef MpiManager* cpp_obj

    def __cinit__(self):
        self.cpp_obj = new MpiManager()

    def __dealloc__(self):
        del self.cpp_obj

    def get_info(self):
        rank = self.cpp_obj.get_rank()
        name = self.cpp_obj.get_processor_name().decode('utf-8')
        return f"Rank {rank} executando em {name}"