FROM continuumio/miniconda3:4.5.12

ENV SLUGIFY_USES_TEXT_UNIDECODE=yes \
	PYTHONDONTWRITEBYTECODE=1 \
	AIRFLOW__CORE__LOAD_EXAMPLES=False \
	AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True \
	AIRFLOW__WEBSERVER__WORKERS=1 \
	AIRFLOW_SCHEDULER_DAG_DIR_LIST_INTERVAL=30

RUN mkdir -p /root/airflow_breakfast/src
COPY setup.py /root/airflow_breakfast
COPY entrypoint.sh /root/airflow_breakfast
COPY src /root/airflow_breakfast/src
COPY dags /root/airflow/dags

RUN apt-get update && \
	apt-get install -y gcc g++ --no-install-recommends && \
    conda install --yes python=3.6 -n base && \
    pip install -e /root/airflow_breakfast && \
    airflow initdb && \
	apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "/root/airflow_breakfast/entrypoint.sh"]
