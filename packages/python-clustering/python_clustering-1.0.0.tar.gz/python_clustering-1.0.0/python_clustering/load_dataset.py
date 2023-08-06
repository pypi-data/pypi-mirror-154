from scipy.io import arff
import pandas as pd

def read_aiff(filename: str) -> pd.DataFrame:
    data = arff.loadarff(filename)
    return pd.DataFrame(data[0])


def load_dataset(dataset_name: str, load_description = False):
    #check if dataset is present
    if load_description:
        return read_aiff(dataset_name), None
    return read_aiff(dataset_name)