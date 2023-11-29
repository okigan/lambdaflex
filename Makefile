venv:
	python3 -m venv .venv
	( \
		. .venv/bin/activate; \
		pip install --upgrade pip; \
		pip install -r services/pet-store/src/requirements.txt; \
		pip install -r infra/requirements.txt; \
		pip install -r requirements-dev.txt; \
		mypy --install-types; \
	)

run:
	( \
		. .venv/bin/activate; \
		cd ./services/pet-store/src; \
		python ./app.py; \
	)

test:
	( \
		. .venv/bin/activate; \
		cd ./services/pet-store/; \
		python -m pytest --verbosity 3; \
	)
	( \
		. .venv/bin/activate; \
		cd ./infra; \
		python -m pytest --verbosity 3; \
	)

build:
	( \
		. .venv/bin/activate; \
		export SAM_CLI_TELEMETRY=0; \
		sam build -u -c  --debug && sam validate --region us-east-1 --lint; \
	)

package:
	sam package --resolve-s3 --output-template-file packaged.yaml --s3-bucket sam-artifacts-xxxx

deploy:
	sam deploy  --config-env dev --resolve-image-repos --disable-rollback 

delete:
	sam delete  --config-env dev 

scale-up:
	( \
	cd scale; \
	./xxxx.sh; \
	)

docker-build:
	( \
	cd services/pet-store/src; \
	docker build -t xx .; \
	)

docker-run:
	( \
	docker run -it xx; \
	)