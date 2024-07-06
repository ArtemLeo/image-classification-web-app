# Specify your base image
FROM python:3.12.2
# create a work directory
RUN mkdir /app
# navigate to this work directory
WORKDIR /app
#Copy all files
COPY requirements.txt
# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
# Run
CMD ["python","app.py"]