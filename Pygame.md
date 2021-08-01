# Pygame



安装

`sudo python3 -m pip install pygame==2.0.0.dev6 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com`







玩具代码



```python
import pygame

pygame.init()



w,h=500,500
pygame.display.set_mode((w,h))
screen=pygame.display.get_surface()
#载入背景图并缩放到宽高
bgpic=pygame.image.load('bgpic.png')
bgpic=pygame.transform.scale(bgpic,(w,h))
#载入超级玛丽图
mario_game=pygame.image.load('mario.png')

#创建精灵
mario=pygame.sprite.Sprite()
mario.image=mario_image
mario.rect=mario.image.get_rect()
mario.rect.x, mario.rect.y=w/2, h/2

#玩家组
player_group=pygame.sprite.Group()
play_group.add(mario)

#开始游戏
while True:
	#更新部分
	for event in pygame.event_get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_DOWN]:
				mario.rect.y+=10
			if keys[pygame.K_UP]:
				mario.rect.y-=10
	#画图部分
	screen.blit(bgpic,(0,0))
	player_group.draw(screen)
	pygame.display.update()
```

