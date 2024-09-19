docker compose exec web alembic revision --autogenerate
docker compose exec web alembic upgrade head
