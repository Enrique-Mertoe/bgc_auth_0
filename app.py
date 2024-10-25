import os

from main import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

application = app

if __name__ == '__main__':
    app.run(debug=True, host="oauth.localhost", port=9500)
