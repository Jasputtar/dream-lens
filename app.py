from flask import Flask
from routes.dream_routes import dream_bp

app = Flask(__name__)

# Register the dream routes blueprint
app.register_blueprint(dream_bp)

if __name__ == '__main__':
    app.run(debug=True)
