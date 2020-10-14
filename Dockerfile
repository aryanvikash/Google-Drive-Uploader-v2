FROM ubuntu:18.04

WORKDIR /bot
RUN chmod 777 /bot


RUN apt -qq update
RUN apt -qq install -y python3 python3-pip locales megatools
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
# RUN chmod +x aria.sh

CMD ["python3","-m","bot"]
