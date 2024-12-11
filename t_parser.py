import google.generativeai as genai
import os
import time

if not os.path.exists('static'):
    os.mkdir('static')

import fitz  
from PIL import Image
from IPython.display import Image as IPImage
from constants import vision_prompt,groq_prompt
from init import document_parser, logger,llm
from config import supported_file_types, supported_image_types, model_name, num_portions_per_page

def extract_document_portions(file_path: str, num_portions: int) -> dict:
    """
    Extract portions from a PDF file and parse the document using a language model.

    Args:
    file_path (str): The path to the PDF file.
    num_portions (int): The number of portions to extract from each page.

    Returns:
    dict: The parsed document in JSON format.
    """
    image_paths = []
    image_list = []

    if file_path.lower().endswith(tuple(supported_image_types)):
        image_list.append(IPImage(filename=file_path))
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content([vision_prompt, *image_list])
        image_list.clear()
        out = llm.invoke(groq_prompt+response.text)
        print(out)
        return document_parser.parse(out.content)

    doc = fitz.open(file_path)

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_height = page.rect.height
        portion_height = page_height // num_portions

        for i in range(num_portions):
            top = i * portion_height
            bottom = (i + 1) * portion_height
            rect = fitz.Rect(0, top, page.rect.width, bottom)

            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect, dpi=300)
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            img_path = f"static/portion_{page_num + 1}_{i + 1}.jpeg"
            img.save(img_path)
            image_paths.append(img_path)

    doc.close()

    for im in image_paths:
        image_list.append(IPImage(filename=im))
    logger.info(f"Generated {len(image_list)} images for processing")

    model = genai.GenerativeModel(model_name=model_name)
    response = model.generate_content([vision_prompt, *image_list])
    image_list.clear()
    for name in image_paths:
        os.remove(name)
    logger.info("Parsed document successfully")

    return document_parser.parse(response.text)

def parse_document(file_path: str) -> dict:
    """
    Parse a document using the extract_document_portions function.

    Args:
    file_path (str): The path to the document file.

    Returns:
    dict: The parsed document in JSON format.
    """
    return extract_document_portions(file_path, num_portions_per_page)