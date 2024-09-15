import glob
import logging
from enum import Enum
from pathlib import Path

from unstructured.documents.elements import Text
from unstructured.partition.auto import partition


class FileType(Enum):
    BMP = "bmp"
    CSV = "csv"
    DOC = "doc"
    DOCX = "docx"
    EML = "eml"
    EPUB = "epub"
    HEIC = "heic"
    HTML = "html"
    JPEG = "jpeg"
    PNG = "png"
    MD = "md"
    MSG = "msg"
    ODT = "odt"
    ORG = "org"
    P7S = "p7s"
    PDF = "pdf"
    PPT = "ppt"
    PPTX = "pptx"
    RST = "rst"
    RTF = "rtf"
    TIFF = "tiff"
    TXT = "txt"
    TSV = "tsv"
    XLS = "xls"
    XLSX = "xlsx"
    XML = "xml"


def valid_file_type(file_path: str) -> bool:
    suffix_sans_dot = Path(file_path).suffix[1:]
    return suffix_sans_dot in FileType._value2member_map_


def extract_page_texts(texts: list[Text]) -> list[str]:
    """
    Extracts and organizes text content by page from a list of text objects.

    Args:
        texts (list): A list of text objects, each containing text and metadata.

    Returns:
        list[str]: A list where each element is the concatenated text of a single page.
    """
    page_texts = []
    current_page_text = ""
    current_page_number = 1
    for text_obj in texts:
        # Start of a new page
        if text_obj.metadata.page_number != current_page_number:
            page_texts.append(current_page_text)
            current_page_text = ""
            current_page_number = text_obj.metadata.page_number

        # Append the text of the current object to the accumulator
        current_page_text += "\n" + text_obj.text

    # Need one final append for the last page
    if current_page_text:
        page_texts.append(current_page_text)
    return page_texts


def extract_texts_from_folder(folder_path: str, cache: bool = True) -> None:
    """
    Extracts text content from all files in a given folder that match supported file types.

    Args:
        folder_path (str): The path to the folder containing files to extract text from.
        cache (bool): Whether to use cached text files if they exist. Defaults to True.

    Returns:
        None
    """
    logging.info(f"Starting text extraction from folder: {folder_path}")
    files = glob.glob(folder_path + "**/*", recursive=True)
    filtered_files: list[str] = [file for file in files if valid_file_type(file)]
    logging.info(f"Found {len(filtered_files)} valid files to process.")
    for file in filtered_files:
        file_path = Path(file)
        input_folder = file_path.parent / "input"
        input_folder.mkdir(exist_ok=True)  # Create the input folder if it doesn't exist
        existing_text_files = list(input_folder.glob(f"{file_path.stem}*.txt"))

        if cache and existing_text_files:
            logging.info(f"Using cached text files for: {file}")
            continue

        logging.info(f"Processing file: {file}")
        texts: list[Text] = partition(file, strategy="hi_res")
        page_texts: list[str] = extract_page_texts(texts)

        for page_number, page_text in enumerate(page_texts):
            txt_filepath = input_folder / f"{file_path.stem}.{page_number}.txt"
            with open(txt_filepath, "w") as f:
                f.write(page_text)
            logging.info(f"Text extracted and saved to: {txt_filepath}")

    logging.info("Text extraction completed.")
