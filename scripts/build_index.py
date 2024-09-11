from enum import Enum
from typing import Literal

import fire

Strategy = Literal["byaldi", "graphrag"]


def main(
    folder: str = "pdfs/",
    index_name: str = "application",
    overwrite: bool = False,
    strategy: Strategy = "byaldi",
    resume: bool = False,
):
    if strategy == "byaldi":
        from byaldi import RAGMultiModalModel

        RAG = RAGMultiModalModel.from_pretrained("vidore/colpali-v1.2", verbose=1)

        RAG.index(
            input_path=folder,
            index_name=index_name,
            store_collection_with_index=True,
            overwrite=overwrite,
        )
    elif strategy == "graphrag":
        from graphrag.index.cli import index_cli

        index_cli(
            root_dir=folder,
            verbose=True,
            resume=resume,
            update_index_id=False,
            memprofile=False,
            nocache=False,
            reporter="rich",
            config_filepath=None,
            emit="csv",
            dryrun=False,
            init=True,
            skip_validations=False,
        )
    else:
        raise ValueError(f"Invalid strategy: {strategy}")


if __name__ == "__main__":
    fire.Fire(main)
