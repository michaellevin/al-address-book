FROM python:3.7
WORKDIR /usr/src/address_app
COPY . .
RUN pwd
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 4000
CMD ["python", "run.py"]