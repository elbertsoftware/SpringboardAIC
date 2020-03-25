import confuse


config = None


def get_config():
    global config

    if config == None:
        config = confuse.Configuration('salinization', __name__)

    return config