start-new: remove-dependencies 
	docker-compose build
	docker-compose up

start-detach:
	docker-compose up -d

start:
	docker-compose build
	docker-compose up

remove-dependencies:
	docker-compose down || true
	docker rm -vf $(docker ps -a -q) || true
	docker rmi -f $(docker images -a -q) || true
	docker volume ls
	docker volume rm mai_ml_development_2023_spamcheck-data || true