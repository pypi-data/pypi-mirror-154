import pickle
import os


def get_data(file_name):
    print(os.path.abspath(__file__))

    data_path = os.path.abspath(__file__).replace("__init__.py", file_name)
    with open(data_path, "rb") as f:
        return pickle.load(f)
