# gunicorn-local:
# 	gunicorn --worker-class eventlet --workers 1 --bind localhost:3000 wsgi:app

run:
	FLASK_APP=main.py flask run -h localhost -p 3000

init:
	pip install -r requirements.txt

test:
	py.test tests

# gunicorn:
# 	gunicorn --worker-class eventlet --workers 1 --bind unix:hsl_backend.sock wsgi:app

docker-build:
	docker build --label hsl_backend --tag hsl_backend .

docker-run:
	docker run -p 3000:3000 hsl_backend

.PHONY: init test run
