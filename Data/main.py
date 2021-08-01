#游戏主要入口

from source.states import  main_menu,load_screen,level
from source import tools , setup

def main():
    state_dict={
        'main_menu':main_menu.MainMenu(),
        'load_screen':load_screen.LoadScreen(),
        'level':level.Level(),
        'game_over': load_screen.GameOver()
    }
    game=tools.Game(state_dict, 'main_menu')
    #state=main_menu.MainMenu()
    #state = load_screen.LoadScreen()
    #state=level.Level()
    game.run()

if __name__=="__main__":
    main()













