dev:
	uvicorn app.main:app --reload

format:
	black ./app
