venv:
	python3 -m venv .venv
	( \
		. .venv/bin/activate; \
		pip install --upgrade pip; \
		pip install -r src/requirements.txt; \
		pip install -r scale/requirements.txt; \
		pip install -r requirements-dev.txt; \
	)

run:
	( \
		. .venv/bin/activate; \
		cd ./src; \
		python ./app.py; \
	)

test:
	( \
		. .venv/bin/activate; \
		export PYTHONPATH=./src:$$PYTHONPATH; \
		pytest -v; \
	)

build:
	sam build && sam validate --region us-east-1 --lint

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
	cd src; \
	docker build -t xx .; \
	)

docker-run:
	( \
	docker run -it xx; \
	)