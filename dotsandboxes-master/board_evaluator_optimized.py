import numpy as np

def user_action(move, cur_player, points, boxes):
    # boxes is numpy matrix
    points_made = check_boxes(move, boxes)
    points[cur_player-1] += points_made
    won_cell = False

    if points_made == 0:
        next_player = 3 - cur_player
    else:
        next_player = cur_player
        won_cell = True
    return next_player, won_cell


def check_boxes(move, boxes):
    r, c, o = move
    shape = boxes.shape
    points_made = 0
    if r < shape[0] and c < shape[1]:
        boxes[r, c] += 1
        if boxes[r, c] == 4:
            won_cell = True
            points_made += 1

    if o == 'h' and r >= 1:
        boxes[r - 1, c] += 1
        if boxes[r - 1, c] == 4:
            won_cell = True
            points_made += 1
    elif o == 'v' and c >= 1:
        boxes[r, c - 1] += 1
        if boxes[r, c - 1] == 4:
            won_cell = True
            points_made += 1
    return points_made
