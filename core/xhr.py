from flask import jsonify, request as req

from core.apis import API
from core.functions import dispatchTemplate, create_token, validate_date
from core.managers.auth import Auth


class XHR:
    @classmethod
    def builder(cls, endpoint):
        try:
            return getattr(XHR, endpoint)()
        except Exception as e:
            print(e)
            return cls.xhr_response()

    @classmethod
    def auth(cls):
        step = req.args.get("step")
        if step == "start":
            code = req.form.get("code")
            phone = req.form.get("phone")
            suc, res = API.login_user(f"{code}-{phone}")
            if suc:
                l_id = res.get("id")
                l_type = res.get("type")
                if l_type == "new":
                    suc = False
                    res = "Account not found!"
                else:
                    token = create_token(l_id)
                    res = dispatchTemplate("xhr/auth_password", target=l_id, token=token)
            return cls.xhr_response(success=suc, data=res)
        if step == "finish":
            uid = req.form.get("target")
            password = req.form.get("password")
            suc, res = API.login_user_password(uid, password)
            if suc:
                user = API.get_from("account").trigger("get_info").eq(uid=uid).commit()
                if user.ok:
                    Auth.set_user(user.data)
            return cls.xhr_response(success=suc, data=res, finish=True)

        return cls.xhr_response()

    @classmethod
    def form_register(cls):
        step = int(req.args.get("step", 0))
        options = {}
        f = req.form
        re_data = dispatchTemplate("auth/xhr", step=step + 1)
        if step == 2:
            user = API.get_from("account").trigger("get_info").eq(email=f.get('smv-email')).commit()
            if user.ok and user.data:
                options["error"] = "Email taken!"
                return cls.xhr_response(**options)
        if step == 3:
            phone = f"{f.get('code')}-{f.get('phone').lstrip('0')}"
            user = API.get_from("account").trigger("get_info").eq(phone=phone).commit()
            if user.ok and user.data:
                options["error"] = "Phone Number Exists"
                return cls.xhr_response(**options)
        if step == 4:
            date = validate_date(f.get('smv-dday'), f.get('smv-dmonth'), f.get('smv-dyear'))
            if not date:
                options["error"] = "Invalid date"
                return cls.xhr_response(**options)

        if step == 5:
            options["can_send"] = True
        return cls.xhr_response(success=True, data=re_data, **options)

    @classmethod
    def xhr_response(cls, *, success=False, data=None, **options):
        return jsonify({
            "ok": success,
            "data": data,
            **options
        })
