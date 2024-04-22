FROM bitnami/python:3.9

# log to stdout
ENV PYTHONUNBUFFERED=1

# Move in server folder
WORKDIR /sighbod

# install dependencies for bot detection
RUN pip install git+https://github.com/mehdigolzadeh/BoDeGHa
RUN pip install git+https://github.com/mehdigolzadeh/BoDeGiC
RUN pip install git+https://github.com/natarajan-chidambaram/RABBIT

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all files in server directory
COPY . .

# ENTRYPOINT ["tail", "-f", "/dev/null"]
# Run BotHunter.py
ENTRYPOINT [ "python",  "main.py"]
CMD ["--help"]
