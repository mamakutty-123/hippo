


from __future__ import division

import time
import numpy as np

"""Designing a bandit class for experimenting"""

class Bandit(object):

    def generate_reward(self, i):
        raise NotImplementedError


class BernoulliBandit(Bandit):

    def __init__(self, n, probas=None):
        assert probas is None or len(probas) == n
        self.n = n
        if probas is None:
            np.random.seed(int(time.time()))
            self.probas = [np.random.random() for _ in range(self.n)]
        else:
            self.probas = probas

        self.best_proba = max(self.probas)

    def generate_reward(self, i):
        # The player selected the i-th machine.
        if np.random.random() < self.probas[i]:
            return 1
        else:
            return 0

"""Utility functions"""

def incremental_avg(arr):
  avg=[]
  Q=0
  for x in range(len(arr)):
    Q=Q+(arr[x]-Q)/(x+1)
    avg.append(Q)
  return avg

def calculate_maxavg(arm,trials):
  nt=0
  r=0
  for x in trials:
    if x[0] == arm:
      nt+=1
      r+=x[1]
  if nt!=0:
    return float(r/nt)
  else:
    return 0

b=BernoulliBandit(3,probas=[0.274,0.765,0.455])
print("Arm probabilities:",b.probas)

"""Incremental Uniform Algorithm"""

def Inc_uni(bandit,no_episodes):
  n=bandit.n
  avg_rewards=np.zeros(n)
  for epi in range(1,no_episodes):
    temp=avg_rewards.copy()
    for arm in range(n):
      avg_rewards[arm] = bandit.generate_reward(arm)
    avg_rewards = temp + (avg_rewards - temp)/epi
  return temp,np.argmax(temp)

"""Greedy/Epsilon Greedy Algorithm"""

def epsilon_greedy(bandit,no_trials,no_turns,epsilon):
  res_rewards=[]
  trials=[]
  n = bandit.n
  max_avg=np.zeros(n)
  arms=list(range(n))
  for i in range(no_trials):
    x = np.random.randint(n)
    y = bandit.generate_reward(x)
    trials.append((x,y))
    max_avg = np.array(list(map(lambda x : calculate_maxavg(x,trials), arms)))

  graph = []
  for i in range(no_turns):
    if np.random.random() < epsilon:
      x = np.random.randint(n)
    else:
      x = np.argmax(max_avg)
    y = bandit.generate_reward(x)
    res_rewards.append(y)
    trials.append((x,y))
    max_avg = np.array(list(map(lambda x : calculate_maxavg(x,trials), arms)))
  graph = incremental_avg(res_rewards)
  return graph

"""UCB1 Algorithm"""

def UCB1(bandit,no_turns,c):
  res_rewards=[]
  trials=[]
  n = bandit.n
  max_avg=np.zeros(n)
  arms=list(range(n))
  for i in range(n):
    x = i
    y = bandit.generate_reward(x)
    trials.append((x,y))
    max_avg = np.array(list(map(lambda x : calculate_maxavg(x,trials), arms)))

  graph = []
  Nt=np.ones(n)
  for i in range(no_turns):
    x = np.argmax(max_avg + c*np.sqrt(np.log(i+1)/Nt))
    y = bandit.generate_reward(x)
    res_rewards.append(y)
    trials.append((x,y))
    max_avg = np.array(list(map(lambda x : calculate_maxavg(x,trials), arms)))
  graph = incremental_avg(res_rewards)
  return graph

"""Generating rewards using different algorithms"""

epg = epsilon_greedy(b,10,1000,0.25)
g = epsilon_greedy(b,10,1000,0.0)
ucb = UCB1(b,1000,0.75)

"""Plotting and comparing differnt methods' results"""

import matplotlib.pyplot as plt

f = plt.figure()
f.set_figwidth(12)
f.set_figheight(9)

plt.plot(range(len(epg)),epg, label ='Epsilon-greedy(e=0.25)')
plt.plot(range(len(g)),g, label ='Greedy')
plt.plot(range(len(ucb)),ucb,label = 'UCB1(C=0.5)')

plt.xlabel("No of turns")
plt.ylabel("Avg_rewards")
plt.legend()
plt.title('Comparing greedy , ep-greedy and UCB')
plt.show()

"""PAC Optimality"""

arms = list(range(3))
arms

p = BernoulliBandit(4)

def PAC_arm(bandit,epsilon,delta):
  n = bandit.n
  t = int(4*np.power(epsilon,-2)*np.log(2*n/delta))
  avg_rewards = np.zeros(n)
  print(t)
  for epi in range(1,t+1):
    temp=avg_rewards.copy()
    for arm in range(n):
      avg_rewards[arm] = bandit.generate_reward(arm)
    avg_rewards = temp + (avg_rewards - temp)/epi
  return np.argmax(temp)

PAC_arm(p,0.1,0.1)

p.probas

def median_elim_PAC(epsilon,delta,bandit):
  S_l=set(range(bandit.n))
  epsilon_l=epsilon/4
  delta_l=delta/2
  while len(S_l)!=1:
    print(S_l)
    avg_rewards = np.zeros(bandit.n)
    samples=int((1/(epsilon_l/2)**2)*np.log(3/delta_l))
    for a in S_l:
      avg=0
      for i in range(samples):
        avg += bandit.generate_reward(a)
      avg/=samples 
      avg_rewards[a]=avg
    M_l=np.median(avg_rewards)
    temp=list(S_l)
    for arm in temp:
      if avg_rewards[arm]<=M_l:
        S_l.remove(arm)
    epsilon_l=3*epsilon_l/4
    delta_l=delta_l/2
  return S_l

median_elim_PAC(0.1,0.1,p)