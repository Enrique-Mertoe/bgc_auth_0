
from flask import url_for, render_template
import jwt
import datetime


def dispatchTemplate(name, **data):
    data.update({
        "theme": {
            "css": {
                "main": url_for("static", filename="css/main.css"),
                "smv": url_for("static", filename="css/smallville.css")
            },
            "js": {
                "main": url_for("static", filename="js/main.js"),
                "smv": url_for("static", filename="js/smallville.js")
            },
            "logo": url_for("static", filename="images/logo.svg"),
            "fav": url_for("static", filename="images/fav.png"),
            "images": url_for("static", filename="images")

        }
    })
    return render_template(f"{name}.html", **data)


SECRET_KEY = "qsjhsa8c768asbdkajs987asdnbks asgda98s7daishdausd7t87$#%$7^7865*&6giujhk"


def create_token(key):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Link expires in 1 hour
    payload = {
        'key': key,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        expiration_time = datetime.datetime.utcfromtimestamp(payload['exp'])
        current_time = datetime.datetime.utcnow()

        if current_time > expiration_time:
            return False, "The password reset link has expired."
        else:
            return True, payload["key"]
    except jwt.InvalidTokenError:
        return False, "Invalid password reset link."


def greet_user(name):
    # nairobi_tz = pytz.timezone('Africa/Nairobi')

    # Get current time in Nairobi
    current_time = datetime.datetime.now()
    # Extract the current hour (24-hour format)
    current_hour = current_time.hour

    if 5 <= current_hour < 12:
        return f"Good morning, {name}!"
    elif 12 <= current_hour < 17:
        return f"Good afternoon, {name}!"
    elif 17 <= current_hour < 20:
        return f"Good evening, {name}!"
    else:
        return f"Good night, {name}!"


def validate_date(day, month, year):
    try:
        day = int(day)
        month = int(month)
        year = int(year)
        min_year = 1900
        max_year = datetime.datetime.now().year + 5

        if not (min_year <= year <= max_year):
            return False

        datetime.datetime(year, month, day)
        return True

    except ValueError:
        return False


def format_email(email):
    # Split the email into local part and domain
    local_part, domain = email.split('@')

    # Mask the local part, keeping the first three letters and replacing the rest with '*'
    formatted_local_part = local_part[:3] + '*' * (len(local_part) - 3)

    # Return the formatted email
    return f"{formatted_local_part}@{domain}"


def prepare_flask_request(request):
    return {
        'https': 'on' if request.url.startswith('https') else 'off',
        'http_host': request.host,
        'server_port': request.environ['SERVER_PORT'],
        'script_name': request.path,
        'path_info': request.path,
        'query_string': request.query_string,
        'request_uri': request.url,
        'http_user_agent': request.headers.get('User-Agent'),
    }
