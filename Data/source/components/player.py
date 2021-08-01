import pygame
from ..  import tools,setup
from .. import constants
from ..components import powerup
import os
import json

class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def load_data(self):
        file_name=self.name+'.json'
        file_name=os.path.join('source/data/player', file_name)
        with open(file_name) as f:
            self.player_data = json.load(f)

    def setup_states(self):
        self.state='stand'
        self.face_right=True
        self.dead=False
        self.big=False
        self.fire=False
        self.can_shoot=True
        self.can_jump=True
        self.hurt_immune=False

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_velo=0
        self.y_velo=0

        self.max_walk_velo=speed['max_walk_speed']
        self.max_run_velo=speed['max_run_speed']
        self.max_y_velo=speed['max_y_velocity']
        self.jump_velo=speed['jump_velocity']
        self.walk_accel=speed['walk_accel']
        self.run_accel=speed['run_accel']
        self.turn_accel=speed['turn_accel']
        self.gravity=constants.GRAVITY
        self.anti_gravity=constants.ANTI_GRAVITY

        self.max_x_velo=self.max_walk_velo
        self.x_accel=self.walk_accel

    def setup_timers(self):
        self.walking_timer=0
        self.transition_timer=0
        self.death_timer=0
        self.hurt_immune_timer=0
        self.last_fireball_timer=0

    def load_images(self):
        sheet=setup.GRAPHICS['mario_bros']
        frame_rects=self.player_data['image_frames']

        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames=[self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames=[self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames=[self.right_big_fire_frames, self.left_big_fire_frames]


        self.all_frames=[
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames
        ]

        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image=tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'], frame_rect['height'], (0,0,0),constants.PLAYER_MULTI)
                left_image=pygame.transform.flip(right_image, True, False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)




        self.frame_index=0
        self.frames = self.right_frames
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_rect()


    def update(self, keys,level):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys,level)
        self.is_hurt_immune()

    def handle_states(self,keys,level):
        self.can_jump_or_not(keys)
        self.can_shoot_or_not(keys)
        if self.state == 'stand':
            self.stand(keys, level)
        elif self.state == 'walk':
            self.walk(keys,level)
        elif self.state == 'jump':
            self.jump(keys,level)
        elif self.state == 'fall':
            self.fall(keys,level)
        elif self.state == 'die':
            self.die(keys)
        elif self.state == 'small2big':
            self.small2big(keys)
        elif self.state == 'big2small':
            self.big2small(keys)
        elif self.state == 'big2fire':
            self.big2fire(keys)
        
        if self.face_right:
            self.image=self.right_frames[self.frame_index]
        else :
            self.image=self.left_frames[self.frame_index]


    def can_jump_or_not(self, keys):
        if not keys[pygame.K_a]:
            self.can_jump = True
    def can_shoot_or_not(self, keys):
        if not keys[pygame.K_s]:
            self.can_shoot = True

    def stand(self, keys,level):
        self.frame_index=0
        self.x_velo=0
        self.y_velo=0
        if keys[pygame.K_RIGHT]:
            self.face_right=True
            self.state='walk'
        elif keys[pygame.K_LEFT]:
            self.face_right=False
            self.state='walk'
        elif keys[pygame.K_a] and self.can_jump:
            self.state='jump'
            self.y_velo=self.jump_velo
        elif keys[pygame.K_s] :
            if self.fire and  self.can_shoot:
                self.shoot_fireball(level)
        
    def walk(self, keys,level):
        if keys[pygame.K_s]:
            self.max_x_velo = self.max_run_velo
            self.x_accel=self.run_accel
            if self.fire and  self.can_shoot:
                self.shoot_fireball(level)
        else:
            self.max_x_velo = self.max_walk_velo
            self.x_accel=self.walk_accel

        if keys[pygame.K_a] and self.can_jump:
            self.state='jump'
            self.y_velo=self.jump_velo

        if self.current_time - self.walking_timer> self.calc_frame_duration():
            if self.frame_index<3:
                self.frame_index+=1
            else:
                self.frame_index=1
            self.walking_timer=self.current_time
        if keys[pygame.K_RIGHT]:
            self.face_right=True
            if self.x_velo<0:
                self.frame_index=5
                self.x_accel=self.turn_accel
            self.x_velo=self.calc_velo(self.x_velo, self.x_accel, self.max_x_velo, True)
        elif keys[pygame.K_LEFT]:
            self.face_right=False
            if self.x_velo>0:
                self.frame_index=5#刹车帧
                self.x_accel=self.turn_accel
            self.x_velo=self.calc_velo(self.x_velo, self.x_accel, self.max_x_velo, False)
        else:
            if  self.face_right:
                self.x_velo -= self.x_accel
                if self.x_velo<0:
                    self.x_velo=0
                    self.state = 'stand'
            else:
                self.x_velo+=self.x_accel
                if self.x_velo>0:
                    self.x_velo=0
                    self.state = 'stand'

    def jump(self, keys,level):
        self.frame_index =4 
        self.y_velo+=self.anti_gravity
        self.can_jump = False

        if self.y_velo >=0:
            self.state = 'fall'
        if keys[pygame.K_RIGHT]:
            self.x_velo=self.calc_velo(self.x_velo, self.x_accel, self.max_x_velo, True)
        elif keys[pygame.K_LEFT]:
            self.x_velo=self.calc_velo(self.x_velo, self.x_accel, self.max_x_velo, False)
        elif keys[pygame.K_s]:
            if self.fire and  self.can_shoot:
                self.shoot_fireball(level)
        
        if not keys[pygame.K_a]:
            self.state = 'fall'

    def fall(self,keys,level):
        self.y_velo  = self.calc_velo(self.y_velo, self.gravity, self.max_y_velo)
        
        if keys[pygame.K_RIGHT]:
            self.x_velo=self.calc_velo(self.x_velo, self.x_accel, self.max_x_velo, True)
        elif keys[pygame.K_LEFT]:
            self.x_velo=self.calc_velo(self.x_velo, self.x_accel, self.max_x_velo, False)
        elif keys[pygame.K_s]:
            if self.fire and  self.can_shoot:
                self.shoot_fireball(level)
        if not keys[pygame.K_a]:
            self.state='fall'


    def die(self, keys):
        self.rect.y+=self.y_velo
        self.y_velo=self.anti_gravity

    def go_die(self):
        self.dead=True
        self.y_velo=self.jump_velo
        self.frame_index=6
        self.state='die'
        self.death_timer=self.current_time

    def small2big(self, keys):
        frame_duration=65
        sizes=[1,0,1,0,1,2,0,1,2,0,2]#0 small 1medium 2 big
        frames_and_index=[(self.small_normal_frames, 0), (self.small_normal_frames,7), (self.big_normal_frames, 0)]
        if self.transition_timer==0:
            self.big=True
            self.transition_timer= self.current_time
            self.changing_index=0
        elif self.current_time - self.transition_timer>frame_duration:
            self.transition_timer= self.current_time
            frames,index=frames_and_index[sizes[self.changing_index]]
            self.change_player_image(frames,index)
            self.changing_index+=1
            if self.changing_index==len(sizes):
                self.transition_timer=0
                self.state='walk'
                self.right_frames=self.right_big_normal_frames
                self.left_frames=self.left_big_normal_frames
            
    def big2small(self, keys):
        frame_duration=65
        sizes=[2,1,0,1,0,1,0,1,0,1,0]#0 small 1medium 2 big
        frames_and_index=[(self.small_normal_frames, 8), (self.big_normal_frames,8), (self.big_normal_frames, 4)]
        if self.transition_timer==0:
            self.big=False
            self.transition_timer= self.current_time
            self.changing_index=0
        elif self.current_time - self.transition_timer>frame_duration:
            self.transition_timer= self.current_time
            frames,index=frames_and_index[sizes[self.changing_index]]
            self.change_player_image(frames,index)
            self.changing_index+=1
            if self.changing_index==len(sizes):
                self.transition_timer=0
                self.state='walk'
                self.right_frames=self.right_small_normal_frames
                self.left_frames=self.left_small_normal_frames
    
    def big2fire(self, keys):
        frame_duration=65
        sizes=[0,1,0,1,0,1,0,1,0,1,0]#0 small 1medium 2 big
        frames_and_index=[(self.big_fire_frames,3), (self.big_fire_frames,3)]
        if self.transition_timer==0:
            self.fire=True
            self.transition_timer= self.current_time
            self.changing_index=0
        elif self.current_time - self.transition_timer>frame_duration:
            self.transition_timer= self.current_time
            frames,index=frames_and_index[sizes[self.changing_index]]
            self.change_player_image(frames,index)
            self.changing_index+=1
            if self.changing_index==len(sizes):
                self.transition_timer=0
                self.state='walk'
                self.right_frames=self.right_big_fire_frames
                self.left_frames=self.left_big_fire_frames
    
    def change_player_image(self, frames, index):
        self.frame_index = index
        if self.face_right:
            self.right_frames=frames[0]
            self.image=self.right_frames[self.frame_index]
        else:
            self.left_frames=frames[1]
            self.image=self.left_frames[self.frame_index]
        last_frame_bottom=self.rect.bottom
        last_frame_centerx=self.rect.centerx
        self.rect=self.image.get_rect()
        self.rect.bottom=last_frame_bottom
        self.rect.centerx=last_frame_centerx


    
    def  calc_velo(self, velo, accel, max_velo, is_positive=True):
        if is_positive:
            return min(velo+accel , max_velo)
        else:
            return max(velo-accel , -max_velo)
    
    def calc_frame_duration(self):
        duration=-60/self.max_run_velo*abs(self.x_velo)*80
        return duration
    
    def is_hurt_immune(self):
        if self.hurt_immune:
            if self.hurt_immune_timer==0:
                self.hurt_immune_timer=self.current_time
                self.blank_image=pygame.Surface((1,1))
            elif self.current_time - self.hurt_immune_timer<2000:
                if (self.current_time - self.hurt_immune_timer)%100<50:
                    self.image=self.blank_image
            else:
                self.hurt_immune=False
                self.hurt_immune_timer=0
    
    def shoot_fireball(self, level):
        if self.current_time-self.last_fireball_timer>300:
            self.frame_index=6
            fireball = powerup.Fireball(self.rect.centerx, self.rect.centery, self.face_right)
            level.powerup_group.add(fireball)
            self.can_shoot=False
            self.last_fireball_timer=self.current_time






















