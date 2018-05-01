import numpy as np

def user_action(move, cur_player, cells, points):
    r, c, o = move
    nb_rows = np.shape(cells)[0]-1
    nb_cols = np.shape(cells)[1]-1

    next_player = cur_player
    won_cell = False
    cell = cells[r][c]
    if o == "h":
        if cell["h"] != 0:
            return cur_player
        cell["h"] = cur_player
        # Above
        if r > 0:
            if cells[r - 1][c]["v"] != 0 \
                and cells[r - 1][c + 1]["v"] != 0 \
                and cells[r - 1][c]["h"] != 0 \
                and cells[r][c]["h"] != 0:
                won_cell = True
                points[cur_player-1] += 1
                cells[r - 1][c]["p"] = cur_player
        # Below
        if r < nb_rows and c < nb_cols:
            if cells[r][c]["v"] != 0 \
                and cells[r][c + 1]["v"] != 0 \
                and cells[r][c]["h"] != 0 \
                and cells[r + 1][c]["h"] != 0:
                won_cell = True
                points[cur_player-1] += 1
                cells[r][c]["p"] = cur_player

    if o == "v":
        if cell["v"] != 0:
            return cur_player
        cell["v"] = cur_player;
        # Left
        if c > 0:
            if cells[r][c - 1]["v"] != 0 \
                and cells[r][c]["v"] != 0 \
                and cells[r][c - 1]["h"] != 0 \
                and cells[r + 1][c - 1]["h"] != 0:
                won_cell = True
                points[cur_player-1] += 1
                cells[r][c - 1]["p"] = cur_player
        # Right
        if c < nb_cols and r < nb_rows:
            if cells[r][c]["v"] != 0 \
                and cells[r][c + 1]["v"] != 0 \
                and cells[r][c]["h"] != 0 \
                and cells[r + 1][c]["h"] != 0:
                won_cell = True
                points[cur_player-1] += 1
                cells[r][c]["p"] = cur_player

    if not won_cell:
        next_player = 3 - cur_player
    else:
        next_player = cur_player
    return next_player, won_cell