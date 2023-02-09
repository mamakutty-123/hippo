

from __future__ import division

import time
import numpy as np
import random
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

"""# Multi arm Bandit Problem"""

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

"""# Epsilon Greedy Approach"""

multi_arm=BernoulliBandit(4)
multi_arm.probas

"""**Generating first 10 trials**"""

reward=np.array([])
arm=np.array([],dtype=int)
no_of_arms=multi_arm.n
for i in range(10):
  a=random.randint(0,3)
  arm=np.append(arm,np.array([a]))
  reward=np.append(reward,np.array([multi_arm.generate_reward(a)]))

arm

def epsilon_greedy(arm,reward,epsilon,n):
  Qt=np.zeros(n)
  for i in range(n):
    for s in range(len(arm)):
      if arm[s]==i:
        Qt[i]+=reward[s]
    Qt[i]=Qt[i]/np.count_nonzero(arm==i)
  if np.random.random() < epsilon:
    At=np.random.randint(n)
  else:
    At=np.argmax(Qt)
  arm=np.append(arm,np.array([At]))
  reward=np.append(reward,np.array([multi_arm.generate_reward(At)]))
  return At,arm,reward

At,arm1,reward1=epsilon_greedy(arm,reward,0,no_of_arms)
print("Arm to be chosen at 11th trial with greedy approach: ",At)

At,arm1,reward1=epsilon_greedy(arm,reward,0.25,no_of_arms)
print("Arm to be chosen at 11th trial with epsilon greedy approach: ",At)

"""# Incremental Uniform"""

def incremental_uniform(bandit,no_of_turns):
  Qt=np.zeros(bandit.n)
  rewards=[]
  for i in range(1,no_of_turns):
    for j in range(bandit.n):
      Qt[j]=Qt[j]+(bandit.generate_reward(j)-Qt[j])/i
  At=np.argmax(Qt)
  return At

print("Arm to be chosen after 15 trials using uniform incremental algorithm :",incremental_uniform(multi_arm,15))

"""# UCB algorithm"""

def ucb(arm,reward,n):
  Nt=np.zeros(n)
  Qt=np.zeros(n)
  for a in arm:
    Nt[a]+=1
  t=len(arm)
  for i in range(n):
    for s in range(t):
      if arm[s]==i:
        Qt[i]+=reward[s]
    Qt[i]=Qt[i]/Nt[i]
  ucb=Qt=np.zeros(len(Qt))
  for a in range(len(Qt)):
    ucb[a]=Qt[a]+np.sqrt(np.log(t)/Nt[a])
  At=np.argmax(ucb)
  arm=np.append(arm,np.array([At]))
  reward=np.append(reward,np.array([multi_arm.generate_reward(At)]))
  return At,arm,reward

print("Arm to be chosen at 11th trial with UCB approach: ",ucb(arm,reward,no_of_arms))

"""# Graph"""

def incremental_avg(arr):
  avg=[]
  Q=0
  for x in range(len(arr)):
    Q=Q+(arr[x]-Q)/(x+1)
    avg.append(Q)
  return avg

#greedy
arm_greedy=arm.copy()
reward_greedy=reward.copy()
turns=500
for x in range(turns):
  At,arm_greedy,reward_greedy = epsilon_greedy(arm_greedy,reward_greedy,0,no_of_arms)
inc_avg_greedy=incremental_avg(reward_greedy[10:])
print(inc_avg_greedy)

#e-greedy
arm_egreedy=arm.copy()
reward_egreedy=reward.copy()
turns=500
for x in range(turns):
  At,arm_egreedy,reward_egreedy = epsilon_greedy(arm_egreedy,reward_egreedy,0.25,no_of_arms)
inc_avg_egreedy=incremental_avg(reward_egreedy[10:])
print(inc_avg_egreedy)

#ucb
arm_ucb=arm.copy()
reward_ucb=reward.copy()
turns=500
for x in range(turns):
  At,arm_ucb,reward_ucb = ucb(arm_ucb,reward_ucb,no_of_arms)
inc_avg_ucb=incremental_avg(reward_ucb[10:])
print(inc_avg_ucb)

f = plt.figure()
f.set_figwidth(10)
f.set_figheight(10)

plt.plot(range(len(inc_avg_egreedy)),inc_avg_egreedy, label ='Epsilon Greedy')
plt.plot(range(len(inc_avg_greedy)),inc_avg_greedy, label ='Greedy')
plt.plot(range(len(inc_avg_ucb)),inc_avg_ucb,label="UCB1")
plt.xlabel("No of turns")
plt.ylabel("Avg_rewards")
plt.legend()
plt.title('Comparing greedy, epsilon-greedy and UCB1')
plt.show()

"""#PAC optimality"""

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

"""# Median Elimination"""

def median_elim_PAC(epsilon,delta,bandit):
  S_l=set(range(bandit.n))
  epsilon_l=epsilon/4
  delta_l=delta/2
  while len(S_l)!=1:
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