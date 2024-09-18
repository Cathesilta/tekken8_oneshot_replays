import os

# def singleton(cls):
#     instances = {}
#     def get_instances(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]
#     return get_instances
            


# @singleton
class hyperparameters():
    
    ### Game Info
    Game = 'SF6'                       
    # Game = 'Tekken8'                    # option: only 'SF6' or 'Tekken8'
    # Match information
    character_1 = ''
    character_2 = ''
    player_1 = ''
    player_2 = ''
    useocr = False
    scoreboard = []         # if useocr == False, you must read who wins, [2,1,2] means player2 won the 1st and 3rd match
    P1_title = ''                       #player 1 title
    p1_character = ''
    P1_control_type = ''
    P2_title = ''
    p2_character = ''
    P2_control_type = ''
    
    
    
    #--------------------------------------------------------------------------------------------