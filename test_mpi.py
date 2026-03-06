from pudimi_mpi import PyMpiManager

def main():
    manager = PyMpiManager()
    print(manager.get_info())

if __name__ == "__main__":
    main()