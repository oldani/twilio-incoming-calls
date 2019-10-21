import os


class Config:
    DEBUG = False
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
