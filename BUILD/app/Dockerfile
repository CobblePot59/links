FROM python:slim-buster
WORKDIR /opt/links
RUN apt update -y && \
    apt install -y gcc libsasl2-dev libldap2-dev && \
	python3 -m pip install gunicorn flask flask-sqlalchemy==2.5.1 flask_simpleldap validators
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:80 --workers=4"
EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["-m", "gunicorn","wsgi:app"]
