from flask import Flask, request, jsonify
from flask_cors import CORS
import random

UPLOAD_EXTENSIONS = ['.docx']

app = Flask(__name__)
CORS(app)
DEBUG = True


@app.route('/get_word', methods=['GET'])
def get_word():
    """End point to get next word and related info."""
    words = ['apple',
             'banana',
             'orange']
    phonemes = [['AE1', 'P', 'AH0', 'L'],
                ['B', 'AH0', 'N', 'AE1', 'N', 'AH0'],
                ['AO1', 'R', 'AH0', 'N', 'JH']]
    idx = random.randrange(len(words))
    data = {'word': words[idx],
            'phonemes': phonemes[idx]}
    return jsonify(data)


@app.route('/submit_results', methods=['POST'])
def submit_results():
    """Endpoint to send word pronunciation results."""
    data = {'msg': 'success'}
    # data = request.data
    print(request.data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='', port=8001)
