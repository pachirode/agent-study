# Project settings
PYTHON_VERSION = 3.12

.PHONY: init clean test shell

# Initialize the project using Hatch (no Conda)
init:
	@echo "Setting up hatch environment..."
	hatch env create default
	@echo "--------------------------------------------------------"
	@echo "Initialization complete!"
	@echo "To start working, run:"
	@echo "  hatch shell"
	@echo "--------------------------------------------------------"
	@echo "Python interpreter path:"
	@hatch run python -c "import sys; print(sys.executable)"

# Enter the hatch environment
shell:
	hatch shell

# Clean up build artifacts and hatch environments
clean:
	rm -rf dist .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	hatch env prune

# Run tests
test:
	hatch run test
