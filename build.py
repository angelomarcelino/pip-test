import os
import subprocess
import shlex
import sys
from typing import Any
from setuptools import Extension, setup
from Cython.Build import cythonize

REQUIRED_LIBS = ["mpi4py", "numpy"]


def get_mpi_config():
    """Extrai as flags e diretórios do MPI via caminho absoluto do OpenMPI 5.0.8."""
    # 1. Tenta usar o caminho absoluto da instalação manual
    # Se não encontrar, tenta o que estiver no PATH (útil para portabilidade)
    mpi_home = os.environ.get("MPI_HOME", "/opt/openmpi-5.0.8")
    mpicxx_path = (
        os.path.join(mpi_home, "bin", "mpicxx")
        if os.path.exists(mpi_home)
        else "mpicxx"
    )

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
        print(f"--> MPI Detectado via: {mpicxx_path}")
        return shlex.split(c_flags), shlex.split(l_flags), lib_dirs
    except Exception as e:
        print(f"Aviso: Não foi possível configurar o MPI via {mpicxx_path}: {e}")
        return [], [], []


def add_lib_includes(include_dirs, libs):
    """Adiciona diretórios de include de bibliotecas Python instaladas (ex: numpy, mpi4py)."""
    for lib_name in libs:
        try:
            # Importação dinâmica para evitar quebra no início do script
            lib = __import__(lib_name)
            if hasattr(lib, "get_include"):
                path = lib.get_include()
                include_dirs.append(path)
                print(f"--> Headers de {lib_name} incluídos: {path}")
        except ImportError:
            print(f"--> Aviso: {lib_name} não encontrado para extração de headers.")


def build(setup_kwargs):
    # 1. Obter configuração do MPI
    mpi_compile_args, mpi_link_args, mpi_lib_dirs = get_mpi_config()

    # 2. Configurar o RPATH
    # Garante que o .so encontre as libs do OpenMPI 5.0.8 em runtime, ignorando o /usr/lib
    rpath_flags = [f"-Wl,-rpath,{d}" for d in mpi_lib_dirs]
    # Desativar 'new-dtags' força RPATH em vez de RUNPATH, facilitando herança de libs
    rpath_flags.append("-Wl,--disable-new-dtags")

    # 3. Gerenciar diretórios de inclusão
    include_dirs = ["cpp_lib/include"]
    # Adicionamos os headers das dependências Python e do OpenMPI manual
    add_lib_includes(include_dirs, REQUIRED_LIBS)
    include_dirs.append("/opt/openmpi-5.0.8/include")

    # 4. Configurar a extensão Cython
    extensions = [
        Extension(
            "pudimi_mpi.bridge",
            sources=["pudimi_mpi/bridge.pyx", "cpp_lib/src/mpi_core.cpp"],
            include_dirs=include_dirs,
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
    # Proteção para o Poetry 2.0: só executa setup() se houver argumentos (ex: build_ext)
    # Isso evita o erro 'no commands supplied' durante o poetry install simples
    if len(sys.argv) > 1:
        setup_kwargs: dict[str, Any] = {"packages": ["pudimi_mpi"]}
        build(setup_kwargs)
        setup(**setup_kwargs)
