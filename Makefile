dev:
	uvicorn app.main:app --reload

format:
	ruff format ./app
