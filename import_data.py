# third party
import pandas as pd
import numpy as np
from langchain.document_loaders import UnstructuredODTLoader


if __name__ == "__main__":

    UnstructuredODTLoader = UnstructuredODTLoader(file_path="downloaded_docs")

    UnstructuredODTLoader.load()
    breakpoint()


