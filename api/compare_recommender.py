from joblib import dump, load

similar_words_top_3000 = load('similar_words_top_3000.joblib')
similar_words_top_3000_prop = load('similar_words_top_3000_prop.joblib')


def top_n_similar_words(word, n=10):
    print('***{}***\n'.format(word.upper()))
    print('OPEN SOURCE: ', similar_words_top_3000[word.upper()][:n])
    print('PROPRIETARY: ', similar_words_top_3000_prop[word.upper()][:n])


top_n_similar_words('apple')
