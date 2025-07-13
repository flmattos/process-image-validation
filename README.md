# 🔍 Process-Image-Validation
## 📑 Table of Contents
1. Overview
2. Project Structure
3. Filter Descriptions
4. Dependencies and Setup
5. Validation Structure
6. Submission Content

## Overview
This repository is designed to validate two filters available via the [openfilter](https://github.com/PlainsightAI/openfilter):

- [Hello World OCR](https://github.com/PlainsightAI/openfilter/tree/main/examples/hello-ocr)
- [License Plate Detection](https://github.com/PlainsightAI/openfilter/tree/main/examples/hello-world)

## Filter Descriptions
📝 **Hello World OCR**: 
- *Input*: .mov video
- *Functionality*: Processes multiple frames containing different variations of the phrase *Hello World*, commonly used in technology demos.
- *Goal*: Detect and extract occurrences of *Hello World* frame by frame, returning the results in a structured format.

🚗 **License Plate Detection**:
- *Input*: .mp4 video of a vehicle
- *Functionality*: Detects the location of the license plate in the video.
- *Goal*: Localize the plate and perform OCR to extract possible license plate values.

## Dependencies and Setup
1. **[Recommended]** Create a virtual environment using ```venv```
```bash
python -m venv venv
source venv/bin/activate
```
2. Install dependencies and download required files using ```make install```
3. You can run the tests using ```make test```
4. You can run the OCR filter using ```make run-ocr```
5. You can run the Branching Pipeline (OCR + License Plate Detection) using ```make run-branching```
6. You can run the both filters mention in topic 4 and 5 together using ```make run-all```

## Validation Structure
Validation is structured into the following components:

```bash
├── tests/
│   ├── e2e/
│   └── unit/
└── utils/
```
### 🔁 **tests/e2e/** 
This folder represents a End-to-End (**E2E**) testing, and, inside have a *test.py* script executes the filters using Filter.multirun([]) calling **utils/ocr_video.py**. 
It validates:

- That the process to run the filter it's **completes successfully**.
- That the expected **.json** output is generated.
- That the output includes at least one instance of the phrase **"Hello World"** (for the OCR filter).
> The output **.json** follows the Webvis metadata format, enabling compatibility with visualization tools and downstream processing.
- There's a failure scenario where the video input is incorrectly passed to the filter, this execution is made calling **utils/ocr_video_failure.py** and the system expects it to not return the **.json** file because it didn't find the video.
- One of the test scenarios targets validation of the **utils/branching_pipeline.py**, which is designed to execute both the Hello World OCR and License Plate Detection filters concurrently on a shared input stream. The .mp4 format is chosen for this test case, as it supports both:
    - Object detection outputs (e.g., bounding boxes for license plates)
    - Text recognition (via OCR for detecting the phrase "Hello World")
This scenario ensures that the framework supports concurrent filter execution and validates interoperability of the output formats.

### 🔁 **tests/unit/**
This folder represents a **Unit testing**, and, inside have a *test.py* script executes the filters using CLI command calling **run_pipeline_cli_OCR** function. A .mov file containing variations of the text "Hello World". It validates:

- The process completes successfully
- The expected output .json file is generated
- The logs directory is created
- The output contains the expected OCR results, including the keywords "Hello" and "World" extracted from video frames.
- The failure scenario validates system behavior when an invalid or mismatched video input is provided and verifies whether the .json file is created or not.

### ⚙️ utils/
The utils/ directory contains essential assets and executable scripts used for running and validating the filter pipelines. These components serve as the foundation for both unit and integration tests, enabling flexible execution of individual filters as well as multi-branch workflows.

```bash
├── utils/
│   ├── branching_pipeline.py
│   ├── ocr_video_failure.py
|   ├── ocr_video.py
```

- **ocr_video.py**:
Executes the Optical Character Recognition (OCR) pipeline using openfilter. Processes a video file containing variations of the phrase "Hello World", extracting text frame-by-frame via EasyOCR.
- **ocr_video_failure.py**:
Simulates a failure scenario where an invalid or incompatible video input is provided. This script is used to test how the system handles missing or malformed input sources and ensures graceful handling of failed executions.
- **branching_pipeline.py**:
Executes a branching pipeline, where both the OCR and License Plate Detection filters run concurrently on the same input stream. Validates the framework's ability to handle parallel filter execution and shared data flow.
- **hello.mov**:
Test video specifically designed for the OCR filter. Contains multiple frames with stylized "Hello World" text, ideal for evaluating text detection capabilities.
- **example_video.mp4**
Generic video used for running the branching pipeline. It contains both readable text and a visible license plate, enabling simultaneous validation of OCR and object detection filters.
> *"hello.mov"* and *"example_video.mp4"* these assets are excluded from version control via *.gitignore* to avoid repository bloat and maintain performance. Large binary files (e.g., .mov, .mp4) are not suitable for Git standard.

## Resume
In alignment with the original technical proposal, this repository satisfies the required implementation and validation scope through the following components:

- **Pipeline Implementation**: 
Refactored and extended pipeline scripts to support modular execution of OCR and License Plate Detection filters, including a branching pipeline scenario for concurrent execution.

- **Test Coverage**:
Comprehensive test suite including the unit tests for isolated logic validation and E2E tests for full pipeline integration and behavioral verification.

- **Media Assets**:
Sample input videos (.mov, .mp4) designed to simulate scenarios for both OCR and plate detection cases.

- **Documentation**:
Updated README and inline comments describing the architecture, usage instructions, validation approach, and all stufs.

- **Bonus Feature**
Implementation of a branching pipeline, demonstrating concurrent filter execution using a shared video stream — enabling both textual and object detection within a unified flow, and, failure scanerios in unit and E2E tests.