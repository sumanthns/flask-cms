def add_registerable():
    def registerable():
        from flask_cms.app import app
        return app.config.get("SECURITY_REGISTERABLE", False)

    return dict(registerable=registerable)

def add_recoverable():
    def recoverable():
        from flask_cms.app import app
        return app.config.get("SECURITY_RECOVERABLE", False)

    return dict(recoverable=recoverable)

def add_confirmable():
    def confirmable():
        from flask_cms.app import app
        return app.config.get("SECURITY_CONFIRMABLE", False)

    return dict(confirmable=confirmable)
