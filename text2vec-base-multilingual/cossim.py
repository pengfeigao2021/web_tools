import sys
import time
from termcolor import colored
from text2vec import SentenceModel
import numpy as np
sys.path.insert(0, '/Users/AlexG/Documents/GitHub/web_tools/sqlite')
import embedding_util

path = '/Users/AlexG/data/text2vec-base-multilingual'
def timecost(start, title=''):
    print(
        colored(
        '{} time cost: {:.3f}s'.format(
            title,
            time.time() - start
        ), 'grey', attrs=['bold'])
        )

def cossim(s1, s2):
    """
    Compute cosine similarity
    """
    start = time.time()
    model = SentenceModel(path)
    print('time to load model:', time.time() - start)
    # print colored time
    timecost(start)

    start = time.time()
    embeddings = model.encode((s1, s2))
    # print colored time
    timecost(start)
    a = embeddings[0]
    b = embeddings[1]
    sim = np.dot(a, b) / (np.linalg.norm(a)
        * np.linalg.norm(b))
    print('cosine similarity between a and b: {:.2f}'.format(sim))
    return sim


class CosineSim(object):
    def __init__(self, model_path=path):
        start = time.time()
        print('time to load model:')
        self.model = SentenceModel(model_path)
        # print colored time
        timecost(start)

    def get_emb(self, s):
        start = time.time()
        res = embedding_util.read_embedding(s)
        if len(res) == 0:
            embeddings = self.model.encode((s,))
            print('type emb:', type(embeddings[0]))
            print(len(embeddings[0]))
            embedding_util.write(s, embeddings[0])
        else:
            embeddings = [v[2] for v in res]
        # print colored time
        timecost(start)
        return embeddings[0]

    def get_similarity(self, s1, s2):
        start = time.time()
        embeddings = self.model.encode((s1, s2))
        # print colored time
        timecost(start)
        a = embeddings[0]
        b = embeddings[1]
        sim = np.dot(a, b) / (np.linalg.norm(a)
            * np.linalg.norm(b))
        print('cosine similarity: {:.2f}'.format(sim))
        return sim

    def cosine(self, emb1, emb2):
        a = emb1
        b = emb2
        sim = np.dot(a, b) / (np.linalg.norm(a)
            * np.linalg.norm(b))
        return sim

if __name__ == '__main__':
    cossim('Apple MacBook Air 13-inch (M3) review', 'Apple Vision Pro review')