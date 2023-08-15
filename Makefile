up:
	docker-compose -f docker-compose.yml up --build

up-d:
	docker-compose -f docker-compose.yml up --build -d

down:
	docker-compose -f docker-compose.yml down && docker network prune --force
