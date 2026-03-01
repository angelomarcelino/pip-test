import os
import subprocess
import shlex
from typing import Any
from setuptools import Extension, setup
from Cython.Build import cythonize


def get_mpi_config():
    """Extrai as flags e diretórios do MPI via caminho absoluto do OpenMPI."""
    # Forçamos o uso do binário específico da instalação manual
    mpicxx_path = "/opt/openmpi-5.0.8/bin/mpicxx"

    try:
        c_flags = subprocess.check_output(
            [mpicxx_path, "--showme:compile"], encoding="utf-8"
        ).strip()
        l_flags = subprocess.check_output(
            [mpicxx_path, "--showme:link"], encoding="utf-8"
        ).strip()
        lib_dirs = (
            subprocess.check_output([mpicxx_path, "--showme:libdirs"], encoding="utf-8")
            .strip()
            .split()
        )

        return shlex.split(c_flags), shlex.split(l_flags), lib_dirs
    except Exception as e:
        print(f"Erro crítico: {mpicxx_path} não encontrado: {e}")
        return [], [], []


def build(setup_kwargs):
    # 1. Obter configuração do MPI
    mpi_compile_args, mpi_link_args, mpi_lib_dirs = get_mpi_config()

    # 2. Configurar o RPATH
    # Isso garante que o .so saiba onde encontrar as libs do OpenMPI em runtime
    rpath_flags = []
    for d in mpi_lib_dirs:
        rpath_flags.append(f"-Wl,-rpath,{d}")

    # Importante: desativar 'new-dtags' força o uso de RPATH em vez de RUNPATH
    # O RPATH é herdado por dependências, o que evita o erro de 'libopen-pal.so not found'
    rpath_flags.append("-Wl,--disable-new-dtags")

    extensions = [
        Extension(
            "pudimi_mpi.bridge",
            sources=["pudimi_mpi/bridge.pyx", "cpp_lib/src/mpi_core.cpp"],
            include_dirs=["cpp_lib/include"],
            language="c++",
            extra_compile_args=["-O3", "-std=c++11"] + mpi_compile_args,
            extra_link_args=mpi_link_args + rpath_flags,
        )
    ]

    setup_kwargs.update(
        {
            "ext_modules": cythonize(extensions, language_level="3", annotate=True),
            "zip_safe": False,
        }
    )


if __name__ == "__main__":
    setup_kwargs: dict[str, Any] = {"packages": ["pudimi_mpi"]}
    build(setup_kwargs)
    setup(**setup_kwargs)
