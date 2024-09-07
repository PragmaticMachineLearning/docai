from unstructured.partition.pdf import partition_pdf
import glob
import fire
from rich import print as Print

def extract_text_from_pdfs(folder: str) -> list[list[str]]:
    pdfs = glob.glob(f"{folder}/*.pdf")
    print(f"Found {len(pdfs)} PDFs")
    text = []
    for pdf in pdfs:
        print(f"processing pdf: {pdf}")
        text.append(partition_pdf(pdf))

    result = [[item.text for item in list_items] for list_items in text]
    print(f"{len(result)} PDFs processed")
    return result
if __name__ == "__main__":
    fire.Fire(extract_text_from_pdfs)
