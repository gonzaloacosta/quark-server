#### Local development 

dev-up:
	docker-compose up --build -d

dev-down:
	docker-compose down

dev-status:
	docker-compose ps -a

healthz:
	curl localhost:8080/healthz

cowsay:
	curl localhost:8080/cowsay

date:
	curl localhost:8080/date

get-posts:
	curl localhost:8080/posts

check-url:  # pass it the name argument, eg `make check-url url=http://example.com`
	curl --data "url=$(url)"  localhost:8080/url

clean-pycache:
	sudo find . -type f -name "*.py[co]" -delete
	sudo find . -type d -name "__pycache__" -exec rm -rv {} +
	sudo find . -type d -name ".pytest_cache" -exec rm -rv {} +
