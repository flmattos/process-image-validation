VERSION ?= $(shell cat VERSION)
export VERSION

.PHONY: install
install:  ## Install package with dev dependencies
	pip install -e .[dev] \
		--extra-index-url https://python.openfilter.io/simple

	@if [ ! -f model.pth ]; then \
		echo "model not found, downloading model archive..."; \
		curl -L -o model.zip https://models.openfilter.io/license_plate_detection_model/v0.1.0.zip; \
		echo "Unzipping model archive to current directory..."; \
		unzip -o model.zip; \
		echo "Removing model.zip..."; \
		rm model.zip; \
	else \
		echo "model already exists, skipping download."; \
	fi
	@if [ ! -f ./utils/example_video.mp4 ]; then \
		echo "Licence plate video not found, downloading..."; \
		curl -L -o ./utils/example_video.mp4 https://github.com/PlainsightAI/openfilter/raw/main/examples/hello-world/example_video.mp4; \
	else \
		echo "Licence plate video found, skipping download."; \
	fi
	@if [ ! -f ./utils/hello.mov ]; then \
		echo "OCR video not found, downloading..."; \
		curl -L -o ./utils/hello.mov https://github.com/PlainsightAI/openfilter/raw/main/examples/hello-ocr/hello.mov; \
	else \
		echo "OCR video found, skipping download."; \
	fi
	
.PHONY: test
test: ## Run tests
	pytest ./tests/e2e/test.py
	pytest ./tests/unit/test.py

.PHONY: run-ocr
run-ocr:
	python ./utils/ocr_video.py

.PHONY: run-branching
run-branching:
	python ./utils/branching_pipeline.py

.PHONY: run-all
run-all: run-ocr run-branching