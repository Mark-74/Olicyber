from flask import Flask, request, session, render_template
import random
import string
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'flag{placeholder}')


def generate_code():
    return ''.join(random.choices(string.digits, k=4))


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        pincode = request.form.get('pincode')
        code = generate_code()

        if pincode and code in pincode:
            return render_template('index.html', FLAG=FLAG)
        return render_template('index.html', error='Codice non valido')


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
