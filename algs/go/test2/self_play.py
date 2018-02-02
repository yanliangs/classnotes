import os, glob, pickle
import json
import re
import numpy as np
from shutil import copy
from ai import MCTSPlayer
import go
from policy_value import PolicyValue
from util import flatten_idx, pprint_board


def self_play_and_save(player, opp_player, boardsize, mock_state=[]):    
    '''Run num_games games to completion, keeping track of each position
    and move of the new_player.  And save the game data

    '''
    state_list = []
    pi_list = []
    player_list = []

    board_size = boardsize
    state = go.GameState(size=board_size, komi=0)

    # Allowing injection of a mock state object for testing purposes
    if mock_state:
        state = mock_state

    player_color = go.BLACK
    current = player
    other = opp_player

    step = 0
    while not state.is_end_of_game:
        move = current.get_move(state, self_play=True)

        #print(move)
        childrens = current.mcts._root._children.items()
        #print(childrens)
        actions, next_states = map(list, zip(*childrens))
        _n_visits = [next_state._n_visits for next_state in next_states]
        if not move == go.PASS_MOVE:
            if step < 25: # temperature is considered to be 1
                distribution = np.divide(_n_visits, np.sum(_n_visits))
            else:
                max_visit_idx = np.argmax(_n_visits)
                distribution = np.zeros(np.shape(_n_visits))
                distribution[max_visit_idx] = 1.0
        else: # to prevent the model from overfitting to PASS_MOVE
            distribution = np.zeros(np.shape(_n_visits))
        pi = zip(actions, distribution)
        #print(zip(actions, _n_visits))
        state_list.append(state)
        pi_list.append(pi)

        current.mcts.update_with_move(move)
        state.do_move(move)
        other.mcts.update_with_move(move)
        current, other = other, current
        step += 1

        #pprint_board(state.board)

    winner = state.get_winner()
    #print(winner)
    if winner == go.BLACK:
        reward_list = [(-1.)**j for j in range(len(state_list))]
    else : # winner == go.WHITE:
        reward_list = [(-1.)**(j+1) for j in range(len(state_list))]
    return state_list, pi_list, reward_list

def run_self_play(cmd_line_args=None):
    while True:
        # Set initial conditions
        policy = PolicyValue()

        boardsize = 9
        # different opponents come from simply changing the weights of 'opponent.policy.model'. That
        # is, only 'opp_policy' needs to be changed, and 'opponent' will change.
        opp_policy = PolicyValue()

        for i in range(10):
            print(str(i) + "th self playing game")
            player = MCTSPlayer(policy.eval_value_state, policy.eval_policy_state, n_playout=10, evaluating=False, self_play=True)
            opp_player= MCTSPlayer(opp_policy.eval_value_state, opp_policy.eval_policy_state, n_playout=10, evaluating=False, self_play=True)
            state_list, pi_list, reward_list = self_play_and_save(opp_player, player, boardsize)
            data_to_save["state"] = state_list
            data_to_save["pi"] = pi_list
            data_to_save["reward"] = reward_list
            del player
            del opp_player
        metadata["self_play_model"] += [best_weight_path]
        save_metadata()
        del policy
        del opp_policy

if __name__ == '__main__':
    run_self_play()
