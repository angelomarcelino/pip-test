cmake_minimum_required(VERSION 3.18)

project(pudimi_mpi LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# -------------------------
# Python
# -------------------------

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# -------------------------
# NumPy
# -------------------------

execute_process(
    COMMAND ${Python_EXECUTABLE} -c "import numpy; print(numpy.get_include())"
    OUTPUT_VARIABLE NUMPY_INCLUDE
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# -------------------------
# MPI
# -------------------------

find_package(MPI REQUIRED)

# -------------------------
# Cython → C++
# -------------------------

execute_process(
    COMMAND ${Python_EXECUTABLE} -m cython
        ${CMAKE_CURRENT_SOURCE_DIR}/pudimi_mpi/bridge.pyx
        --cplus
        -3
        -o ${CMAKE_CURRENT_BINARY_DIR}/bridge.cpp
)

# -------------------------
# Extension module
# -------------------------

add_library(pudimi_mpi MODULE
    ${CMAKE_CURRENT_BINARY_DIR}/bridge.cpp
    cpp_lib/src/mpi_core.cpp
)

target_include_directories(pudimi_mpi PRIVATE
    ${NUMPY_INCLUDE}
    cpp_lib/include
    ${MPI_CXX_INCLUDE_PATH}
)

target_link_libraries(pudimi_mpi PRIVATE
    Python::Module
    MPI::MPI_CXX
)

set_target_properties(pudimi_mpi PROPERTIES
    PREFIX ""
    OUTPUT_NAME "bridge"
)

# -------------------------
# Install inside package
# -------------------------

install(
    TARGETS pudimi_mpi
    LIBRARY DESTINATION pudimi_mpi
)