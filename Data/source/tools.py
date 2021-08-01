#工具和游戏主控
import pygame
import random
import os


class Game:
    def __init__(self, state_dict, start_state):
        #pygame.init()
        #pygame.display.set_mode((800,600))
        self.screen=pygame.display.get_surface()
        self.clock=pygame.time.Clock()#计时加控制帧数
        self.keys = pygame.key.get_pressed()
        self.state_dict=state_dict
        self.state=state_dict[start_state]
    
    def update(self):
        if self.state.finished:
            game_info=self.state.game_info
            next_state=self.state.next
            self.state.finished=False
            self.state=self.state_dict[next_state]
            self.state.start(game_info)
        else:
            self.state.update(self.screen, self.keys)


    
    def run(self):
        #GRAPHICS = tools.load_graphics('Data/resources/graphics')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
            #self.screen.fill((random.randint(0,255), random.randint(0,255) ,random.randint(0,255)))
            #image = get_image(GRAPHICS['mario_bros'], 145,32,16,16,(0 ,0 ,0), 5)
            #左上角x,y，宽，高，抠图底色，放大倍数
            #self.screen.blit(image,(300,300))
            #state.update(self.screen, self.keys)
            self.update()

            pygame.display.update()
            self.clock.tick(60)#计时加控制帧数


def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):
    graphics={}
    for pic in os.listdir(path):
        name ,extension = os.path.splitext(pic)
        if extension.lower() in accept:
            img=pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img=img.convert_alpha()
            else:
                img=img.convert()
            graphics[name]=img
    return graphics

def get_image(sheet, x ,y, width, height, colorkey, scale):
    image=pygame.Surface((width, height))
    image.blit(sheet, (0,0), (x,y,width,height))#0,0表示画到哪个位置，x,y,w,h代表sheet里哪个区域要取出来
    image.set_colorkey(colorkey)
    image=pygame.transform.scale(image, (int(width*scale),int(height*scale)))
    return image






