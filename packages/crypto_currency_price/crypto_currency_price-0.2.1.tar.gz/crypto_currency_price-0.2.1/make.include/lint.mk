# lint / source format

lint_src = $(project) tests docs

_fmt_lint:  
	isort $(lint_src)
	black $(lint_src)
	flake8 --config tox.ini $(lint_src)

# format source with black, check style, lint with flake8
fmt: _fmt_lint

lint: _fmt_lint

# vim:ft=make
