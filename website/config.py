import socket

class Config:

    # Load in enviornemnt variables
    TESTING = 'False'
    FLASK_DEBUG = 'True'
    SECRET_KEY = 'youwontguessthiskeys'
    SERVER = socket.gethostbyname(socket.gethostname())
