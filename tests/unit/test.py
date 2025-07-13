import subprocess
import os
import json
import pytest
import unittest

VIDEO_PATH = "utils/hello.mov"
OUTPUT_PATH = "output/subject_data.json"
SCRIPT_PATH = "utils/ocr_video.py"
LOGS_PATH = "logs/"
 
def run_pipeline_cli_OCR():
    result = subprocess.run(
        [
            "openfilter",
            "run",
            *"""
            - VideoIn
                --sources file://utils/hello.mov!no-loop'
            - filter_optical_character_recognition.filter.FilterOpticalCharacterRecognition
                --ocr_engine easyocr
                --forward_ocr_texts true
            - Webvis
        """.strip().split(),
            ])
    return result

def test_OCR_CLI():
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    result = run_pipeline_cli_OCR()

    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"
    assert os.path.exists(OUTPUT_PATH), "OCR output JSON was not created."
    assert os.path.exists(LOGS_PATH), "OCR output LOGS was not created."

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    extracted_texts = [frame.get("meta", {}).get("ocr_texts", []) for frame in data]
    substringHello = "Hello"
    substringWorld = "World"
    assert (substringHello in text for text in extracted_texts), "Expected OCR text 'hello' not found."
    assert (substringWorld in text for text in extracted_texts), "Expected OCR text 'world' not found."

def run_pipeline_cli_OCR_failure():
    result = subprocess.run(
        [
            "openfilter",
            "run",
            *"""
            - VideoIn
                --sources file://utils/hello.mp4!no-loop'
            - filter_optical_character_recognition.filter.FilterOpticalCharacterRecognition
                --ocr_engine easyocr
                --forward_ocr_texts true
            - Webvis
        """.strip().split(),
            ])
    return result

def test_OCR_CLI_failure():
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    run_pipeline_cli_OCR_failure()

    os.path.exists(OUTPUT_PATH), "OCR output JSON was not created."