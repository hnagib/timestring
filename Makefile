SHELL=/bin/bash

install-env:
	conda create -n timestring python=3.7
	source activate timestring && pip install -r requirements.txt
	conda install ipykernel
	python -m ipykernel install --user --name timestring --display-name "timestring"

uninstall-env:
	conda remove --name timestring --all
