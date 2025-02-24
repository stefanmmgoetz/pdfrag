default: env

env:
	python -m venv env
	env/bin/pip install -r requirements.txt

dev:
	env/bin/pip install jupyterlab jupyterlab-vim

lab:
	env/bin/jupyter lab
