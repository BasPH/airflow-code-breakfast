.PHONY: pytest
pytest:
	pytest tests/

.PHONY: build
build:
	docker build -t basph/airflow-breakfast .

.PHONY: run
run:
	docker rm -f airflow-breakfast || true
	docker run -p 8080:8080 -d -v `pwd`/dags:/root/airflow/dags -v `pwd`/src:/root/airflow_breakfast/src --name airflow-breakfast basph/airflow-breakfast
