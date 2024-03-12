FROM python:3.8.7
ADD . ./opt/
WORKDIR /opt/
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0 --port=5000
