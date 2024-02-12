FROM bitnami/python:3.8.8

# Move in server folder
WORKDIR /sighbod

# install dependencies for bot detection
RUN pip install git+https://github.com/mehdigolzadeh/BoDeGHa
RUN pip install git+https://github.com/mehdigolzadeh/BoDeGiC

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in server directory
COPY . .

# Run BotHunter.py
ENTRYPOINT [ "python",  "main.py"]
CMD ["--help"]
