import numpy as np

def user_action(move, cur_player, points, boxes):
    # boxes is numpy matrix
    r, c, o = move
    won_cell = False

    boxes[r, c] += 1
    if boxes[r, c] == 4:
        won_cell = True
        points[cur_player] += 1

    if o == 'h' and r >= 1:
        boxes[r-1, c] += 1
        if boxes[r-1, c] == 4:
            won_cell = True
            points[cur_player] += 1
    elif c >= 1:
        boxes[r, c-1] += 1
        if boxes[r, c-1] == 4:
            won_cell = True
            points[cur_player] += 1

    if not won_cell:
        next_player = 3 - cur_player
    else:
        next_player = cur_player
    return next_player, won_cell