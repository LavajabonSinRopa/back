#all squares needed to form a figure
#to check if a set of squares matches, sort and match the first remembering the diference in x and y. Check if all other squares given -<dx,dy> match as well
#TODO: complete for all cardtypes
figure_card_hard_types = [[[0,-1],[0,0],[-1,-1],[1,-1],[0,1]],
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
                     ]