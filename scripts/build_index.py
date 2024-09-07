import base64
import glob
import os

import fire
from byaldi import RAGMultiModalModel


def main(folder: str = "pdfs/", index_name: str = "application"):
    RAG = RAGMultiModalModel.from_pretrained("vidore/colpali-v1.2", verbose=1)

    RAG.index(
        input_path=folder,
        index_name=index_name,
        store_collection_with_index=True,
        overwrite=True,
    )


if __name__ == "__main__":
    fire.Fire(main)
