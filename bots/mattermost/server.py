import json
import os
import urllib.request as request

from flask import Flask
from flask import request as flask_request

app = Flask(__name__)

app.config["URL"] = os.environ.get("MATTERMOST_BOT_URL", None)
app.config["CHANNEL"] = os.environ.get("MATTERMOST_BOT_CHANNEL", None)
app.config["USERNAME"] = os.environ.get("MATTERMOST_BOT_USERNAME", None)
app.config["ICON_EMOJI"] = os.environ.get("MATTERMOST_BOT_ICON_EMOJI", None)
app.config["AUTH_TOKEN"] = os.environ.get("MATTERMOST_BOT_AUTH_TOKEN", None)

if not (
    app.config["URL"]
    and app.config["CHANNEL"]
    and app.config["USERNAME"]
    and app.config["ICON_EMOJI"]
    and app.config["AUTH_TOKEN"]
):
    exit()


def make_ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]

    return str(n) + suffix


def create_message(data: dict) -> str:
    solver = data["team"] if data["team"] else data["user"]
    solve_ordinal = make_ordinal(data["solve_id"])
    category = data["category"]
    challenge = data["challenge"]

    return (
        f"Congratulations {solver} for the "
        f"{solve_ordinal} solve on {challenge} ({category})!"
    )


def create_mattermost_data(data: dict) -> dict:
    message = create_message(data)

    return {
        "channel": app.config["CHANNEL"],
        "username": app.config["USERNAME"],
        "icon_emoji": app.config["AUTH_TOKEN"],
        "text": message,
    }


def make_request(url: str, data: dict) -> None:
    mattermost_data = create_mattermost_data(data)
    json_data = json.dumps(mattermost_data)
    json_data_bytes = json_data.encode("utf-8")

    req = request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("Content-Length", len(json_data_bytes))
    request.urlopen(req, json_data_bytes)


@app.route("/", methods=["POST"])
def hello():
    token = flask_request.args.get("token", None)
    if not token or token != app.config["AUTH_TOKEN"]:
        return "", 401

    data = flask_request.get_json()
    make_request(app.config["URL"], data)

    return "", 201


app.run(host="0.0.0.0", port=8080)
