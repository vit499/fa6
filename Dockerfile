FROM python:3.9

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app


WORKDIR /app

COPY requirements.txt /app/requirements.txt

# RUN pip install --upgrade pip && \
#     pip install -r requirements.txt 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app