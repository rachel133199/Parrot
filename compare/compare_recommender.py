from joblib import dump, load

similar_words_top_3000 = load('similar_words_top_3000.joblib')
similar_words_top_3000_prop = load('similar_words_top_3000_prop.joblib')


def top_n_similar_words(word, n=10):
    word = word.strip().upper()
    try:
        print('***{}***'.format(word))
        # print('OPEN SOURCE: ', similar_words_top_3000[word][:n])
        print('PROPRIETARY: ', similar_words_top_3000_prop[word][:n])
    except:
        pass



while True:
    word = input()
    top_n_similar_words(word, 20)
