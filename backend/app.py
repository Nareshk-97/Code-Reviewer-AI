from flask import Flask
from routes.auth import auth
from routes.review import review

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(review)

if __name__ == "__main__":
    app.run(debug=True)