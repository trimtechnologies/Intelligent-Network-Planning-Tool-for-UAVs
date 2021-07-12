import os
import zipfile


def unzip(filename: str, extract_to: str) -> None:
    """
    This method run unzip a file to specified path
    :param filename:    Path/filename of zip file
    :param extract_to:  Path with name of output folder
    :return: None
    """

    this_folder = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(this_folder, filename)

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(extract_to)
