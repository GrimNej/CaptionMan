.PHONY: setup api-sync api-test api-lint api-run-mock validate docker-build docker-run-mock docker-doctor web-install web-dev web-build hygiene secrets doctor all-checks

setup:
	cd apps/api && uv sync
	pnpm install

api-sync:
	cd apps/api && uv sync

api-test:
	cd apps/api && uv run pytest

api-lint:
	cd apps/api && uv run ruff check . && uv run ruff format --check .

api-run-mock:
	cd apps/api && AI_PROVIDER=mock uv run captionman run --input ../../input/tasks.json --output ../../output/results.json

validate:
	python scripts/validate_results.py output/results.json

docker-build:
	docker build -t captionman .

docker-doctor:
	docker run --rm captionman captionman doctor

docker-run-mock:
	docker run --rm -e AI_PROVIDER=mock -v "$$PWD/input:/input" -v "$$PWD/output:/output" captionman

web-install:
	pnpm install

web-dev:
	pnpm --filter web dev

web-build:
	pnpm --filter web build

hygiene:
	python scripts/check_source_hygiene.py

secrets:
	python scripts/check_no_secrets.py

doctor:
	cd apps/api && uv run captionman doctor

all-checks: api-lint api-test api-run-mock validate hygiene secrets docker-build docker-doctor docker-run-mock validate
