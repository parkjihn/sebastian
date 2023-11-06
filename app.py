from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    user_input = data['input']

    # For now, Sebastian just repeats what you say
    output = f"You said: {user_input}"

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
