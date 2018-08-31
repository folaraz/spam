from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from app.processor.wordprocess import separator, correction


class Process(object):

    def __init__(self,body):
        try:
            self.body = body.decode("utf-8")
        except Exception as e:
            self.body = body
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.punctuations = string.punctuation

    def process(self):
        vocabulary = []
        all_words = self.tokenizer.tokenize(self.body.lower())
        lemma_words = [self.lemmatizer.lemmatize(i) for i in all_words]
        words = [i for i in lemma_words if i not in self.stopwords]

        for word in words:
            word = separator(word)
            for c in word:
                if c not in self.punctuations:
                    vocabulary.append(c)

        vocabulary = set(vocabulary)
        corrected = [correction(i) for i in vocabulary]
        corrected = set(corrected)

        return corrected


