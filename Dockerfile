FROM python:3

WORKDIR /usr/src/app

ADD . /usr/src/app

ADD requirements.txt /requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/usr/src/app/boto3_venv"

RUN pip install -r /requirements.txt

CMD [ "python", "./boto3_automation_script.py" ]
