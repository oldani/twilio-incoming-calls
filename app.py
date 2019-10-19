from collections import deque
from uuid import uuid4

from flask import Flask, render_template
from twilio.jwt.client import ClientCapabilityToken
from twilio.twiml.voice_response import VoiceResponse, Dial


app = Flask(__name__)
app.config.from_object("config.Config")


AVAILABALE_AGENTS = deque()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/leave/<string:agent_id>")
def leave(agent_id):
    if agent_id in AVAILABALE_AGENTS:
        AVAILABALE_AGENTS.remove(agent_id)
    return ""


@app.route("/twilio-webhook", methods=["POST"])
def handle_incoming_call():
    response = VoiceResponse()

    try:
        next_agent = AVAILABALE_AGENTS.popleft()

        dial = Dial()
        dial.client(str(next_agent))
        response.append(dial)
    except IndexError:
        response.say(
            "Lo sentimos, no tenemos agentes disponibles en estos momentos, llame mas tarde!",
            voice="woman",
            language="es-ES",
        )
        response.reject()

    return str(response)


@app.route("/call-done/<string:agent_id>")
def call_done(agent_id):
    """ When agent finish a call add him back to the queue. """
    if agent_id not in AVAILABALE_AGENTS:
        AVAILABALE_AGENTS.append(agent_id)

    return ""


@app.route("/twilio-token")
def generate_app_token():
    capability = ClientCapabilityToken(
        app.config["TWILIO_ACCOUNT_SID"], app.config["TWILIO_AUTH_TOKEN"]
    )

    agent_id = uuid4()
    AVAILABALE_AGENTS.append(agent_id)

    capability.allow_client_incoming(agent_id)
    token = capability.to_jwt()

    return {"token": token.decode(), "agentId": agent_id}
