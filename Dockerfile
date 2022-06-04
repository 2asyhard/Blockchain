FROM python:3.9

# Set up code directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install linux dependencies
RUN apt-get update && apt-get install -y libssl-dev
RUN apt-get update && apt-get install -y npm
RUN npm install -g ganache-cli

# install brownie
RUN python3 -m pip install --user pipx
RUN python3 -m pipx ensurepath

# type in this command when setting is complete
# `pipx install eth-brownie`
