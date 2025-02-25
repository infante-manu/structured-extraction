import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from llama_index.readers.file import PDFReader
from llama_index.llms.openai import OpenAI
import json
from llama_index.core.prompts import PromptTemplate


class LineItem(BaseModel):
    """A line item in an invoice."""

    item_name: str = Field(description="The name of this item")
    price: float = Field(description="The price of this item")


class Invoice(BaseModel):
    """A representation of information from an invoice."""

    invoice_id: str = Field(
        description="A unique identifier for this invoice, often a number"
    )
    date: datetime = Field(description="The date this invoice was created")
    line_items: list[LineItem] = Field(
        description="A list of all the items in this invoice"
    )

def extract_text(file_path):
    pdf_reader = PDFReader()
    documents = pdf_reader.load_data(file_path)
    data = documents[0].text
    return data


def error_exit(error_message):
    print(error_message)
    sys.exit(1)


def show_usage_and_exit():
    error_exit("Please pass name of directory or file to process.")


def enumerate_pdf_files(file_path):
    files_to_process = []
    # Users can pass a directory or a file name
    if os.path.isfile(file_path):
        if os.path.splitext(file_path)[1][1:].strip().lower() == 'pdf':
            files_to_process.append(file_path)
    elif os.path.isdir(file_path):
        files = os.listdir(file_path)
        for file_name in files:
            full_file_path = os.path.join(file_path, file_name)
            if os.path.isfile(full_file_path):
                if os.path.splitext(file_name)[1][1:].strip().lower() == 'pdf':
                    files_to_process.append(full_file_path)
    else:
        error_exit(f"Error. {file_path} should be a file or a directory.")

    return files_to_process


def extract_values_from_file(raw_file_data):

    prompt = PromptTemplate(
       """Extract an invoice from the following text. 
       If you cannot find an invoice ID, use the company name '{company_name}' and 
       the date as the invoice ID: {text}"""
    )
    llm = OpenAI(model="gpt-4o")

    print("Querying model...")
    response = llm.structured_predict(Invoice, prompt, text=raw_file_data, company_name="Uber")
    print("Response from model:")
    print(response.dict())
    return response.json()


def process_pdf_files(file_list):
    for file_path in file_list:
        raw_file_data = extract_text(file_path)
        print(f"Extracted text for file {file_path}:\n{raw_file_data}")
        extracted_json = extract_values_from_file(raw_file_data)
        json_file_path = f"{file_path[:-4]}.json"
        with open(json_file_path, "w") as f:
            f.write(extracted_json)


def main():
    load_dotenv()
    if len(sys.argv) < 2:
        show_usage_and_exit()

    print(f"Processing path {sys.argv[1]}...")
    file_list = enumerate_pdf_files(sys.argv[1])
    print(f"Processing {len(file_list)} files...")
    print(f"Processing first file: {file_list[0]}...")
    process_pdf_files(file_list)


if __name__ == '__main__':
    main()
