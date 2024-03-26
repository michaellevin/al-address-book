FROM python:3.7
WORKDIR /usr/src/address_app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 4000
CMD ["python", "-m", "unittest", "discover", "tests"]