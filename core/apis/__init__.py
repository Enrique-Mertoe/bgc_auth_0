from core.apis.builder import _APIBuilder


class API:
    @classmethod
    def get_from(cls, path: str):
        return _APIBuilder(path)

    @classmethod
    def login_user(cls, phone: str):
        res = (_APIBuilder("auth")
               .trigger("login_user")
               .eq(phone=phone, accountType="main")
               .commit())
        return res.ok, res.data

    @classmethod
    def user_recovery(cls, token):
        res = (_APIBuilder("account")
               .trigger("user_recovery")
               .eq(token=token)
               .commit())
        return res.ok, res.data

    @classmethod
    def login_user_password(cls, uid, password: str):
        res = (_APIBuilder("auth")
               .trigger("login_user_password")
               .eq(uid=uid, password=password)
               .commit())
        return res.ok, res.data

    @classmethod
    def create_user(cls, **data):
        res = (_APIBuilder("auth")
               .trigger("create_user")
               .eq(**data)
               .commit())
        return res.ok, res.data

    @classmethod
    def reset_user_password(cls, uid, p1):
        res = (_APIBuilder("account")
               .trigger("reset_user_password")
               .eq(uid=uid, password=p1)
               .commit())
        return res.ok, res.data

    @classmethod
    def create_user_v2(cls, **data):
        res = (_APIBuilder("auth")
               .trigger("create_user_v2")
               .eq(**data)
               .commit())
        return res.ok, res.data
