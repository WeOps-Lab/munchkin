push:
	git add . && codegpt commit . && git push

setup:
	virtualenv .venv -p python3.10