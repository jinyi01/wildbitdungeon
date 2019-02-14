# Use in http://www.codeskulptor.org/
# Wild Wild bit Dungeon
# Top down rogue like shooter
# WASD to move
# 1 to select slot one, 2 to select slot two, Q to quick switch between them
# R to reload, F to pickup items (drops current item if inventory full)
# mouse click to fire or mouse click and hold to auto fire (autofire is slower)
# By Jinyi

# Need to implement:
# Pick character
# Enemy and player knockback
# Enemy ranged attacks
# Better animations
# Better art
# Sound
# Menus

# imports
import simplegui
import random
import math

# load images
tile_set = simplegui.load_image('https://i.imgur.com/4aKkKaL.png')
menu_image = simplegui.load_image('https://i.imgur.com/Up0xvHj.png')
background = simplegui.load_image('https://i.imgur.com/KsJ4ZdL.png')
grey_backing = simplegui.load_image('https://i.imgur.com/EFT1xns.png')
crosshair = simplegui.load_image('https://i.imgur.com/y4981Rb.png')

# GAME VARIABLES
WIDTH = 1000
HEIGHT = 750
DEATH_MENU_DELAY = 60
FONT = "monospace"

# PLAYER VARIABLES
PLAYER_IMAGE = {
    'Female': {
        'CenterRight': (769 + 32, 59 + 34),
        'CenterLeft': (572 + 32, 568 + 34),
        'Width': 63,
        'Height': 68,
        'DrawRatio': 1,
        'HitboxRatio': .85
        },
    'Male': {
        'CenterRight': (771 + 32, 171 + 45),
        'CenterLeft': (571 + 32, 680 + 45),
        'Width': 64,
        'Height': 82,
        'DrawRatio': 1,
        'HitboxRatio': .85
        },
    'FrameSpeed': 8,
    # placeholder
    'Width': 64,
    'Height': 64,
    'DrawRatio': 1,
    'HitboxRatio': 1
    }

PLAYER_HEALTH = 5
PLAYER_ACC = 1.65
INVINCIBLE_TIME = 60

# WEAPON VARIABLES
BULLET_LIFESPAN = 350

PISTOL = {
    "Name": "pistol",
    "Image": simplegui.load_image("https://i.imgur.com/QmNXU2J.png"),
    "Width": 600,
    "Height": 600,
    "DrawRatio": .1,
    "HitboxRatio": 1,
    "InvRatio": .125,

    "DropChance": 3,

    "BulletSize": 1.2,
    "Damage": 5,
    "Ammo": 32,
    "MagSize": 4,
    "ReloadTime": 25,
    "FireRate": 20,
    "AutoFireRate": 450,
    "BulletSpeed": 35
}

SUBMAC = {
    "Name": "submac",
    "Image": simplegui.load_image("https://i.imgur.com/kMFZnwZ.png"),
    "Width": 84,
    "Height": 32,
    "DrawRatio": 0.9,
    "HitboxRatio": 1,
    "InvRatio": 1,

    "DropChance": 4,

    "BulletSize": .9,
    "Damage": 1,
    "Ammo": 96,
    "MagSize": 32,
    "ReloadTime": 35,
    "FireRate": 2,
    "AutoFireRate": 100,
    "BulletSpeed": 35
}

SHOTGUN = {
    "Name": "shotgun",
    "Image": simplegui.load_image("https://i.imgur.com/8K0XDNI.png"),
    "Width": 43,
    "Height": 12,
    "DrawRatio": 1.8,
    "HitboxRatio": 1,
    "InvRatio": 1.8,

    "DropChance": 5,

    "BulletSize": .8,
    "Damage": 2,
    "Ammo": 18,
    "MagSize": 6,
    "ReloadTime": 30,
    "FireRate": 45,
    "AutoFireRate": 1200,
    "BulletSpeed": 30
}

RIFLE = {
    "Name": "rifle",
    "Image": simplegui.load_image("https://i.imgur.com/vTauBjG.png"),
    "Width": 64,
    "Height": 12,
    "DrawRatio": 1.4,
    "HitboxRatio": 1,
    "InvRatio": 1.3,

    "DropChance": 2,

    "BulletSize": 1,
    "Damage": 12,
    "Ammo": 24,
    "MagSize": 6,
    "ReloadTime": 70,
    "FireRate": 50,
    "AutoFireRate": 1500,
    "BulletSpeed": 40
}

# ENEMY VARIABLES
NEST_SPAWN_DELAY = 75

BRUTE = {
        "Name": "brute",
        "Type": 0,
        "Health": 8,
        "Speed": 4,
        "FollowRange": 300,
        "MeleeDamage": 1,
        "Weapon": None,

        'CenterRight': (1743 + 22, 823 + 36),
        'CenterLeft': (1489 + 22, 1438 + 36),
        'Width': 64,
        'Height': 72,
        'DrawRatio': 1.15,
        'HitboxRatio': 0.95,
        'FrameSpeed': 8,
        'FrameSize': 64
        }

LACKEY = {
        "Name": "lackey",
        "Type": 0,
        "Health": 5,
        "Speed": 3,
        "FollowRange": 350,
        "MeleeDamage": 1,
        "Weapon": {"Gun": "pistol",
                   "Firerate": 100,
                   "WeaponDamage": 1,
                   "BulletSpeed": 3
                   },
        'CenterRight': (1743 + 22, 823 + 36),
        'CenterLeft': (1489 + 22, 1438 + 36),
        'Width': 64,
        'Height': 72,
        'DrawRatio': 1,
        'HitboxRatio': 0.95,
        'FrameSpeed': 9,
        'FrameSize': 64
        }

RUNNER = {
        "Name": "runner",
        "Type": 1,
        "Health": 3,
        "Speed": 5.5,
        "FollowRange": 500,
        "MeleeDamage": 1,
        "Weapon": None,

        'CenterRight': (1743 + 20, 79 + 23),
        'CenterLeft': (1487 + 23, 1540 + 23),
        'Width': 64,
        'Height': 64,
        'DrawRatio': 1,
        'HitboxRatio': 0.7,
        'FrameSpeed': 5,
        'FrameSize': 64
        }

SNIPER = {
        "Name": "sniper",
        "Type": 1,
        "Health": 12,
        "Speed": 0.8,
        "FollowRange": 400,
        "MeleeDamage": 1,
        "Weapon": {"Gun": "rifle",
                   "Firerate": 200,
                   "WeaponDamage": 1,
                   "BulletSpeed": 8
                   },
        'CenterRight': (1474 + 28, 1083 + 32),
        'CenterLeft': (1736 + 28, 1083 + 32),
        'Width': 68,
        'Height': 72,
        'DrawRatio': 1,
        'HitboxRatio': 0.9,
        'FrameSpeed': 7,
        'FrameSize': 64
    }
QUEEN = {
        "Name": "queen",
        "Type": 2,
        "Health": 32,
        "Speed": 1,
        "FollowRange": 350,
        "MeleeDamage": 2,
        "Weapon": None,

        'CenterRight': (600 + 45, 1295 + 58),
        'CenterLeft': (85 + 45, 1654 + 58),
        'Width': 90,
        'Height': 115,
        'DrawRatio': 1.1,
        'HitboxRatio': 1,
        'FrameSpeed': 10,
        'FrameSize': 128
    }

BASIC_DROP_CHANCE_BOOST = 0
ADVANCED_DROP_CHANCE_BOOST = 1
BOSS_DROP_CHANCE_BOOST = 5

HEALTH_DROP_CHANCE = 4
AMMO_DROP_CHANCE = 20

# ITEM VARIABLES

WEAPON_LIFESPAN = 999999
ITEM_LIFESPAN = 800

HEALTH_RESTORE = 1
AMMO_RESTORE = 20

AMMOBOX = {
    "Image": simplegui.load_image("https://i.imgur.com/9pFnJHX.png"),
    "DrawRatio": 0.2,
    "HitboxRatio": 1
    }
                                  
MEDPACK = {
    "Image": simplegui.load_image("https://i.imgur.com/SMYe2Sz.png"),
    "DrawRatio": 0.9,
    "HitboxRatio": 1
    }

# TILE VARIABLES
GROUND = {
    'Center': (64 + 32, 256 + 32),
    'Width': 64,
    'Height': 64
    }
WALL = {
    'Center': (128 + 32, 64 + 32),
    'Width': 64,
    'Height': 64
    }
WARP = {
    'Center': (195 + 28, 399 + 18),
    'Width': 56,
    'Height': 36
    }
HEART = {
    'Center': (1155 + 26, 1031 + 24),
    'Width': 52,
    'Height': 48
    }  
