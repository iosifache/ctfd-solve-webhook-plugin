FROM python

WORKDIR /

ENV MATTERMOST_BOT_URL=
ENV MATTERMOST_BOT_CHANNEL=
ENV MATTERMOST_BOT_USERNAME=
ENV MATTERMOST_BOT_ICON_EMOJI=
ENV MATTERMOST_BOT_AUTH_TOKEN=

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY server.py server.py

EXPOSE 80

CMD [ "python3", "server.py"]
