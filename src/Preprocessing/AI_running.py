from gensim.models import Word2Vec
import os
os.chdir(os.path.dirname(__file__))
model=Word2Vec.load("word2vec.model")
outputs = model.wv.most_similar(positive=["警察","銃火器"],negative=["道徳心"], topn=10)
outputs = model.seeded_vector("こんにちは")
for word in outputs:
    print(word)