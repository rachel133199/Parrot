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
    user_id = int(request.args.get('user_id'))
    print("USER_ID", user_id)
    wr = WordRecommender()
    word = wr.get_next_word(user_id)
    data = {
        'word': word.spelling,
        'phonemes': word.phonemes.split(),
    }
    return jsonify(data)


@app.route('/submit_results', methods=['POST'])
def submit_results():
    """Endpoint to send word pronunciation results."""
    data = request.get_json(force=True)
    user_id = int(data.get('user_id'))
    scores = data.get('scores')
    word = scores[0]['word'].capitalize()
    score = int(scores[0]['score'])
    print(word, score)
    return jsonify({'msg': 'success'})


if __name__ == '__main__':
    app.run(host='', port=8001)
