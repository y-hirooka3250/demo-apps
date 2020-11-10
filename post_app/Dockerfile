FROM python:3.8.3

RUN mkdir /post_app

COPY post_app /post_app/post_app

WORKDIR /post_app/post_app

RUN pip install --upgrade pip --proxy http://10.51.8.102:8080/
RUN pip install flask --proxy http://10.51.8.102:8080/
RUN pip install flask-login --proxy http://10.51.8.102:8080/
RUN pip install mariadb --proxy http://10.51.8.102:8080/
RUN pip install pytz --proxy http://10.51.8.102:8080/

EXPOSE 5000
CMD ["python", "/post_app/post_app/mediaPost.py"]
