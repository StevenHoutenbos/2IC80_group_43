from flask import Flask, render_template, request
from os import system as call

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_file', methods=['POST'])
def run_python_file():
    wifipassword = request.form['nopol']
    call("python /home/emile/Downloads/Lifx_lamp/onboard.py {0}".format(wifipassword))
    return render_template('yougotpwnd.html')

if __name__ == "__main__":
    app.run(debug=True)

