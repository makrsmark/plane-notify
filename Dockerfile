FROM python:3

WORKDIR /plane-notify

# Set the Chrome repo.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install \
    google-chrome-stable \
    python3-dev=3.9.2-3 \
    --no-install-recommends

# Add pipenv
RUN pip install pipenv==2021.5.29

# Added needed folder for plane-notify process
RUN mkdir /home/plane-notify

# Install dependencies
COPY Pipfile* .
RUN pipenv install

COPY . .
CMD pipenv run python /plane-notify/__main__.py
