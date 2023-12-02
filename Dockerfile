FROM python:3.10
RUN mkdir -p /app
COPY ./azure_poc/* /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD python /app/create_table.py

# docker build ./MailWings -t poc-mail-wings
# docker run -d -p 8080:80 poc-mail-wings