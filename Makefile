up:
	docker-compose -f docker-compose.yaml up -d

down:
	docker-compose -f docker-compose.yaml down && docker network prune --force 

run:
	cd shift && uvicorn shift.main:app --reload

get_migrations:
	alembic  revision --autogenerate -m "Change User's model" 

upgrade_migrations:
	alembic upgrade heads