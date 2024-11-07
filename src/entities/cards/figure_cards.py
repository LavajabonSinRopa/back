HARD_FIGURE_SZ = 5

EASY_FIGURE_SZ = 4

#all squares needed to form a figure
#to add a new figure choose one of its squares as [0,0] and write it in the corresponding list below. Then call main and copypaste the resulting hard_figures and easy figures
figure_card_types_hard = [
    [[0,-1],[0,0],[-1,-1],[1,-1],[0,1]],
    [[0,0],[0,1],[1,1],[1,2],[1,3]],
    [[0,0],[0,-1],[1,-1],[1,-2],[1,-3]],
    [[0,0],[1,0],[1,1],[2,1],[2,2]],
    [[0,0],[0,1],[0,2],[0,3],[0,4]],
    [[0,0],[1,0],[2,0],[2,1],[2,2]],
    [[0,0],[0,1],[0,2],[0,3],[1,3]],
    [[0,0],[0,1],[0,2],[0,3],[-1,3]],
    [[0,0],[0,1],[0,2],[1,1],[-1,2]],
    [[0,0],[1,0],[1,-1],[1,-2],[2,-2]],
    [[0,0],[1,0],[1,1],[2,1],[1,2]],
    [[0,0],[1,0],[1,1],[1,2],[2,2]],
    [[0,0],[0,1],[0,2],[0,3],[1,2]],
    [[0,0],[0,1],[0,2],[0,3],[-1,2]],
    [[0,0],[0,1],[0,2],[-1,1],[-1,2]],
    [[0,0],[0,1],[-1,0],[0,2],[-1,2]],
    [[0,0],[0,1],[1,0],[-1,0],[0,-1]],
    [[0,0],[0,1],[0,2],[1,1],[1,2]]
    ]

figure_card_types_easy = [
    [[0,0],[0,1],[-1,1],[-1,2]],
    [[0,0],[0,1],[-1,0],[-1,1]],
    [[0,0],[0,1],[1,1],[1,2]],
    [[0,0],[0,1],[0,2],[-1,1]],
    [[0,0],[0,1],[0,2],[1,2]],
    [[0,0],[0,1],[0,2],[0,3]],
    [[0,0],[0,1],[0,2],[-1,2]]
]

