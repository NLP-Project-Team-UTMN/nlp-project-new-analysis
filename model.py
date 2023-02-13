import pandas as pd
import numpy as np
import re
import nltk
from pymorphy2 import MorphAnalyzer
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras import preprocessing
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM

def freqwords(text):                                                            # a function that removes frequent words
    return " ".join([word for word in str(text).split() if word not in freq])

def lemmatize(text):                                                            # the function that makes the lemmatization
    text = re.sub(patterns, ' ', text)
    tokens = []
    for token in text.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]            
            tokens.append(token)
    if len(tokens) > 2:
        return ' '.join(tokens)
    return None

def predict(path):
  with open(path) as file:
    text = str(file.readlines())
    text = f.replace('\\n', '')
  model = keras.models.load_model('/content/model')
  text = freqwords(text)
  patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
  stopwords_ru = stopwords.words("russian")
  morph = MorphAnalyzer()
  text = lemmatize(text)
  text = tfidfconverter.transform([text]).toarray()
  prediction = model.predict(text)
  print("Prediction: "+str(float(prediction[0][0])*100)+"%")
  if (float(prediction[0][0])*100)<=50:
    print("The news will have a bad effect on stocks")
  else:
    print("The news will have a good effect on stocks")  

df = pd.read_csv('/content/drive/MyDrive/Finally_csv')
df_new = df.drop(columns = ['Unnamed: 0', 'level_0', 'index', 'Name of news',
                            'Time', 'Day', 'Month', 'Closing time',
                            'Close', 'Time in 3 hours', 'Closing in 3 hours',
                            'Change'])

binary = {
    'Good':1,
    'Bad':0
}

df_new['Text'] = df_new['Text'].str.lower()

cnt = Counter()
for text in df_new["Text"].values:
    for word in text.split():
        cnt[word] += 1
      
freq = set([w for (w, wc) in cnt.most_common(15)])
df_new["Text"] = df_new["Text"].apply(freqwords) 

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

df_new['Text'] = df_new['Text'].apply(lemmatize)
df_new['Class']=df_new['Class'].map(binary)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(df_new['Text'].tolist())                                 # creating a single dictionary for conversion


textSequences = tokenizer.texts_to_sequences(df_new['Text'].tolist())           # we convert all descriptions into numerical sequences, replacing words with numbers according to the dictionary.


max_words = 0
for desc in df_new['Text'].tolist():
    words = len(desc.split())
    if words > max_words:
        max_words = words
print('Maximum number of words in the longest text: {} words'.format(max_words))

total_unique_words = len(tokenizer.word_counts)
print('Total unique words in the dictionary: {}'.format(total_unique_words))

max_sequence_length = max_words

vocab_size = round(total_unique_words/30)

tfidfconverter = TfidfVectorizer(max_features = max_sequence_length, min_df = 5, max_df = 0.7)
X_lstm = tfidfconverter.fit_transform(df_new['Text']).toarray()
Y_lstm = df_new['Class'].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X_lstm, Y_lstm, shuffle = True, test_size = 0.4)

encoder = LabelEncoder()
encoder.fit(y_train)
y_train = encoder.transform(y_train)
y_test = encoder.transform(y_test)

num_classes = np.max(y_train) + 1
print('Number of categories to classify: {}'.format(num_classes))

# максимальное количество слов для анализа
max_features = vocab_size

print(u'Assembling the model...')
model = Sequential()
model.add(Embedding(max_features, max_sequence_length))
model.add(LSTM(32, dropout = 0.2, recurrent_dropout = 0.2))
model.add(Dense(num_classes, activation='sigmoid'))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print (model.summary())

batch_size = 16
epochs = 3

print(u'Training the model...')
history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(X_test, y_test))

score = model.evaluate(X_test, y_test,
                       batch_size=batch_size, verbose=1)
print()
print(u'Test score: {}'.format(score[0]))
print(u'Estimation of model accuracy: {}'.format(score[1]))

model.save('/content/drive/MyDrive/model')

predict('/content/file.txt')
