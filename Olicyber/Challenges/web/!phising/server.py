from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/token_login.php', methods=['GET'])
def getToken():
    print('Token: ', request.args.get('token'))
    return 'ok', 200


if __name__ == '__main__':
    print('use ngrok http 5000')
    app.run(debug=True)