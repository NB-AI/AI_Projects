"""
Assignment 04 - q_learning
"""

from .. environment import Environment, Outcome
import numpy as np


def eps_greedy(rng, qs, epsilon):
    # this function makes an epsilon greedy decision

    if rng.uniform(0, 1) < epsilon:
        # - with p == epsilon, an action is chosen uniformly at random

        action = rng.randint(0, len(qs))

    else:
        # - with p == 1 - epsilon, the action
        #   having the currently largest q-value estimate is chosen
        #max_tuple = max(zip(qs.values(), qs.keys())) # qs is Q[s] and thats a dictionary with four entries for four actions with their values
        # Now we get the tuple with the biggest value. The d.values() is standing first because the max() is refering to the first
        # element in the tuple. So we get the highest values with the corresponding action/key
        # This way of solution doesn't work because when all q_values are the same it chooses the last one where as your
        # solution expects the first one.
        #action = max_tuple[1]

        first_call = True
        for d,e in zip(qs.values(), qs.keys()):
            if first_call == True:
                first_max = d
                action = e
                first_call = False
            elif first_max < d:
                first_max = d
                action = e

    return action


class QLearning():
    def train(self, env: Environment):
        ########################################
        # please leave untouched
        rng = np.random.RandomState(1234)
        alpha = 0.2
        epsilon = 0.3
        gamma = env.get_gamma()
        n_episodes = 10000
        ########################################

        ########################################
        # initialize the 'table'
        Q = dict()
        for s in range(env.get_n_states()):
            Q[s] = dict()
            for a in range(env.get_n_actions()):
                Q[s][a] = 0.
        ########################################

        # TODO #################################
        for episode in range(1, n_episodes + 1):
            # TODO, exercise 4, generate an episode
            # with an eps_greedy policy, and then
            # implement the q-learning update here

            # you interact with the environment
            # ONLY via the methods
            #      'state = env.reset()'
            # and
            #      'state, reward, done = env.step(action)'
            #
            # 'state = env.reset()' is used to
            # reset the environment at the start
            # of an episode
            #
            # 'state, reward, done = env.step(action)'
            # is used to tell the environment that your
            # agent has decided to do 'action'.
            # the environment will then tell you, in
            # which state you actually ended up in,
            # what the immediate reward was, and whether
            # or not the episode ended.
            state = env.reset()
            done = False
            while done == False:
                 action = eps_greedy(rng, Q[state], epsilon)
                 new_state, reward, done = env.step(action)

                 # also implement qlearning update here:
                 old_value = Q[state][action]
                 max_value_next_state = max(Q[new_state].values())
                 new_value = old_value + alpha * (reward + (gamma * max_value_next_state) - old_value)

                 Q[state][action] = new_value  # update Q table
                 state = new_state


        ########################################

        ########################################
        # this computes a deterministic policy
        # from the Q value function
        # along the way, we compute V, the
        # state value function as well
        policy = dict()
        V = dict()
        for s, qs in Q.items():
            policy[s] = dict()
            V[s] = 0.
            best_a = None
            best_q = float('-Inf')
            for a, q in qs.items():
                if q > best_q:
                    best_q = q
                    best_a = a

            # how good is it to be in state 's'?
            # if we take the best action, we can expect to get 'best_q'
            # future reward. hence, being in state V[s] we can expect
            # the same amount of reward ...
            V[s] = best_q
            for a in qs.keys():
                if a == best_a:
                    policy[s][a] = 1.
                else:
                    policy[s][a] = 0.
        ########################################

        return Outcome(n_episodes, policy, V=V, Q=Q)
