from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from .generate.queries import random_words, new_random_word, performed_well_words, performed_poorly_words
from .database.engine import check

UPLOAD_EXTENSIONS = ['.docx']

app = Flask(__name__)
CORS(app)
DEBUG = True


check()


@app.route('/get_word', methods=['GET'])
def get_word():
    """End point to get next word and related info."""
    word = random_words(count=1)[0]
    #word = new_random_word(0)
    #word = performed_well_words(1, limit=2)[0]
    #word = performed_poorly_words(2, limit=2)[0]
    data = {
        'word': word.spelling,
        'phonemes': word.phonemes.split(),
    }
    return jsonify(data)


@app.route('/submit_results', methods=['POST'])
def submit_results():
    """Endpoint to send word pronunciation results."""
    data = {'msg': 'success'}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='', port=8001)
