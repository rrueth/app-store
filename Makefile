init:
	pip install -r requirements.txt

test:
	python -m unittest discover

update_requirements:
	pip freeze > requirements.txt