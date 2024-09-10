from unstructured.partition.pdf import partition_pdf
from unstructured.partition.image import partition_image

import glob
import os
from rich import print as Print

def extract_text_from_pdfs(folder: str) -> list[dict]:
    pdfs = glob.glob(os.path.join(folder, "*.pdf"))
    pngs = glob.glob(os.path.join(folder, "*.png"))


    result = []
    for i, file in enumerate(sorted(pdfs + pngs)):
        if file.lower().endswith('.pdf'):
            elements = partition_pdf(file)
        else:
            elements = partition_image(file)

        text = " ".join([elem.text for elem in elements])
        result.append({
            "text": text,
            "doc_id": i,
            "file_path": file
        })

    print(f"{len(result)} documents processed")
    # Print(result)
    return result

if __name__ == "__main__":
    import fire
    fire.Fire(extract_text_from_pdfs)
