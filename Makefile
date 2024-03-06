LINT_PATHS = *.py

mypy:
	mypy ${LINT_PATHS} --install-types --non-interactive

lint:
	# stop the build if there are Python syntax errors or undefined names
	# see https://www.flake8rules.com/
	ruff ${LINT_PATHS} --select=E9,F63,F7,F82 --output-format=full
	# exit-zero treats all errors as warnings.
	ruff ${LINT_PATHS} --exit-zero

format:
	# Sort imports
	ruff --select I ${LINT_PATHS} --fix
	# Reformat using black
	black ${LINT_PATHS}
	# yamlfmt data/*.yaml

check-codestyle:
	# Sort imports
	ruff --select I ${LINT_PATHS}
	# Reformat using black
	black --check ${LINT_PATHS}

commit-checks: format type lint

live-reload:
	when-changed html/ data/ read.py -c python read.py

.PHONY: lint format check-codestyle commit-checks doc spelling docker type pytest


server:
	python3 -m http.server

# live-server:
# 	livereload