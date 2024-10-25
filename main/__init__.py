from flask import Flask
# from bgc_cloud import BGCCloud, Credentials
from .views import main
from settings import config, BASE_PATH

# BGCCloud.initialise(Credentials(api_key="bgc_key0a0271de697d09a9997dfdcf5c26e7ff17f5c2c527ddb074df5bf49588765f01"))


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])
    app.template_folder = BASE_PATH.joinpath("resources/templates")
    app.static_folder = BASE_PATH.joinpath("resources/static")
    app.register_blueprint(main)
    return app
