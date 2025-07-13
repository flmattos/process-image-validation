# ---------------------------------
# Targets
# ---------------------------------

.PHONY: install
install:  ## Install package with dev dependencies
	pip install -e .[dev] \
		--extra-index-url https://python.openfilter.io/simple
	curl -O ./utils/example_video.mp4 https://github.com/PlainsightAI/openfilter/blob/main/examples/hello-world/example_video.mp4
	curl -O ./utils/hello.mov https://github.com/PlainsightAI/openfilter/blob/main/examples/hello-ocr/hello.mov

.PHONY: test
test:  ## Run tests
	pytest tests/

.PHONY: clean
clean:  ## Delete all generated files and directories
	sudo rm -rf build/ cache/ dist/ *.egg-info/ telemetry/
	find . -name __pycache__ -type d -exec rm -rf {} +