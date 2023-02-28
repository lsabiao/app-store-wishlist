FROM python:3.10.7

RUN mkdir /srv/wishlist
WORKDIR /srv/wishlist

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 2 -b "0.0.0.0:8180" server:app
