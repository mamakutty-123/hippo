

from __future__ import division

import time
import numpy as np
import itertools

class Bandit(object):

    def generate_reward(self, i):
        raise NotImplementedError


class BernoulliBandit(Bandit):

    def __init__(self, n, m, probas=None):
        assert probas is None or len(probas) == m*n
        self.n = n
        self.m = m
        if probas is None:
            np.random.seed(int(time.time()))
            N = range(n)
            M = range(m)
            c =list(itertools.product(N,M))
            self.probas = {pair:np.random.random() for pair in c}
        else:
            self.probas = probas


    def generate_reward(self, pair):
        # The player selected the i-th machine.
        if np.random.random() < self.probas[pair]:
            return 1
        else:
            return 0

N = 5
M = 5
preference_matrix = np.random.randint(10,size=(N,M))

b = BernoulliBandit(5,5)

def generate_x(epsilon,delta,k):
  x = (2*((k/epsilon)**2))*(np.log(2*k/delta))
  return x

def return_topk(R,k):
  arrsum = np.sum(R,axis=0)
  topk = list((-arrsum).argsort()[:k])
  return topk

def ranking_algorithm(bandit,epsilon,delta,k,preference_matrix):
  R = preference_matrix.copy()
  users = range(bandit.n)
  items = return_topk(R,k)
  x = generate_x(epsilon,delta,k)
  Rank={}
  for rank in range(1,k):
    item_x = items.copy()
    for user in users:
      for item in item_x:
        for trial in range(int(x)):
          R[user][item]+=bandit.generate_reward(pair=(user,item))
    Rank[rank] = return_topk(R,1)[0]
    if Rank[rank] in items:
      items.remove(Rank[rank])
  Rank[k] = items[0]
  return Rank

ranking_algorithm(b,0.9,0.1,3,preference_matrix)