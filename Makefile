OUTPUT_DIR = docs
STATIC_DIR = static
AUTOGEN_DIR = autogen
PYTHON_DIR = .venv/Scripts

.PHONY: all
all:
	rm -rf $(OUTPUT_DIR)/*
	@mkdir -p $(OUTPUT_DIR)/css $(OUTPUT_DIR)/img
	@cp -r $(STATIC_DIR)/* $(OUTPUT_DIR)
	$(PYTHON_DIR)/python $(AUTOGEN_DIR)/main.py
	$(PYTHON_DIR)/pygmentize -S vs -f html -a .codehilite > $(OUTPUT_DIR)/css/pygments.css