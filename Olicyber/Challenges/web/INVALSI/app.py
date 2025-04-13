from flask import Flask, session, redirect, request, render_template
import os
import time
import random
import string

app = Flask(__name__)

def random_str(k=10):
    return ''.join(random.choices(string.ascii_letters, k=k))

app.config['SECRET_KEY'] = random_str(50)
FLAG = os.environ.get('FLAG', 'flag{placeholder}')

local_db = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id', None)

    if user_id is None:
        user_id = random_str()
        session['user_id'] = user_id
        local_db[user_id] = 0

    count = local_db[user_id]

    if request.method == 'GET':
        return render_template('poll.html', count=count)
    else:
        if request.headers.get('Content-Type') == "application/json" and count == 0:
            data = request.json
            if not isinstance(data, list):
                return render_template('poll.html', count=local_db[user_id])

            # Solo i primi 10 record, un attimo per capire
            for r in data[:10]:
                # TODO: aggiungere i dati nel database
                # per adesso lo simulo con una sleep
                time.sleep(0.1)

            local_db[user_id] += 1

        return render_template('poll.html', count=local_db[user_id])


@app.route("/flag", methods=['GET'])
def get_flag():
    user_id = session.get('user_id', None)
    count = local_db[user_id]
    
    if count is None:
        return redirect('/')
    else:
        return render_template('flag.html', count=count, FLAG=FLAG)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
