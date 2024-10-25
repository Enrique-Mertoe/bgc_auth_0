from flask import session, url_for, redirect


class Auth:
    @classmethod
    def current_user(cls, f):
        def decorator():
            if session.get("current_user"):
                return f()
            return redirect(url_for("main.login"))

        return decorator

    @classmethod
    def set_user(cls, user):
        session["current_user"] = user

    @classmethod
    def get_user(cls):
        return session["current_user"]

    @classmethod
    def end_session(cls):
        session.clear()
        pass
