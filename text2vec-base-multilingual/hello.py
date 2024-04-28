import time
from termcolor import colored
from text2vec import SentenceModel
import numpy as np
sentences = ['如何更换花呗绑定银行卡', 'How to replace the Huabei bundled bank card']

path = '/Users/AlexG/data/text2vec-base-multilingual'
# model = SentenceModel('shibing624/text2vec-base-multilingual')
start = time.time()
model = SentenceModel(path)
print('time to load model:', time.time() - start)
# print colored time
print(colored('time to load model:', 'red', attrs=['bold']) +
    colored(str(time.time() - start), 'green', attrs=['bold']))

start = time.time()
embeddings = model.encode(sentences)
# print colored time
print(colored('time to encode:', 'red', attrs=['bold']) +
    colored(str(time.time() - start), 'green', attrs=['bold']))
print(embeddings)
a = embeddings[0]
b = embeddings[1]
print('cosine similarity between a and b: {:.2f}'.format(
    np.dot(a, b)
    / (np.linalg.norm(a)
       * np.linalg.norm(b))
))
