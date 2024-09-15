import glob
import logging
from enum import Enum
from pathlib import Path

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


def extract_texts_from_folder(folder_path: str) -> None:
    """
    Extracts text content from all files in a given folder that match supported file types.

    Args:
        folder_path (str): The path to the folder containing files to extract text from.

    Returns:
        dict[str, str]: A dictionary where keys are file paths and values are the extracted text content.
    """
    logging.info(f"Starting text extraction from folder: {folder_path}")
    files = glob.glob(folder_path + "**/*", recursive=True)
    filtered_files: list[str] = [file for file in files if valid_file_type(file)]
    logging.info(f"Found {len(filtered_files)} valid files to process.")
    for file in filtered_files:
        logging.info(f"Processing file: {file}")
        texts = partition(file)
        for i, text_obj in enumerate(texts):
            txt_filepath = Path(file).with_suffix(f".{i}.txt")
            with open(txt_filepath, "w") as f:
                f.write(text_obj.text)
            logging.info(f"Text extracted and saved to: {txt_filepath}")
    logging.info("Text extraction completed.")
