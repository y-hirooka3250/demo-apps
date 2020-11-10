FROM python:3.8.3

RUN mkdir /post_app

COPY post_app /post_app/post_app

WORKDIR /post_app/post_app

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flask-login
RUN pip install mariadb
RUN pip install pytz

EXPOSE 5000
CMD ["python", "/post_app/post_app/mediaPost.py"]