NOHEART = {
    'Center': (1283 + 26, 1031 + 24),
    'Width': 52,
    'Height': 48
    }  
PORTAL = {
    "Image": simplegui.load_image("https://i.imgur.com/T7pzKou.png"),  
    }
PORTAL_WARP_TIME = 50
BULLET = {
    "Image": simplegui.load_image("https://i.imgur.com/DbDv43x.png"),
    "DrawRatio": 0.3,
    "HitboxRatio": 1
    }    

# converts rbg into hex color code string
def color(r,g,b):
    hex_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    # turn rgb values into hex as string
    return '#'+hex_digits[r//16]+hex_digits[r%16]+hex_digits[g//16]+hex_digits[g%16]+hex_digits[b//16]+hex_digits[b%16]

# generates random 2 element tuple with a range and how many decimals to go into
def rand_2tuple(size, decimals):
    size *= math.pow(10, decimals)
    d = math.pow(10, decimals)
    if d == 0:
        return (random.randint(-size, size), random.randint(-size, size))
    return (random.randint(-size, size)/d, random.randint(-size, size)/d)

# gets distance between two positions in 2d space    
def dist(pos1, pos2):
    x = pos2.x - pos1.x
    y = pos2.y - pos1.y
    return math.sqrt(x**2+y**2)

# gets the resulting vector
def get_vector(pos, angle, vec_size, get_pos = False):
    if get_pos:
        return Vec2d(pos.x + vec_size*math.sin(angle), pos.y + vec_size*math.cos(angle))
        # gets position + vector
    else:
        return Vec2d(vec_size*math.sin(angle), vec_size*math.cos(angle))
        # returns x, y based on vector

# return angles
def get_angle(pos1, pos2, camera_pos = False):
    if camera_pos:
        x = pos2.x + camera.pos.x - pos1.x 
        y = pos2.y + camera.pos.y - pos1.y
    else:
        x = pos2.x - pos1.x 
        y = pos2.y - pos1.y
    return math.atan2(x, y)        

# 2d vector math (add vectors, subtract vectors, get tuple)        
class Vec2d:
    
    def __init__(self, x, y):
        self.x = x * 1.0
        self.y = y * 1.0
    
    def xy(self):
        return self.x, self.y
    
    def __add__(self, other):
        if type(other) == tuple or type(other) == list and len(other) == 2:
            return Vec2d(self.x + other[0], self.y + other[1])
        elif type(other).__name__ == 'Vec2d':
            return Vec2d(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        if type(other) == tuple or type(other) == list and len(other) == 2:
            return Vec2d(self.x + other[0], self.y + other[1])
        elif type(other).__name__ == 'Vec2d':
            return Vec2d(self.x + other.x, self.y + other.y)    
    
    def __sub__(self, other):
        if type(other) == tuple or type(other) == list and len(other) == 2:
            return Vec2d(self.x - other[0], self.y - other[1])  
        elif type(other).__name__ == 'Vec2d':
            return Vec2d(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        if type(other) == tuple or type(other) == list and len(other) == 2:
            return Vec2d(self.x - other[0], self.y - other[1]) 
        elif type(other).__name__ == 'Vec2d':
            return Vec2d(self.x - other.x, self.y - other.y) 
    
    def __mul__(self, other):
        return Vec2d(self.x * other, self.y * other)
        
    def __imul__(self, other):
        return Vec2d(self.x * other, self.y * other)
    
    def __div__(self, other):
        return Vec2d(self.x / other, self.y / other)
    
    def __idiv__(self, other):
        return Vec2d(self.x / other, self.y / other)
    
    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)
    
    def magnitude(self):
        import math
        return math.sqrt((self.x**2)+(self.y**2))
    
    def direction(self):
        import math
        return math.atan(self.y/self.x)
    
    def rotate(self, angle):
        import math
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = y * math.cos(angle) + x * math.sin(angle)

# camera for tracking player movement and defining where to draw
class Camera:
    
    def __init__(self, track):
        self.pos = Vec2d(-WIDTH/2, -HEIGHT/2)
        self.track = track
    
    # tracks the player position
    def get_playerpos(self, pos):
        self.track = pos
    
    def update(self):
        # get difference in position
        delta = self.track - self.pos

        # check if theres change in pos and move camera to player pos
        if delta.x > 0:
            if self.track.x > self.pos.x + WIDTH/2:
                self.pos.x = int(self.track.x) - WIDTH/2
            if self.track.x < self.pos.x + WIDTH/2:
                self.pos.x = int(self.track.x) - WIDTH/2
        if delta.y > 0:
            if self.track.y > self.pos.y + HEIGHT/2:
                self.pos.y = int(self.track.y) - HEIGHT/2
            if self.track.y < self.pos.y + HEIGHT/2:
                self.pos.y = int(self.track.y) - HEIGHT/2	
                    

# class for all entities (position, velocity, draw size, hitbox size)            
class Entity:
    def __init__(self, pos, vel, image, rotate = 0):
        self.pos = Vec2d(*pos)
        self.vel = Vec2d(*vel)

        try:
            self.image = image["Image"]
            self.width = image["Image"].get_width()
            self.height = image["Image"].get_height()
        except:
            self.width = image["Width"]
            self.height = image["Height"]

        self.rotate = rotate
        
        self.draw_width = self.width * image["DrawRatio"]
        self.draw_height = self.height * image["DrawRatio"]
        self.hit_width = self.draw_width * image["HitboxRatio"]
        self.hit_height = self.draw_height * image["HitboxRatio"]

    def get_box(self):
        # get box area around entity
        return (self.pos.x-self.hit_width/2, self.pos.x + self.hit_width/2,
           self.pos.y -self.hit_height/2, self.pos.y +self.hit_height/2)            

    def is_hit(self, hits):
        for h in hits:
            # check if hit with wall using the grid coords
            if self.game.level.grid[h[1]][h[0]] == "W":  
                return True
   
    def collide(self, target):
        # checks if two objects collide
        min_xdistance = target.hit_width/2 + self.hit_width/2
        current_xdistance = abs(target.pos.x - self.pos.x)
        min_ydistance = target.hit_height/2 + self.hit_height/2
        current_ydistance = abs(target.pos.y - self.pos.y)
        if (current_xdistance < min_xdistance) and (current_ydistance < min_ydistance):
            return self
        # if nothing hit return false
        return None

    def draw_stats(self, canvas, hitbox = False, pos = False, health = False, damage = False):
        # draw stats for debug
        draw_pos = self.pos - camera.pos
        if hitbox:
            canvas.draw_polygon([(draw_pos.x - self.hit_width/2, draw_pos.y - self.hit_height/2), 
                             (draw_pos.x + self.hit_width/2, draw_pos.y - self.hit_height/2),
                             (draw_pos.x + self.hit_width/2, draw_pos.y + self.hit_height/2),
                             (draw_pos.x - self.hit_width/2, draw_pos.y + self.hit_height/2)], 
                            1, 'Black')              
        if pos:
            canvas.draw_text("(%s, %s)" % (round(self.pos.x), round(self.pos.y)), draw_pos.xy(), 22, 'Black')        
        if health:
            canvas.draw_text(str(self.health), draw_pos.xy(), 22, 'Black')
        if damage:
            canvas.draw_text(str(self.damage), draw_pos.xy(), 22, 'Black')


# Player class for the user to control (contains all player functions)
class Player(Entity):
    
    def __init__(self, game, pos):  
        Entity.__init__(self, pos, (0, 0), PLAYER_IMAGE)
        
        self.game = game
        
        self.acc = Vec2d(0, 0)
        # different gender has different hit boxes (need way to choose character)
        self.gender = random.choice(['Male', 'Female'])
        # flip gender to set hitboxes
        self.flip_gender()
        
        self.frame = 0
        
        self.max_health = PLAYER_HEALTH
        self.health = PLAYER_HEALTH
        self.invinc_timer = -INVINCIBLE_TIME
        
        self.aim = 0
        self.weapons = [Gun(self.game, self, PISTOL), Nothing]
        
        self.item_hits = []
        self.reloading = False
        
        self.flicker = False
        self.direction = PLAYER_IMAGE[self.gender]["CenterRight"]

    def update(self):        
        
        # gravity
        self.acc = Vec2d(0, 0)
        
        # check if WASD keys and pressed and accelerate depending on which key
        if self.game.up:
            self.acc.y = -PLAYER_ACC
        if self.game.down:
            self.acc.y = PLAYER_ACC
        if self.game.right:
            self.acc.x = PLAYER_ACC
        if self.game.left:
            self.acc.x = -PLAYER_ACC
         
        # check if weapon is locked and reduce its cooldown
        try:
            if self.weapons[self.current_slot].lock:
                self.weapon_lock -= 1
                if self.weapon_lock <= 0:
                    self.weapons[self.current_slot].lock = False
        except:
            pass

        # if mag is empty, auto reload
        try:
            if self.weapons[self.current_slot].mag == 0 and self.weapons[self.current_slot].ammo > 0:
                self.reloading = True
        except:
            pass
        
        # if reloading, slow player and count down reload clock, if finished, reload gun and reset clock
        if self.reloading:
            slow = .3
            
            self.weapons[self.current_slot].reload_clock -= 1
            if self.weapons[self.current_slot].reload_clock <= 0:
                self.weapons[self.current_slot].reload()
                self.weapons[self.current_slot].reload_clock = self.weapons[self.current_slot].reload_time
                self.reloading = False
        else:
            slow = .16

        # friction to cap velocity
        self.acc.x += self.vel.x * -slow
        self.acc.y += self.vel.y * -slow
        
        # get grid coords for each point of the box
        cell = [int(p//64) for p in self.get_box()] 
        
        # accelerate
        self.vel.x += self.acc.x
        if abs(self.vel.x) < 0.05:
            # floor to 0
            self.vel.x = 0
        # update x position
        self.pos.x += self.vel.x
        # get new coords after movement
        cell_new = [int(p//64) for p in self.get_box()]
        # if moved, check collision
        if cell[0] != cell_new[0] or cell[1] != cell_new[1]:
            box = self.get_box()
            # get side that can hit depending on velocity
            side_x = box[0] if self.vel.x < 0 else box[1]
            # get hit points of box
            hits_x = [(side_x//64, k//64) for k in (box[3], (box[3]+box[2])/2, box[2])]

            if self.is_hit(hits_x):
                # if hit with wall, push player x pos
                if self.vel.x > 0:
                    self.pos.x = self.pos.x - side_x%64 - .1
                elif self.vel.x < 0:
                    self.pos.x = self.pos.x + (-side_x)%64 + .1
        
        # accelerate y
        self.vel.y += self.acc.y
        if abs(self.vel.y) < 0.05:
            # floor
            self.vel.y = 0
        # update y pos
        self.pos.y += self.vel.y
        # get grid coords
        cell_new = [int(p//64) for p in self.get_box()]
        # check if coords changed
        if cell[2] != cell_new[2] or cell[3] != cell_new[3]:
            box = self.get_box()
            side_y = box[2] if self.vel.y < 0 else box[3]
            # get sides that can hit
            hits_y = [(k//64, side_y//64) for k in (box[1], (box[1]+box[0])/2, box[0])]

            if self.is_hit(hits_y):
                # push player out of wall depending on velocity
                if self.vel.y > 0:
                    self.pos.y = self.pos.y - side_y%64 - .1
                elif self.vel.y < 0:
                    self.pos.y = self.pos.y + (-side_y)%64 + .1

        # every 8 ticks increment frame        
        if self.game.time % PLAYER_IMAGE["FrameSpeed"] == 0:  
            # check which direction to find which way frame increments
            if self.vel.x > 0:      
                self.frame += 1
            elif self.vel.x < 0:
                self.frame -= 1
            # if only moving in y, check last direction to find which way frame increments
            elif abs(self.vel.y) > 0:
                if self.direction == PLAYER_IMAGE[self.gender]["CenterRight"]:
                    self.frame += 1
                else:
                    self.frame -= 1
            # if not moving, freeze frame
            else:
                self.frame = 0
            self.frame %= 4        
       
    def set_aim(self, pos):
        # gets angle of player direction
        self.aim = get_angle(self.pos, pos, camera_pos = True)
    
    def get_hit(self, source):
        # check if player has health and if last time hit has reached a certain time
        if self.health > 0 and self.invinc_timer + INVINCIBLE_TIME < self.game.time:
            # remove health and update last hit time
            self.health -= source.damage
            self.invinc_timer = self.game.time
    
    def pickup(self):
        def add_weapon(weapon, data):
            # find empty slot, if non remain at current slot
            for i, spot in enumerate(self.weapons):
                if spot.__name__ == "Nothing":
                    self.current_slot = i
                    break
            # drop gun if slot has weapon        
            self.drop()

            # equip new gun
            if data:
                self.weapons[self.current_slot] = data
            else:
                self.weapons[self.current_slot] = Gun(self.game, self, weapon)
            self.equip(self.current_slot)

        # if there are items player collides with, get first item and see if it is a gun to pickup
        if self.item_hits:
            item = self.item_hits[0]

            if item.name == "pistol":
                add_weapon(PISTOL, item.data)
                self.game.items.remove(item)                
            elif item.name == "shotgun":
                add_weapon(SHOTGUN, item.data)
                self.game.items.remove(item)  
            elif item.name == "submac":
                add_weapon(SUBMAC, item.data)
                self.game.items.remove(item)  
            elif item.name == 'rifle':
                add_weapon(RIFLE, item.data)
                self.game.items.remove(item)  
    
    def drop(self):
        # drop weapon in current slot and create item in world (saves ammo and mag info)
        if self.weapons[self.current_slot].__name__ != "Nothing":
            gun = self.weapons[self.current_slot]
            if gun.name == "pistol":
                self.game.items.append(Item(self.game, "pistol", PISTOL, 
                                            self.pos.xy(), rand_2tuple(8, 1), 
                                            lifespan = WEAPON_LIFESPAN, data = self.weapons[self.current_slot]))     
            elif gun.name == "shotgun":
                self.game.items.append(Item(self.game, "shotgun", SHOTGUN, 
                                            self.pos.xy(), rand_2tuple(8, 1), 
                                            lifespan = WEAPON_LIFESPAN, data = self.weapons[self.current_slot]))  
            elif gun.name == "submac":
                self.game.items.append(Item(self.game, "submac", SUBMAC, 
                                            self.pos.xy(), rand_2tuple(8, 1), 
                                            lifespan = WEAPON_LIFESPAN, data = self.weapons[self.current_slot]))      
            elif gun.name == "rifle":
                self.game.items.append(Item(self.game, "rifle", RIFLE, 
                                            self.pos.xy(), rand_2tuple(8, 1), 
                                            lifespan = WEAPON_LIFESPAN, data = self.weapons[self.current_slot]))    

            self.weapons[self.current_slot] = Nothing
            self.equip(self.current_slot)

    def equip(self, index):
        self.reloading = False
        self.current_slot = index 
        # try to equip weapon at index

        # stop weapon firing
        self.stop_autofire()

        if self.weapons[index].__name__ != 'Nothing':
            # weapon lock to prevent quick switch firing
            self.weapons[index].lock = True
            self.weapon_lock = self.weapons[index].cooldown/10.0
        
        # set click handler to whats equipped
        set_clickhandler(self.weapons[index].mouseclick_handler, self.weapons[index].mousedrag_handler)
    
    def quick_switch(self):
        # flip current slot between 0 and 1
        self.current_slot ^= 1
        self.equip(self.current_slot)
    
    def stop_autofire(self):
        # attempt to stop all weapon autofire (doesnt fix autofire bug)
        for weapon in self.weapons:
            try:
                weapon.autofire.stop()
            except:
                pass
        
    def reload(self):
        if self.weapons[self.current_slot].__name__ == 'Nothing':
            return

        # reloads if it is not already reloading and there is space in mag
        if not self.reloading and self.weapons[self.current_slot].mag != self.weapons[self.current_slot].mag_size:
            self.reloading = True

    def flip_gender(self):
        # flip character
        if self.gender == 'Male':
            self.gender = 'Female'
        else:
            self.gender = 'Male'

        # update images and hitboxes
        self.width = PLAYER_IMAGE[self.gender]["Width"]
        self.height = PLAYER_IMAGE[self.gender]["Height"]

        self.draw_width = self.width * PLAYER_IMAGE[self.gender]["DrawRatio"]
        self.draw_height = self.height * PLAYER_IMAGE[self.gender]["DrawRatio"]
        self.hit_width = self.draw_width * PLAYER_IMAGE[self.gender]["HitboxRatio"]
        self.hit_height = self.draw_height * PLAYER_IMAGE[self.gender]["HitboxRatio"]

        self.direction = PLAYER_IMAGE[self.gender]["CenterRight"]

    def draw(self, canvas):
        draw_pos = self.pos - camera.pos
        
        # check direction player is in
        if self.vel.x > 0.1:
            self.direction = PLAYER_IMAGE[self.gender]["CenterRight"]
        elif self.vel.x < -0.1:
            self.direction = PLAYER_IMAGE[self.gender]["CenterLeft"] 
            
        if self.invinc_timer + INVINCIBLE_TIME > self.game.time:
            # switch between draw character and dont draw character
            if self.game.time % 15 == 0:
                self.flicker = not self.flicker
            if self.flicker:
                canvas.draw_image(tile_set, 
                                (self.direction[0] + self.frame*64, self.direction[1]), 
                                (PLAYER_IMAGE[self.gender]["Width"], PLAYER_IMAGE[self.gender]["Height"]),
                                draw_pos.xy(), 
                                (self.draw_width, self.draw_height))
        # if not hit, just draw character
        else:
            canvas.draw_image(tile_set, 
                            (self.direction[0] + self.frame*64, self.direction[1]), 
                            (PLAYER_IMAGE[self.gender]["Width"], PLAYER_IMAGE[self.gender]["Height"]),
                            draw_pos.xy(), 
                            (self.draw_width, self.draw_height))
        

class Item(Entity):
    def __init__(self, game, name, item, pos, vel, lifespan = 300, data = None):
        Entity.__init__(self, pos, vel, item)
        self.game = game
        self.name = name
        # data used to store ammo information etc
        self.data = data
            
        self.picked_up = False   
        self.lifespan = lifespan
            
    def update(self):
        self.pos += self.vel
        self.vel.x *= .8
        self.vel.y *= .8
        
        if abs(self.vel.x) < 0.01:
            self.vel.x = 0
        if abs(self.vel.y) < 0.01:
            self.vel.y = 0   

        # lifespan for despawn    
        self.lifespan -= 1

    def draw(self, canvas):
        draw_pos = self.pos - camera.pos
        canvas.draw_image(self.image, 
                          (self.width/2, self.height/2), 
                          (self.width, self.height),
                          draw_pos.xy(), 
                          (self.draw_width, self.draw_height), self.rotate)

class Gun:
    def __init__(self, game, person, weapon): 
        self.game = game
        self.person = person
        # pass in weapon variable and assign
        self.name = weapon["Name"]
        
        self.damage = weapon["Damage"]
        
        self.ammo = weapon["Ammo"]
        self.mag = weapon["MagSize"]
        self.mag_size = weapon["MagSize"]
        
        self.reload_clock = weapon["ReloadTime"]
        self.reload_time = weapon["ReloadTime"]
        
        self.last_fire = -weapon["FireRate"]
        self.cooldown = weapon["FireRate"]
        # auto fire rate is slower than click
        self.autofire = simplegui.create_timer(weapon["AutoFireRate"], self.timer)
        
        # weapon lock prevents spam quick switch
        self.lock = False
    
    def reload(self):
        missing = self.mag_size - self.mag
        if self.ammo - missing < 0:
            # if not enough ammo to fill mag use remainder
            missing = self.ammo
            self.ammo = 0
        else:
            self.ammo -= missing
        self.mag += missing
        
    def shoot(self):
        # make sure cooldown has passed before shooting
        if self.mag > 0 and self.last_fire + self.cooldown < self.game.time:
            self.create_bullet()
            self.mag -= 1
            self.last_fire = self.game.time
            
    def create_bullet(self):
        # check what gun to create unique bullet
        if self.name == "pistol":
            self.game.projectiles.append(Bullet(self.game, 
                                                BULLET,
                                                True,
                                                get_vector(self.person.pos, 
                                                          self.person.aim, 
                                                          0, True).xy(), 
                                                self.person.aim, 
                                                get_vector(self.person.pos, 
                                                          self.person.aim,
                                                          PISTOL["BulletSpeed"], False).xy(), 
                                                self.damage, 
                                                PISTOL["BulletSize"],
                                                BULLET_LIFESPAN))  
        elif self.name == "shotgun":
            # bullet spread
            angles = [-32.0, -64.0, -128.0, 128.0, 64.0, 32.0]
            for i in range(7):
                # get random rangles
                rand_angle = self.person.aim + math.pi/random.choice(angles)
                self.game.projectiles.append(Bullet(self.game, 
                                                    BULLET, 
                                                    True,
                                                    get_vector(self.person.pos, 
                                                            self.person.aim, 
                                                            0, True).xy(), 
                                                    self.person.aim, 
                                                    get_vector(self.person.pos, 
                                                            rand_angle,
                                                            SHOTGUN["BulletSpeed"], False).xy(), 
                                                    self.damage, 
                                                    SHOTGUN["BulletSize"],
                                                    BULLET_LIFESPAN)) 
        elif self.name == "submac":                                                    
            self.game.projectiles.append(Bullet(self.game, 
                                                BULLET, 
                                                True,
                                                get_vector(self.person.pos, 
                                                        self.person.aim, 
                                                        0, True).xy(), 
                                                self.person.aim, 
                                                get_vector(self.person.pos, 
                                                        self.person.aim,
                                                        SUBMAC["BulletSpeed"], False).xy(), 
                                                self.damage, 
                                                SUBMAC["BulletSize"],
                                                BULLET_LIFESPAN))  
        elif self.name == "rifle":
            self.game.projectiles.append(Bullet(self.game, 
                                                BULLET,
                                                True,
                                                get_vector(self.person.pos, 
                                                        self.person.aim, 
                                                        0, True).xy(), 
                                                self.person.aim, 
                                                get_vector(self.person.pos, 
                                                        self.person.aim,
                                                        RIFLE["BulletSpeed"], False).xy(),
                                                self.damage, 
                                                RIFLE["BulletSize"],
                                                BULLET_LIFESPAN))                                                    

    def mouseclick_handler(self, position):
        # update mouse pos and angles
        self.game.mouse_pos = Vec2d(*position)
        self.person.set_aim(Vec2d(*position))
        
        # allow shooting if not locked
        if not self.lock:
            self.shoot()

        if self.autofire.is_running():
            self.autofire.stop()
            
    def mousedrag_handler(self, position):
        self.game.mouse_pos = Vec2d(*position)
        self.person.set_aim(Vec2d(*position))
        
        if not self.lock:
            if not self.autofire.is_running():
                # shoot before starting clock so theres no delay
                self.shoot()
                self.autofire.start()        
        
    def timer(self):
        # creats bullet if mag allows
        if self.mag > 0:
            self.create_bullet()
            self.mag -= 1  
            
class Bullet(Entity):  
    
    def __init__(self, game, image, player_bullet, pos, angle, vel, damage, size_ratio, lifespan):
        Entity.__init__(self, pos, vel, image)
        self.game = game
        self.player_bullet = player_bullet
        
        self.draw_width *= size_ratio
        self.draw_height *= size_ratio
        self.hit_width *= size_ratio
        self.hit_height *= size_ratio

        self.lifespan = lifespan
        self.despawn = False
        
        self.angle = angle
        
        self.damage = damage
    
    def update(self):
        
        cell = [int(p//64) for p in self.get_box()] 
        # update x position
        self.pos.x += self.vel.x
        # get new coords after movement
        # get new coords after movement
        cell_new = [int(p//64) for p in self.get_box()]

        # if moved, check collision
        if cell[0] != cell_new[0] or cell[1] != cell_new[1]:
            box = self.get_box()
            # get side that can hit depending on velocity
            side_x = box[0] if self.vel.x < 0 else box[1]
            # get hit points of box
            hits_x = [(side_x//64, k//64) for k in (box[3], (box[3]+box[2])/2, box[2])]

            if self.is_hit(hits_x):
                # if hit with wall, push player x pos
                if self.vel.x > 0:
                    self.pos.x = self.pos.x - side_x%64 - 1
                    self.despawn = True
                elif self.vel.x < 0:
                    self.pos.x = self.pos.x + (-side_x)%64 + 1
                    self.despawn = True
                else:
                    pass
        # update y pos
        self.pos.y += self.vel.y
        # get grid coords
        cell_new = [int(p//64) for p in self.get_box()]
        # check if coords changed
        if cell[2] != cell_new[2] or cell[3] != cell_new[3]:
            box = self.get_box()
            side_y = box[2] if self.vel.y < 0 else box[3]
            # get sides that can hit
            hits_y = [(k//64, side_y//64) for k in (box[1], (box[1]+box[0])/2, box[0])]

            if self.is_hit(hits_y):
                # push player out of wall depending on velocity
                if self.vel.y > 0:
                    self.pos.y = self.pos.y - side_y%64 - 1
                    self.despawn = True
                elif self.vel.y < 0:
                    self.pos.y = self.pos.y + (-side_y)%64 + 1
                    self.despawn = True
                else:
                    pass
        
        if self.lifespan <= 0:
            self.despawn = True
        
        self.lifespan -= 1

    def draw(self, canvas):
        draw_pos = self.pos - camera.pos
        canvas.draw_image(self.image, 
                          (self.width/2, self.height/2), 
                          (self.width, self.height),
                          draw_pos.xy(), 
                          (self.draw_width, self.draw_height), self.rotate)

 
class Tile:
    def __init__(self, game, tile_info, pos, draw_ratio = 1, hit_ratio = 1):
        self.game = game
        self.pos = Vec2d(*pos)
        self.tile_info = tile_info
        self.width = tile_info['Width']
        self.height = tile_info['Height']
        self.draw_width = self.width * draw_ratio
        self.draw_height = self.height * draw_ratio
        self.hit_width = self.width
        self.hit_height = self.height
        
    def draw(self, canvas):
        draw_pos = self.pos - camera.pos
        canvas.draw_image(tile_set, self.tile_info['Center'], (self.width, self.height),
                          draw_pos.xy(), (self.draw_width, self.draw_height))
        
class Portal(Tile):
    def __init__(self, game, tile_info, pos):
        Tile.__init__(self, game, tile_info, pos, draw_ratio = 1, hit_ratio = 0.5)
        self.warp_time = PORTAL_WARP_TIME

    def collide(self, other):
        # use size larger than image for larger area of influence
        min_xdistance = other.hit_width/2 + self.draw_width
        current_xdistance = abs(other.pos.x - self.pos.x)
        min_ydistance = other.hit_height/2 + self.draw_height
        current_ydistance = abs(other.pos.y - self.pos.y)
        if (current_xdistance < min_xdistance) and (current_ydistance < min_ydistance):
            return True
        # if nothing hit return false
        return False

    def warp(self, other):
        min_xdistance = other.hit_width/2 + self.hit_width/2
        current_xdistance = abs(other.pos.x - self.pos.x)
        min_ydistance = other.hit_height/2 + self.hit_height/2
        current_ydistance = abs(other.pos.y - self.pos.y)
        if (current_xdistance < min_xdistance) and (current_ydistance < min_ydistance):
            return True
        # if nothing hit return false
        return False
    
class EnemyNest(Tile):
    
    def __init__(self, game, tile_info, pos, brutes, lackeys, runners, snipers, queens):
        Tile.__init__(self, game, tile_info, pos)
        self.active = True
        
        self.brutes = brutes
        self.lackeys = lackeys
        self.runners = runners
        self.snipers = snipers
        self.queens = queens
        self.total_spawn = brutes + runners + snipers + queens

    def spawn(self):
        if self.queens > 0:
            self.game.enemies.append(Enemy(self.game, self.pos.xy(), rand_2tuple(5, 1), QUEEN))
            self.queens -=1
            self.decrease_count()

        if self.snipers > 0:
            self.game.enemies.append(Enemy(self.game, self.pos.xy(), rand_2tuple(5, 1), SNIPER))
            self.snipers -=1  
            self.decrease_count()

        if self.runners > 0:
            self.game.enemies.append(Enemy(self.game, self.pos.xy(), rand_2tuple(5, 1), RUNNER))
            self.runners -=1  
            self.decrease_count()
        
        if self.lackeys > 0:
            self.game.enemies.append(Enemy(self.game, self.pos.xy(), rand_2tuple(5, 1), LACKEY))
            self.lackeys -=1        
            self.decrease_count()  
            
        if self.brutes > 0:
            self.game.enemies.append(Enemy(self.game, self.pos.xy(), rand_2tuple(5, 1), BRUTE))
            self.brutes -=1        
            self.decrease_count()
    
    def decrease_count(self):
        self.total_spawn -= 1
        self.game.level.total_enemies -= 1
        
class Enemy(Entity):     
    
    def __init__(self, game, pos, vel, enemy):  
        Entity.__init__(self, pos, vel, enemy)
        self.game = game

        self.enemy = enemy
        self.name = enemy['Name']
        self.type = enemy['Type']
        self.health = enemy['Health']
        self.damage = enemy['MeleeDamage']
        
        self.speed = enemy['Speed']
        self.previous_vel = self.vel
        
        if enemy["Weapon"]:
            self.weapon = True
            self.weapon_damage = enemy["Weapon"]["WeaponDamage"]
            self.bullet_speed = enemy["Weapon"]["BulletSpeed"]
            self.cooldown = enemy["Weapon"]["Firerate"]
            # set cooldown clock to firerate so enemy does not immediately fire at player
            self.cooldown_clock = enemy["Weapon"]["Firerate"]/2.0
        else:
            self.weapon = None
        
        self.aim = 0
        self.follow_range = enemy["FollowRange"]
        self.follow_player = False
        
        self.direction = self.enemy["CenterRight"]
        self.frame = 0
    
    def update(self):   
        # check if within a radius or if following player
        if (dist(self.pos, self.game.player.pos) < self.follow_range) or self.follow_player:
            if not self.follow_player:
                # set following player so it is permanent
                self.follow_player = True
            # get angle player is at
            direction = get_angle(self.pos, self.game.player.pos)
            # get the velocity vector to move towards player
            self.vel = get_vector(self.pos, direction, self.speed)
        else:
            if random.randint(1, 100) > 95:   
                rand_vel = Vec2d(random.choice([-self.speed, 0, self.speed]), 
                                 random.choice([-self.speed, 0, self.speed]))
                self.previous_vel = rand_vel
                self.vel = rand_vel
            else:
                self.vel = self.previous_vel

        
        self.aim = get_angle(self.pos, self.game.player.pos) + random.choice([math.pi/48.0, 0, -math.pi/48.0])
        
        # get grid coords for each point of the box
        cell = [int(p//64) for p in self.get_box()] 
        
        if abs(self.vel.x) < 0.01:
            # floor to 0
            self.vel.x = 0
        # update x position
        self.pos.x += self.vel.x
        # get new coords after movement
        cell_new = [int(p//64) for p in self.get_box()]
        # if moved, check collision
        if cell[0] != cell_new[0] or cell[1] != cell_new[1]:
            box = self.get_box()
            # get side that can hit depending on velocity
            side_x = box[0] if self.vel.x < 0 else box[1]
            # get hit points of box
            hits_x = [(side_x//64, k//64) for k in (box[3], (box[3]+box[2])/2, box[2])]

            if self.is_hit(hits_x):
                # if hit with wall, push player x pos
                if self.vel.x > 0:
                    self.pos.x = self.pos.x - side_x%64 - .1
                elif self.vel.x < 0:
                    self.pos.x = self.pos.x + (-side_x)%64 + .1
        
        if abs(self.vel.y) < 0.01:
            # floor
            self.vel.y = 0
        # update y pos
        self.pos.y += self.vel.y
        # get grid coords
        cell_new = [int(p//64) for p in self.get_box()]
        # check if coords changed
        if cell[2] != cell_new[2] or cell[3] != cell_new[3]:
            box = self.get_box()
            side_y = box[2] if self.vel.y < 0 else box[3]
            # get sides that can hit
            hits_y = [(k//64, side_y//64) for k in (box[1], (box[1]+box[0])/2, box[0])]

            if self.is_hit(hits_y):
                # push player out of wall depending on velocity
                if self.vel.y > 0:
                    self.pos.y = self.pos.y - side_y%64 - .1
                elif self.vel.y < 0:
                    self.pos.y = self.pos.y + (-side_y)%64 + .1
                
        if self.follow_player and self.weapon:
            if self.cooldown_clock <= 0:
                self.shoot()
                self.cooldown_clock = self.cooldown
            self.cooldown_clock -= 1
                
        # every 8 ticks increment frame        
        if self.game.time % self.enemy["FrameSpeed"] == 0:  
            # check which direction to find which way frame increments
            if self.vel.x > 0:      
                self.frame += 1
            elif self.vel.x < 0:
                self.frame -= 1
            # if only moving in y, check last direction to find which way frame increments
            elif abs(self.vel.y) > 0:
                if self.direction == self.enemy["CenterRight"]:
                    self.frame += 1
                else:
                    self.frame -= 1
            # if not moving, freeze frame
            else:
                self.frame = 0
            self.frame %= 4      
            
    def drop(self):
        # get drop boost based on enemy type
        if self.type == 2:
            boost = BOSS_DROP_CHANCE_BOOST
        elif self.type == 1:
            boost = ADVANCED_DROP_CHANCE_BOOST
        elif self.type == 0:
            boost = BASIC_DROP_CHANCE_BOOST
            
        def roll_number():
            return random.randint(1, 100000)/1000.0
        
        # first roll lower chance item, if fail, then roll higher. Create item when successful roll
        if roll_number() < HEALTH_DROP_CHANCE:
            self.game.items.append(Item(self.game, "health", MEDPACK, self.pos.xy(), rand_2tuple(10, 1)))
        elif roll_number() < AMMO_DROP_CHANCE:
            self.game.items.append(Item(self.game, "ammo", AMMOBOX, self.pos.xy(), rand_2tuple(10, 1)))

        if roll_number() < RIFLE['DropChance'] + boost:
            self.game.items.append(Item(self.game, "rifle", RIFLE, 
                                        self.pos.xy(), rand_2tuple(10, 1), 
                                        lifespan = WEAPON_LIFESPAN))
        elif roll_number() < SHOTGUN['DropChance'] + boost:
            self.game.items.append(Item(self.game, "shotgun", SHOTGUN, 
                                        self.pos.xy(), rand_2tuple(10, 1), 
                                        lifespan = WEAPON_LIFESPAN))
        elif roll_number() < SUBMAC['DropChance'] + boost:
            self.game.items.append(Item(self.game, "submac", SUBMAC, 
                                        self.pos.xy(), rand_2tuple(10, 1), 
                                        lifespan = WEAPON_LIFESPAN))
        elif roll_number() < PISTOL['DropChance'] + boost:
            self.game.items.append(Item(self.game, "pistol", PISTOL, 
                                        self.pos.xy(), rand_2tuple(10, 1), 
                                        lifespan = WEAPON_LIFESPAN))           
            
    def shoot(self):
        # shoot bullet that can only hurt player
        self.game.projectiles.append(Bullet(self.game, 
                                            BULLET,
                                            False,
                                            get_vector(self.pos, 
                                                      self.aim, 
                                                      0, True).xy(), 
                                            self.aim, 
                                            get_vector(self.pos, 
                                                      self.aim,
                                                      self.bullet_speed, False).xy(),
                                            self.weapon_damage,
                                            1,
                                            BULLET_LIFESPAN))

    def draw_type(self, canvas, image, draw_pos):
        # check which direction to use
        if self.vel.x > 0:
            self.direction = image['CenterRight']
        elif self.vel.x < 0:
            self.direction = image['CenterLeft']

        canvas.draw_image(tile_set, 
                            (self.direction[0] + self.frame*image['FrameSize'], self.direction[1]), 
                            (image['Width'], image['Height']),
                            draw_pos.xy(), 
                            (self.draw_width, self.draw_height))

    def draw(self, canvas):
        draw_pos = self.pos - camera.pos
        # check which enemy type to draw
        if self.name == "brute":
            self.draw_type(canvas, BRUTE, draw_pos)

        elif self.name == "lackey":
            self.draw_type(canvas, LACKEY, draw_pos)

        elif self.name == "runner":
            self.draw_type(canvas, RUNNER, draw_pos)

        elif self.name == "sniper":
            self.draw_type(canvas, SNIPER, draw_pos)

        elif self.name == "queen":
            self.draw_type(canvas, QUEEN, draw_pos)

        
# Map generation (currently 19x19 square)
# X = Nothing
# W = Wall
# ' ' = Ground
# N = Enemy Nest
# P = Player spawn

levels = [
    {
        "Grid": ["XXXXWWWWWWWWWWXXXXX",
                 "WWWWW        WWWWWW",
                 "WW       P       WW",
                 "WW                W",
                 "W    WW      WW   W",
                 "W   WWWWW         W",
                 "W                 W",
                 "WWW             WWW",
                 "WWWWWWW     WWWWWWW",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W     N     N     W",
                 "WW              WWW",
                 "XWWW           WWXX",
                 "XXXWWWWWWWWWWWWWXXX",
                 "XXXXXXXXXXXXXXXXXXX"],
        "brutes": 2,
        "lackeys": 2,
        "runners": 1,
        "snipers": 0,
        "queens": 0
    },
    {
        "Grid": ["XXXXXXXXWWWWWWWWWWW",
                 "WWWWWWWWW         W",
                 "W       W         W",
                 "W             P   W",
                 "W                 W",
                 "W       W         W",
                 "W       W         W",
                 "W       WWWWW  WWWW",
                 "W        W        W",
                 "W   N    W        W",
                 "W        W        W",
                 "W        W        W",
                 "WWW  WWWWWWW    WWW",
                 "W         W       W",
                 "W         W       W",
                 "W              N  W",
                 "W   N             W",
                 "W         W       W",
                 "WWWWWWWWWWWWWWWWWWW"],
        "brutes": 3,
        "lackeys": 2,
        "runners": 1,
        "snipers": 1,
        "queens": 0
    },
    {
        "Grid": ["WWWWWWWWWWWWWWWWWWW",
                 "W       W         W",
                 "W       W     N   W",
                 "W                 W",
                 "W                 W",
                 "W       W         W",
                 "WW    WWWWWWWWWWWWW",
                 "W       WXXXXXXXXXX",
                 "W       WWWWWWWWWWW",
                 "W       W         W",
                 "W       W     N   W",
                 "W       W         W",
                 "W       W   WW   WW",
                 "WWW  WWWW   W     W",
                 "W       W   W     W",
                 "W           W  N  W",
                 "W  P        W     W",
                 "W       WWWWWWWWWWW",
                 "WWWWWWWWWXXXXXXXXXX"],
        "brutes": 2,
        "lackeys": 1,
        "runners": 3,
        "snipers": 1,
        "queens": 1
    },    
    {
        "Grid": ["WWWWWWWWWWWWWWWWWWW",
                 "W        W        W",
                 "W        W    N   W",
                 "W  P     W        W",
                 "WW     WWWWW      W",
                 "W                 W",
                 "W                 W",
                 "W      WWWWW      W",
                 "W      WXXXW      W",
                 "W      WXXXW      W",
                 "W      WXXXW      W",
                 "W      WWWWW      W",
                 "W                 W",
                 "W                 W",
                 "WWWWWWW     WWWWWWW",
                 "W                 W",
                 "W        N        W",
                 "W                 W",
                 "WWWWWWWWWWWWWWWWWWW"],
        "brutes": 1,
        "lackeys": 1,
        "runners": 3,
        "snipers": 4,
        "queens": 0
    },
    {
        "Grid": ["XXXXXXXXWWWWWWWWWWW",
                 "XWWWWWWWWW        W",
                 "XW     WWW    N   W",
                 "XW  N  WWW        W",
                 "WW     WWW        W",
                 "WWW  WWWWW        W",
                 "WWW  WXXXW        W",
                 "WWW  WWWWW        W",
                 "W        W        W",
                 "W        W        W",
                 "W        WWW    WWW",
                 "W                 W",
                 "W                 W",
                 "W        W        W",
                 "WWW    WWW    P   W",
                 "W        W        W",
                 "W  N     W        W",
                 "W        W        W",
                 "WWWWWWWWWWWWWWWWWWW"],
        "brutes": 4,
        "lackeys": 4,
        "runners": 1,
        "snipers": 1,
        "queens": 1
    },
    {
        "Grid": ["XXXWWWWWWWWWWWWWXXX",
                 "XXWW           WWXX",
                 "XWW             WWX",
                 "WW       N       WW",
                 "W                 W",
                 "W                 W",
                 "W    N       N    W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "W                 W",
                 "WW       P       WW",
                 "XWW             WWX",
                 "XXWW           WWXX",
                 "XXXWWWWWWWWWWWWWXXX"],
        "brutes": 4,
        "lackeys": 4,
        "runners": 1,
        "snipers": 2,
        "queens": 2
    }
]
        
class Level:
    def __init__(self, game, level):
        self.game = game
        self.grid = level["Grid"]
        
        # increase enemies based off difficulty
        self.num_brutes = level["brutes"] + self.game.difficulty * 5
        self.num_lackeys = level["lackeys"] + self.game.difficulty * 3
        self.num_runners = level["runners"] + self.game.difficulty * 2
        self.num_snipers = level["snipers"] + self.game.difficulty * 2
        self.num_queens = level["queens"] + self.game.difficulty * 1
        
        self.total_enemies = 0
        
        self.walls = []
        self.enemynests = []

        # go over 2d array and create all objects (walls, ground, enemy nests, player spawn position)
        for k in range(len(self.grid[0])):
            for j in range(len(self.grid)):
                if self.grid[j][k] == 'W':
                    self.walls.append(Tile(self.game, WALL, (32 + k * 64, 32 + j * 64)))
                elif self.grid[j][k] == ' ':
                    self.walls.append(Tile(self.game, GROUND, (32 + k * 64, 32 + j * 64)))
                elif self.grid[j][k] == 'N':
                    # pass number of enemies to spawn to nest
                    self.enemynests.append(EnemyNest(self.game, GROUND, (32 + k * 64, 32 + j * 64),
                                                    self.num_brutes,
                                                    self.num_lackeys,
                                                    self.num_runners,
                                                    self.num_snipers,
                                                    self.num_queens))
                    self.total_enemies += (self.num_brutes + self.num_lackeys + self.num_runners + self.num_snipers + self.num_queens)
                elif self.grid[j][k] == 'P':
                    self.player_pos = (32 + k * 64, 32 + j * 64)
                    self.walls.append(Tile(self.game, GROUND, (32 + k * 64, 32 + j * 64)))
                elif self.grid[j][k] == 'X':
                    # create nothing
                    pass

class Menu:
    def __init__(self):
        self.image = menu_image
        self.image_width = menu_image.get_width()
        self.image_height = menu_image.get_height()
        self.delay = 0
        
    def draw(self, canvas):
        canvas.draw_image(self.image,
                         (self.image_width/2, self.image_height/2),
                         (self.image_width, self.image_height),
                         (WIDTH/2, HEIGHT/2),
                         (self.image_width, self.image_height))
        
        # draw score
        score = "SCORE: " + str(g.score)
        text_width = frame.get_canvas_textwidth(score, 24, FONT)
        canvas.draw_text(score, (WIDTH/2 - text_width/2, HEIGHT * 0.8), 24, 'White', FONT)

        # draw highscore
        highscore = "HIGHSCORE: " + str(g.highscore)
        text_width = frame.get_canvas_textwidth(highscore, 24, FONT)
        canvas.draw_text(highscore, (WIDTH/2 - text_width/2, HEIGHT * 0.85), 24, 'White', FONT)

        self.delay -= 1
        if self.delay <= 0:
            self.delay = 0
        
    def menu_clickhandler(self, pos):
        # delay prevents accidental spam click
        if self.delay == 0:
            frame.set_draw_handler(g.draw)
            g.new_game()
            self.delay = DEATH_MENU_DELAY

    def menu_draghandler(self, pos):
        # delay prevents accidental spam click
        if self.delay == 0:
            frame.set_draw_handler(g.draw)
            g.new_game()
            self.delay = DEATH_MENU_DELAY

class Overlay:
    def __init__(self, game, player):
        self.game = game
        self.player = player
    
    def draw_score(self, canvas):
        score = "Score: " + str(self.game.score)
        highscore = "Highscore: " + str(self.game.highscore)
        size = 16
        score_width = frame.get_canvas_textwidth(score, size, FONT)
        highscore_width = frame.get_canvas_textwidth(highscore, size, FONT)
        
        rect_right = WIDTH - 10
        rect_left = rect_right - 10 - score_width if score_width > highscore_width else rect_right - 10 - highscore_width
        rect_top = 10
        rect_bot = rect_top + 10 + size * 2
        
        # backing
        canvas.draw_polygon([(rect_left, rect_top),
                            (rect_right, rect_top),
                            (rect_right, rect_bot),
                            (rect_left, rect_bot)], 2, 'Black', 'White')   

        # score info
        canvas.draw_text(score, (rect_left + 5, (rect_top + rect_bot)/2.0), size, 'Black', FONT)
        canvas.draw_text(highscore, (rect_left + 5, rect_bot - 5), size, 'Black', FONT)
        
    def draw_health(self, canvas):
        # iterate over missing hearts and draw all, then draw amount of full hearts
        for i in range(self.player.max_health):
            canvas.draw_image(tile_set,
                              NOHEART['Center'],
                              (NOHEART['Width'], NOHEART['Height']),
                              (NOHEART['Width'] + i * (NOHEART['Width'] + 5), HEIGHT - NOHEART['Height']),
                              (NOHEART['Width'] * 1, NOHEART['Height'] * 1))        
        for i in range(self.player.health):
            canvas.draw_image(tile_set,
                              HEART['Center'],
                              (HEART['Width'], HEART['Height']),
                              (HEART['Width'] + i * (HEART['Width'] + 5), HEIGHT - HEART['Height']),
                              (HEART['Width'] * 1, HEART['Height'] * 1))

            
    def draw_inventory(self, canvas):
        rect_left = WIDTH - 220
        rect_right = rect_left + 75
        rect_top = HEIGHT - 100
        rect_bot = HEIGHT - 25
        
        # backing
        grey_backing_width = grey_backing.get_width()
        grey_backing_height = grey_backing.get_height()
        canvas.draw_image(grey_backing,
                          (grey_backing_width/2, grey_backing_height/2),
                          (rect_right + 95 - rect_left, rect_bot - rect_top),
                          (rect_right + 10, (rect_top + rect_bot)/2),
                          (rect_right + 100 - rect_left, rect_bot - rect_top))
        
        # draw selection box
        if self.player.current_slot == 0:
            canvas.draw_polygon([(rect_left, rect_top),
                                (rect_right, rect_top),
                                (rect_right, rect_bot),
                                (rect_left, rect_bot)], 8, 'Yellow')
            
        elif self.player.current_slot == 1:
            canvas.draw_polygon([(rect_left + 95, rect_top),
                                (rect_right+ 95, rect_top),
                                (rect_right+ 95, rect_bot),
                                (rect_left+ 95, rect_bot)], 8, 'Yellow')  
            
        # try to get gun info
        try:
            ammo = str(self.player.weapons[self.player.current_slot].ammo)
            mag = self.player.weapons[self.player.current_slot].mag
        except:
            ammo = ''
            mag = False
        
        mag_left = WIDTH - 30
        mag_right =  mag_left + 18
        mag_bot = HEIGHT - 35
        mag_top = mag_bot + 5

        # draw mag
        if mag:
            for i in range(mag):
                y_displace = i * 10    
                canvas.draw_polygon([(mag_left, mag_top - y_displace),
                                    (mag_right, mag_top - y_displace),
                                    (mag_right, mag_bot - y_displace),
                                    (mag_left, mag_bot - y_displace)], 1, 'Green', 'Green') 

        # draw ammo 
        ammobox_left = WIDTH - 35
        ammobox_right = ammobox_left + 30
        ammobox_top =  HEIGHT - 20
        ammobox_bot = ammobox_top + 15
        canvas.draw_polygon([(ammobox_left, ammobox_top), 
                             (ammobox_right, ammobox_top), 
                             (ammobox_right, ammobox_bot),
                             (ammobox_left, ammobox_bot)], 1, 'Black', 'Black')
        canvas.draw_text(ammo, (ammobox_right - 1 - frame.get_canvas_textwidth(ammo, 12, FONT), HEIGHT -8), 12, 'White', FONT)                  
        
        # if reloading draw a reloading message
        if self.player.reloading:
            message = 'Reloading'
            text_width = frame.get_canvas_textwidth(message, 14, FONT)
            canvas.draw_text(message, (WIDTH - text_width * 1.7, HEIGHT - 7), 14, 'Red', FONT)

        # draw weapons
        def draw_gun(image, draw_ratio):
            image_width = image.get_width()
            image_height = image.get_height()
            canvas.draw_image(image,
                                (image_width/2, image_height/2),
                                (image_width, image_height),
                                pos,
                                (image_width * draw_ratio, image_height * draw_ratio), -math.pi/8.0)               

        # goes over each inventory spot and draws if weapon available
        for i in range(2):
            if not i:
                # left pos
                pos = ((rect_left + rect_right)/2, (rect_top + rect_bot)/2)
            else:
                # right pos
                pos = (95 + (rect_left + rect_right)/2  , (rect_top + rect_bot)/2)
                
            if self.player.weapons[i].name == "pistol":
                draw_gun(PISTOL["Image"], PISTOL["InvRatio"])  
                
            if self.player.weapons[i].name == "shotgun":
                draw_gun(SHOTGUN["Image"], SHOTGUN["InvRatio"])

            elif self.player.weapons[i].name == "submac":
                draw_gun(SUBMAC["Image"], SUBMAC["InvRatio"])  

            elif self.player.weapons[i].name == "rifle":
                draw_gun(RIFLE["Image"], RIFLE["InvRatio"])  

            
class Game:
    def __init__(self):
        # debug (might be buggy but not intended to be on anyways)
        self.draw_hitboxes = False
        self.draw_positions = False
        self.draw_health = False
        self.draw_damage = False
        
        self.score = 0
        self.highscore = 0
    
    def new_game(self):
        global camera
        # create new objects and variables for everything
        self.level_num = 1
        self.difficulty = 0
        # level - 1 to get correct index
        self.level = Level(self, levels[self.level_num - 1])
        self.player = Player(self, self.level.player_pos)
        frame.set_keydown_handler(g.keydown_handler)
        frame.set_keyup_handler(g.keyup_handler)
        # create camera
        camera = Camera(self.player.pos)
        # equip and set slot
        self.player.current_slot = 0
        set_clickhandler(self.player.weapons[0].mouseclick_handler, self.player.weapons[0].mousedrag_handler)
        self.mouse_pos = Vec2d(WIDTH/2, HEIGHT/2)
        
        self.enemies = []
        self.projectiles = []
        self.items = []
        self.particles = []
        self.portal = None
        
        self.time = 0
        self.score = 0
        
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        
        self.overlay = Overlay(self, self.player)
    
    def new_level(self):
        global camera
        # only update level and clear entities
        self.level = Level(self, levels[self.level_num - 1])
        self.player.pos = Vec2d(*self.level.player_pos)
        camera = Camera(self.player.pos)
        
        set_clickhandler(self.player.weapons[self.player.current_slot].mouseclick_handler, 
                         self.player.weapons[self.player.current_slot].mousedrag_handler)
                
        self.enemies = []
        self.projectiles = []
        self.items = []
        self.particles = []
        self.portal = None

        self.mouse_pos = Vec2d(WIDTH/2, HEIGHT/2)
        
        self.up = False
        self.down = False
        self.right = False
        self.left = False        
    
    def draw(self, canvas):
        # count time (used for cooldowns etc)
        self.time += 1

        # draw background
        bg_width = background.get_width()
        bg_height = background.get_height()
        canvas.draw_image(background, (bg_width/2, bg_height/2),
                          (bg_width, bg_height),
                          (WIDTH/2 - camera.track.x/10, HEIGHT/2 - camera.track.y/10), 
                          (bg_width, bg_height))
        
        # update camera
        camera.get_playerpos(self.player.pos)
        camera.update()
        
        # go through all elements in level
        for wall in self.level.walls:
            wall.draw(canvas)
        for nest in self.level.enemynests:
            # check if nest is still active, and spawn
            if nest.total_spawn <= 0:
                nest.active = False
            elif self.time % NEST_SPAWN_DELAY == 0:
                nest.spawn()
            nest.draw(canvas)
        a = not all([nest.active for nest in self.level.enemynests])
        # if all nests are deactivated, and no enemies in stage, and no portal exists
        if a and not self.enemies and not self.portal:
            # create portal if no portal exisits and all enemies have been spawned and killed
            self.portal = Portal(self, WARP, self.player.pos.xy())
        if self.portal:
            self.portal.draw(canvas)
            # check if player is on portal
            if self.portal.warp(self.player):
                # check if warp time is counted down
                if self.portal.warp_time <= 0:
                    # check if the level is also the last level
                    if self.level_num % len(levels) == 0:
                        # set level back to 1 and increase difficulty
                        self.level_num = 1
                        self.difficulty += 1
                    else:
                        # otherwise just increment level
                        self.level_num += 1
                    # create new level, and break draw loop
                    self.new_level()
                    return
                
                # count down warp time
                self.portal.warp_time -= 1

        self.player.item_hits = []        
        for item in self.items:
            # remove items if they are old or picked up
            if item.lifespan <= 0 or item.picked_up:
                self.items.remove(item)
            else:
                item.update()
                item.draw(canvas)
                # add items that collied with player to hit list
                hit = item.collide(self.player)
                if hit:
                    self.player.item_hits.append(hit) 
        
        for hit in self.player.item_hits:
            # do not remove if no health or ammo can be gained
            if hit.name == "health":
                # make sure adding health would not go over max
                if self.player.health + HEALTH_RESTORE <= self.player.max_health:
                    self.player.health += HEALTH_RESTORE
                    self.items.remove(hit)
            elif hit.name == "ammo":
                try:
                    self.player.weapons[self.player.current_slot].ammo += AMMO_RESTORE
                    self.items.remove(hit)
                except:
                    pass

        for enemy in self.enemies:
            enemy.update()
            if enemy.collide(self.player):
                # damage player if hit
                self.player.get_hit(enemy)
            enemy.draw(canvas)
            # if dead give score and spawn ammo and maybe weapon
            if enemy.health <= 0:
                if enemy.type == 0:
                    self.score += 100
                elif enemy.type == 1:
                    self.score += 150
                elif enemy.type == 2:
                    self.score += 300
                enemy.drop()
                # remove enemy
                self.enemies.remove(enemy)
        
        # update projectiles
        for projectile in self.projectiles:
            if projectile.despawn:
                self.projectiles.remove(projectile)
            else:
                projectile.update()
                projectile.draw(canvas)

                # check if shot by player or by enemy
                if projectile.player_bullet:
                    for enemy in self.enemies:
                        # check collisions with enemies
                        if projectile.collide(enemy):
                            enemy.health -= projectile.damage
                            # despawn projectile so it wont collide again
                            projectile.despawn = True         
                else:
                    # check if projectile hits player
                    if projectile.collide(self.player):
                        self.player.health -= projectile.damage
                        projectile.despawn = True
         
        if self.player.health <= 0:
            # if player dies, open menu and exit out of draw
            self.player.stop_autofire()
            open_menu()
            return

        # update and draw player    
        self.player.update()
        self.player.draw(canvas)

        # update highscore if greater than previous
        if self.score > self.highscore:
            self.highscore = self.score   
        
        # debug stats
        if self.draw_hitboxes or self.draw_positions or self.draw_health or self.draw_damage:
            self.player.draw_stats(canvas, self.draw_hitboxes, self.draw_positions, self.draw_health, False)
            for item in self.items:
                item.draw_stats(canvas, 
                                hitbox = self.draw_hitboxes, 
                                pos = self.draw_positions)
            for projectile in self.projectiles:
                projectile.draw_stats(canvas, 
                                      hitbox = self.draw_hitboxes, 
                                      pos = self.draw_positions, 
                                      damage = self.draw_damage)
            for enemy in self.enemies:
                enemy.draw_stats(canvas, 
                                 hitbox = self.draw_hitboxes, 
                                 pos = self.draw_positions, 
                                 health = self.draw_health)
            
        # draw overlay    
        self.overlay.draw_score(canvas)
        self.overlay.draw_health(canvas)
        self.overlay.draw_inventory(canvas)
        canvas.draw_image(crosshair,
                          (200/2, 200/2),
                          (200, 200),
                          self.mouse_pos.xy(),
                          (200/5, 200/5))
    
    def keydown_handler(self, key):
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
            self.up = True
        elif key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = True
        elif key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = True
        elif key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = True
        elif key == simplegui.KEY_MAP['1']:
            self.player.current_slot = 0
            self.player.equip(0)
        elif key == simplegui.KEY_MAP['2']:
            self.player.current_slot = 1
            self.player.equip(1)
        elif key == simplegui.KEY_MAP['r']:
            self.player.reload()
        elif key == simplegui.KEY_MAP['f']:
            self.player.pickup()
        elif key == simplegui.KEY_MAP['q']:
            self.player.quick_switch() 

    def keyup_handler(self, key):
        # turns off so player does not move
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
            self.up = False
        elif key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
        elif key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = False
        elif key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = False 

class Nothing:
    # does nothing (used if character has no weapon)
    # still updates mouse position and players direction
    def mouseclick_handler(pos):
        g.mouse_pos = Vec2d(*pos)
        g.player.set_aim(Vec2d(*pos))
    
    def mousedrag_handler(pos):
        g.mouse_pos = Vec2d(*pos)
        g.player.set_aim(Vec2d(*pos))

def open_menu():
    frame.set_draw_handler(menu.draw)
    frame.set_mouseclick_handler(menu.menu_clickhandler)
    frame.set_mousedrag_handler(menu.menu_draghandler)

# sets mouseclick and mouse drag to the input function
def set_clickhandler(mouseclick = Nothing.mouseclick_handler, mousedrag = Nothing.mousedrag_handler):
    frame.set_mouseclick_handler(mouseclick)
    frame.set_mousedrag_handler(mousedrag)

frame = simplegui.create_frame("Game", WIDTH, HEIGHT)

# create game
g = Game()
# create menu
menu = Menu()
# open the menu
open_menu()

# start frame
frame.set_canvas_background("White")
frame.start()