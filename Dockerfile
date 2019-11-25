FROM python:2.7
ADD . /todoPy
WORKDIR /todoPy
RUN pip install -r requirements.txt
CMD python2 -u app.py
EXPOSE 5000/tcp 
ENV MONGODB_USER=
ENV MONGODB_PASS=