init:
	pip install -r requirements.txt

test:
	tox

update_requirements:
	pip freeze > requirements.txt