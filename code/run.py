from flask import Flask
from routes import api_bp
import os
from flask import render_template

# Set custom folder locations
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', '1_templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', '2_static')
)

app.register_blueprint(api_bp)

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)




#python code/run.py
#http://127.0.0.1:5000/
