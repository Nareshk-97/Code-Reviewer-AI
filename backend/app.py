from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from routes.review import review

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth)
app.register_blueprint(review)

print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)