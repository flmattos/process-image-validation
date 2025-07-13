import subprocess
import os
import json
from pathlib import Path

VIDEO_PATH = "utils/hello.mov"
OUTPUT_PATH = "output/subject_data.json"
SCRIPT_PATH = "utils/ocr_video.py"
SCRIPT_PATH_FAILURE = "utils/ocr_video_failure.py"
SCRIPT_BRANCHING_PATH = "utils/branching_pipeline.py"


def run_pipeline():
    result = subprocess.Popen(['python', SCRIPT_PATH])
    result.wait()
    return result

def test_e2e_pipeline():
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    result = run_pipeline()    
    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"

    assert os.path.exists(OUTPUT_PATH), "OCR output JSON was not created."

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    extracted_texts = [frame.get("meta", {}).get("ocr_texts", []) for frame in data]
    assert any("Hello World" in text for text in extracted_texts), "Expected OCR text 'hello' not found."

def run_pipeline_failure():
    result = subprocess.Popen(['python', SCRIPT_PATH_FAILURE])
    result.wait()
    return result

def test_e2e_pipeline_failure():
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    run_pipeline_failure()    

    assert not os.path.exists(OUTPUT_PATH), "OCR output JSON was not created."

def run_branching_pipeline():
    result = subprocess.Popen(['python', SCRIPT_BRANCHING_PATH])
    result.wait()
    return result

def test_branching_pipeline():
    result = run_branching_pipeline()  
    assert result.returncode == 0
