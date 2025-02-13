from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('./to_send.py', as_attachment=True)

if __name__ == '__main__':
    app.run()
