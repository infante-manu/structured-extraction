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
from typing import Optional

class StudyData(BaseModel):
    intervention_type: Optional[str] = Field(None, description="Type of intervention tested.")
    total_participants: Optional[int] = Field(None, description="Total number of participants.")
    group_distribution: Optional[str] = Field(None, description="Group-wise distribution of participants.")
    age_mean_range: Optional[str] = Field(None, description="Average or range of participants' age.")
    primary_objective: Optional[str] = Field(None, description="Primary goal of the study.")
    percentage_change: Optional[float] = Field(None, description="Percentage change observed.")
    measurement_method: Optional[str] = Field(None, description="How results were measured.")
    group_comparison: Optional[str] = Field(None, description="Comparison between experimental and control groups.")
    adverse_events: Optional[str] = Field(None, description="Adverse events reported, if any.")
    biomarkers_measured: Optional[str] = Field(None, description="Biomarkers and observed changes.")
    study_duration: Optional[str] = Field(None, description="Duration of the study.")
    therapeutic_indications: Optional[str] = Field(None, description="Conditions targeted in the study.")
    validation_methods: Optional[str] = Field(None, description="Methods used to validate the results.")

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
        template="""You are an advanced language model assisting in extracting structured information from scientific documents related to pharmaceutical research. 
            Your task is to analyze the content of these documents and provide detailed, accurate responses that directly map to a Pydantic schema.

            ### Context:
            - The documents describe pharmaceutical experiments and research.
            - Your job is to extract relevant details for integration into a structured pipeline.
            - Each extracted variable will align with the descriptions provided in the Pydantic schema.

            ### Requirements:
            1. **Behavior:**
            - Extract data strictly from the content of the provided documents.
            - Ensure responses are concise, accurate, and factual.
            - Avoid making assumptions or interpolations beyond what is explicitly stated in the document.

            2. **Handling Missing or Ambiguous Data:**
            - If a piece of information is not explicitly present in the document, return `None` for the corresponding variable.
            - For ambiguous content, include the relevant text snippet from the document for review.

            3. **Robustness:**
            - Handle inconsistencies or contradictions in the document gracefully by returning `None` and adding a note explaining the issue.
            - Focus on reliability and precision in your output.

            ### Objective:
            - Your goal is to enable seamless integration of extracted information into a Pydantic pipeline for analysis in the pharmaceutical domain.
            - Ensure high accuracy and alignment with the schema's descriptions while minimizing errors or inconsistencies.

            Use the following text to extract the required information: {text}
            """
    )
    llm = OpenAI(model="gpt-4o")

    print("Querying model...")
    response = llm.structured_predict(StudyData, prompt, text=raw_file_data)
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
