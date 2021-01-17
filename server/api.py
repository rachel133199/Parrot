from flask import Flask, request, jsonify
from flask_cors import CORS
from .generate.WordRecommender import WordRecommender
from .database.engine import check

UPLOAD_EXTENSIONS = ['.docx']

app = Flask(__name__)
CORS(app)
DEBUG = True


check()


@app.route('/get_word', methods=['GET'])
def get_word():
    """End point to get next word and related info."""
    wr = WordRecommender()
    word = wr.get_next_word(1)
    data = {
        'word': word.spelling,
        'phonemes': word.phonemes.split(),
    }
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
