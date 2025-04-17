from flask import Flask
from routes import api_bp
import os

# Set custom folder locations
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', '1_templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', '2_static')
)

app.register_blueprint(api_bp)

@app.route('/')
def home():
    return app.send_static_file('index.html')  # Optional if you want to serve it directly

if __name__ == '__main__':
    app.run(debug=True)
