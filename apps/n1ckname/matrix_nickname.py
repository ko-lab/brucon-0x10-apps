import nvs
from .messages import kolab_message
from .matrixanimation import MatrixAnimation
def main():
    # kolab_game_state = nvs.get_str("system", 'kolab_game_state')
    kolab_game_state='won'
    nickname = nvs.get_str("system", 'nickname')

   #  if kolab_game_state == 'lost':
   #      nickname = 'Loser'
   #
   # elif kolab_game_state != 'won':
   #      nickname = 'Ko-Lab'
   #  gif, pos, size,  frames = calc_matrix_gif()
   #  rgb.gif(gif, pos, size, frames)
   #  rgb.text(nickname)
    MatrixAnimation(None).show_loop()

def calc_matrix_gif():
    frames = 5
    gifdata =[]
    for i in range(frames):
       gifdata = gifdata + get_matrix_frame(i)
    return gifdata, (0,0), (32, 19), frames

def get_matrix_frame(i):
    cyan_columns = calc_cyan_columns()
    return buffer_matrix_frame(cyan_columns)