#INCLUDES ALL ROTATIONS NORMALIZED
hard_cards = [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]],
[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]],
[[0, 0], [0, 1], [0, 2], [0, 3], [1, 0]],
[[0, 0], [0, 1], [0, 2], [0, 3], [1, 1]],
[[0, 0], [0, 1], [0, 2], [0, 3], [1, 2]],
[[0, 0], [0, 1], [0, 2], [0, 3], [1, 3]],
[[0, 0], [0, 1], [0, 2], [1, -1], [1, 0]],
[[0, 0], [0, 1], [0, 2], [1, 0], [1, 1]],
[[0, 0], [0, 1], [0, 2], [1, 0], [1, 2]],
[[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]],
[[0, 0], [0, 1], [0, 2], [1, 1], [1, 2]],
[[0, 0], [0, 1], [0, 2], [1, 1], [2, 1]],
[[0, 0], [0, 1], [0, 2], [1, 2], [1, 3]],
[[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]],
[[0, 0], [0, 1], [1, -2], [1, -1], [1, 0]],
[[0, 0], [0, 1], [1, -1], [1, 0], [1, 1]],
[[0, 0], [0, 1], [1, -1], [1, 0], [2, -1]],
[[0, 0], [0, 1], [1, -1], [1, 0], [2, 0]],
[[0, 0], [0, 1], [1, 0], [1, 1], [1, 2]],
[[0, 0], [0, 1], [1, 0], [1, 1], [2, 0]],
[[0, 0], [0, 1], [1, 0], [1, 1], [2, 1]],
[[0, 0], [0, 1], [1, 0], [2, -1], [2, 0]],
[[0, 0], [0, 1], [1, 0], [2, -1], [2, 0]],
[[0, 0], [0, 1], [1, 0], [2, 0], [2, 1]],
[[0, 0], [0, 1], [1, 0], [2, 0], [3, 0]],
[[0, 0], [0, 1], [1, 1], [1, 2], [1, 3]],
[[0, 0], [0, 1], [1, 1], [1, 2], [2, 1]],
[[0, 0], [0, 1], [1, 1], [1, 2], [2, 2]],
[[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]],
[[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]],
[[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]],
[[0, 0], [0, 1], [1, 1], [2, 1], [3, 1]],
[[0, 0], [0, 2], [1, 0], [1, 1], [1, 2]],
[[0, 0], [1, -3], [1, -2], [1, -1], [1, 0]],
[[0, 0], [1, -2], [1, -1], [1, 0], [1, 1]],
[[0, 0], [1, -2], [1, -1], [1, 0], [2, -2]],
[[0, 0], [1, -2], [1, -1], [1, 0], [2, -2]],
[[0, 0], [1, -2], [1, -1], [1, 0], [2, -1]],
[[0, 0], [1, -2], [1, -1], [1, 0], [2, 0]],
[[0, 0], [1, -1], [1, 0], [1, 1], [1, 2]],
[[0, 0], [1, -1], [1, 0], [1, 1], [2, -1]],
[[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]],
[[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]],
[[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]],
[[0, 0], [1, -1], [1, 0], [1, 1], [2, 0]],
[[0, 0], [1, -1], [1, 0], [1, 1], [2, 1]],
[[0, 0], [1, -1], [1, 0], [2, -2], [2, -1]],
[[0, 0], [1, -1], [1, 0], [2, -1], [2, 0]],
[[0, 0], [1, -1], [1, 0], [2, -1], [3, -1]],
[[0, 0], [1, -1], [1, 0], [2, 0], [2, 1]],
[[0, 0], [1, -1], [1, 0], [2, 0], [3, 0]],
[[0, 0], [1, 0], [1, 1], [1, 2], [1, 3]],
[[0, 0], [1, 0], [1, 1], [1, 2], [2, 0]],
[[0, 0], [1, 0], [1, 1], [1, 2], [2, 1]],
[[0, 0], [1, 0], [1, 1], [1, 2], [2, 2]],
[[0, 0], [1, 0], [1, 1], [1, 2], [2, 2]],
[[0, 0], [1, 0], [1, 1], [2, -1], [2, 0]],
[[0, 0], [1, 0], [1, 1], [2, 0], [2, 1]],
[[0, 0], [1, 0], [1, 1], [2, 0], [3, 0]],
[[0, 0], [1, 0], [1, 1], [2, 1], [2, 2]],
[[0, 0], [1, 0], [1, 1], [2, 1], [3, 1]],
[[0, 0], [1, 0], [2, -2], [2, -1], [2, 0]],
[[0, 0], [1, 0], [2, -1], [2, 0], [2, 1]],
[[0, 0], [1, 0], [2, -1], [2, 0], [3, -1]],
[[0, 0], [1, 0], [2, -1], [2, 0], [3, 0]],
[[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],
[[0, 0], [1, 0], [2, 0], [2, 1], [3, 0]],
[[0, 0], [1, 0], [2, 0], [2, 1], [3, 1]],
[[0, 0], [1, 0], [2, 0], [3, -1], [3, 0]],
[[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]],
[[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
[[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
]

easy_cards = [[[0, 0], [0, 1], [0, 2], [0, 3]],
[[0, 0], [0, 1], [0, 2], [0, 3]],
[[0, 0], [0, 1], [0, 2], [1, 0]],
[[0, 0], [0, 1], [0, 2], [1, 1]],
[[0, 0], [0, 1], [0, 2], [1, 2]],
[[0, 0], [0, 1], [1, -1], [1, 0]],
[[0, 0], [0, 1], [1, -1], [1, 0]],
[[0, 0], [0, 1], [1, 0], [1, 1]],
[[0, 0], [0, 1], [1, 0], [1, 1]],
[[0, 0], [0, 1], [1, 0], [1, 1]],
[[0, 0], [0, 1], [1, 0], [1, 1]],
[[0, 0], [0, 1], [1, 0], [2, 0]],
[[0, 0], [0, 1], [1, 1], [1, 2]],
[[0, 0], [0, 1], [1, 1], [1, 2]],
[[0, 0], [0, 1], [1, 1], [2, 1]],
[[0, 0], [1, -2], [1, -1], [1, 0]],
[[0, 0], [1, -1], [1, 0], [1, 1]],
[[0, 0], [1, -1], [1, 0], [2, -1]],
[[0, 0], [1, -1], [1, 0], [2, -1]],
[[0, 0], [1, -1], [1, 0], [2, 0]],
[[0, 0], [1, 0], [1, 1], [1, 2]],
[[0, 0], [1, 0], [1, 1], [2, 0]],
[[0, 0], [1, 0], [1, 1], [2, 1]],
[[0, 0], [1, 0], [1, 1], [2, 1]],
[[0, 0], [1, 0], [2, -1], [2, 0]],
[[0, 0], [1, 0], [2, 0], [2, 1]],
[[0, 0], [1, 0], [2, 0], [3, 0]],
[[0, 0], [1, 0], [2, 0], [3, 0]],
]

def print_figure(card):
    board = []
    for i in range(2*HARD_FIGURE_SZ):
        board.append([])
        for j in range(2*HARD_FIGURE_SZ):
            board[i].append('*')
    for square in card:
        board[square[0]+HARD_FIGURE_SZ][square[1]+HARD_FIGURE_SZ] = '#'
    for col in board:
        print(col)

def normalize_card(card):
    if(len(card)==0):
        return card
    card = sorted(card)
    x,y = card[0][0],card[0][1]
    nor_card = []
    for square in card:
        nor_card.append([square[0]-x,square[1]-y])
    return nor_card

def rotate_card(card):
    rot_card = []
    for square in card:
        rot_card.append([-square[1], square[0]])
    return rot_card

def generate_cards():
    easy_cards = []
    for card_type in figure_card_types_easy:
        card = normalize_card(card_type)
        easy_cards.append(card)
        for rotation in range(3):
            card = rotate_card(card)
            card = normalize_card(card)
            easy_cards.append(card)
    easy_cards = sorted(easy_cards)

    hard_cards = []
    for card_type in figure_card_types_hard:
        card = normalize_card(card_type)
        hard_cards.append(card)
        for rotation in range(3):
            card = rotate_card(card)
            card = normalize_card(card)
            hard_cards.append(card)
    hard_cards = sorted(hard_cards)

    print("hard_cards = [",end='')
    for card in hard_cards:
        print(card, end='')
        print(',')
    print("]")
    print("easy_cards = [",end='')
    for card in easy_cards:
        print(card, end='')
        print(',')
    print("]")

#RETURN TRUE IF FIGURE EXISTS in O(log(len(hard_cards))*HARD_FIGURE_SZ)
def figure_exists(card):
    card = normalize_card(card)
    if(len(card) == EASY_FIGURE_SZ):
        l,r = 0,len(easy_cards)-1
        while(l+1<r):
            m = (l+r)//2
            if(easy_cards[m]<card):
                l = m
            else:
                r = m
        return easy_cards[l+1] == card
    elif(len(card) == HARD_FIGURE_SZ):
        l,r = 0,len(hard_cards)-1
        while(l+1<r):
            m = (l+r)//2
            if(hard_cards[m]<card):
                l = m
            else:
                r = m
        return hard_cards[l+1] == card
    return False

def figure_matches_type(figure_type, figure):
    figure = normalize_card(figure)
    # assuming easy figures from 0.., hard from len(easy)..
    if figure_type < len(figure_card_types_easy):
        possible_match = normalize_card(figure_card_types_easy[figure_type])
    else:
        figure_type -= len(figure_card_types_easy)
        if figure_type >= len(figure_card_types_hard):
            return False
        possible_match = normalize_card(figure_card_types_hard[figure_type])

    if figure == possible_match:
        return True
    for rotation in range(3):
        possible_match = normalize_card(rotate_card(possible_match))
        if figure == possible_match:
            return True

    return False

if __name__ == "__main__":
    #printea las figuras en el orden de su codigo
    code = 0
    for card in figure_card_types_easy:
        print("code = ", code)
        code += 1
        print_figure(card)
        print("--------------")
    for card in figure_card_types_hard:
        print("code = ", code)
        code += 1
        print_figure(card)
        print("--------------")
    #generate_cards()
    