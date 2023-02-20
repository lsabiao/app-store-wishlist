FROM python:3.10.7

RUN mkdir /srv/wishlist
WORKDIR /srv/wishlist

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD python server.py
