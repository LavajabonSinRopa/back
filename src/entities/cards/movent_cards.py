#defined as tuples. If standing at position <i,j> card [x,y] can move to: <i+x,j+y>, <i+y,j-x>, <i-x,j-y>, <i-y,j+x> 
movement_card_types = [[2,2],[2,0],[1,0],[1,1],[2,-1],[2,1],[4,0]]

def rotate_90(x,y):
    return [-y,x]

def can_move_to(from_x, from_y, to_x, to_y, card_type):
    movement_type = movement_card_types[card_type]
    for rotation in range(4):
        if to_x == from_x + movement_type[0] and to_y == from_y + movement_type[1]:
            return True
        movement_type = rotate_90(movement_type[0],movement_type[1])
    return False
