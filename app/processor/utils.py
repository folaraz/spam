from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from stop_words import get_stop_words
from string import ascii_letters
import string
from app.processor.wordprocess import separator, correction


def filter_chinese(word):
    allowed = set(ascii_letters)
    count = 0
    for letter in word:
        if letter in allowed:
            count += 1
            if count >=1:
                return word
            else:
                return 'No'


def remove_wrong_words(word):
    if word.count('_') <= 1 and len(word) < 20:
        return word
    else:
        return ''


class Process(object):

    def __init__(self, body):
        self.body = body.decode("utf-8")
        self.stopwords = get_stop_words('english')
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.punctuations = string.punctuation

    def process(self):
        vocabulary = []
        all_words = self.tokenizer.tokenize(self.body.lower())
        lemma_words = [self.lemmatizer.lemmatize(i) for i in all_words]
        words = [i for i in lemma_words if i not in self.stopwords]

        for word in words:
            if filter_chinese(word) == None:
                word = ''
            word = remove_wrong_words(word)
            word = separator(word)
            for c in word:
                if c not in self.punctuations:
                    vocabulary.append(c)

        vocabulary = set(vocabulary)
        corrected = [correction(i) for i in vocabulary]
        corrected = set(corrected)

        return corrected


