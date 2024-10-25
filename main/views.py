from core.apis import API
from core.functions import dispatchTemplate, decode_token, greet_user, validate_date, format_email, \
    prepare_flask_request
from core.managers.auth import Auth
from flask import Blueprint, request as req, redirect, url_for

from core.xhr import XHR
from .fn import SMVPage

main = Blueprint("main", __name__)


@main.route('/')
@Auth.current_user
def home():
    user = Auth.get_user()
    return dispatchTemplate("home", page=SMVPage(
        "home"
    ), greet=greet_user(user.get("title")))


@main.route('/auth/login')
def login():
    # auth = OneLogin_Saml2_Auth(prepare_flask_request(req), custom_base_path=SAML_SETTINGS_PATH)
    return dispatchTemplate("auth")


@main.route('/auth/register', methods=["POST", "GET"])
def register():
    if req.method == "POST":
        f = req.form
        if f.get('smv-password') and f.get('smv-password') != f.get('smv-c-password'):
            return XHR.xhr_response(data=None, success=False, error="Passwords dont match!")
        data = {
            "title": f"{f.get('smv-f-name')} {f.get('smv-l-name')}",
            "dob": f"{f.get('smv-dday')}-{f.get('smv-dmonth')}-{f.get('smv-dyear')}",
            "b_name": f.get('smv-b-name'),
            "email": f.get('smv-email'),
            "gender": f.get('smv-gender'),
            "password": f.get('smv-password'),
            "phone": f"{f.get('code')}-{f.get('phone')}"
        }
        options = {}
        ok, data = API.create_user_v2(**data)
        if not ok:
            options["error"] = data

        else:
            user = API.get_from("account").trigger("get_info").eq(uid=data["id"]).commit()
            if user.ok:
                Auth.set_user(user.data)
        return XHR.xhr_response(success=ok, **options)
    return dispatchTemplate("register")


@main.route("/personal-details")
def personal_details():
    return dispatchTemplate("personal-info", page=SMVPage(
        "personal-details"
    ))


@main.route("/security")
def security():
    return dispatchTemplate("security/content", page=SMVPage(
        "security"
    ))


@main.route("/xhr/<endpoint>", methods=["POST", "GET"])
def xhr(endpoint):
    return XHR.builder(endpoint)


@main.route("/auth/recovery")
def recovery():
    user = req.args.get("user_token")

    suc, uid = decode_token(user)
    if not user or not suc:
        return redirect(url_for("main.login"))
    data = (API.get_from("account")
            .trigger("reset_password")
            .eq(uid=uid)
            .commit())

    return dispatchTemplate("auth/recovery", success=data.ok, email=data.data.get("email") if data.ok else None,
                            email_link=format_email(data.data.get("email")) if data.ok else None)


@main.route("/auth/password_reset", methods=["POST", "GET"])
def password_reset():
    token = req.args.get("token")
    if req.method == "POST":
        options = {"is_reset": True}
        p1 = req.form.get("smv-password")
        p2 = req.form.get("smv-c-password")
        uid = req.form.get("smv-target", "")

        if p1 and p1 == p2:
            ok, data = API.reset_user_password(uid.strip(), p1)
            if ok:
                options["rdr"] = url_for("main.login")
            return XHR.xhr_response(success=ok, data=data, **options)
        else:
            return XHR.xhr_response(data="Passwords don`t match!", **options)
    res, data = API.user_recovery(token)
    return dispatchTemplate("auth/password_reset", success=res, message=data)


@main.route("/logout")
def logout():
    Auth.end_session()
    return redirect("/")
