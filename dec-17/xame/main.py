import pyglet
import random
import shutil
import random
from random import randrange as rr
from opensimplex import OpenSimplex
import time as clock
import os
import pickle
import sys
import threading
black = (0,0,0)
white = (255,255,255)
def tren(x,y,t):
    label = pyglet.text.Label(str(t),
              font_name='Times New Roman',
              font_size=36,
              x=window.width//2, y=window.height//2)
    label.draw
def gen_w(ox,oy):
    for i in range(10):
        try:
            gen(ox,oy)
            return True
        except:
            raise
            return False
def save_dump(ox,oy,ch):
    ox,oy = float(ox),float(oy)
    name = 'world/chunks/'
    root = '{0}_{1}.pkl'.format(ox,oy)
    name += root
    cfile = open(name,'wb')
    pickle.dump(ch, cfile, protocol = -1)
    cfile.close()
def save_all():
    global cchunks
    global blocks
    for pl,pos in enumerate(cchunks):
        save_dump(pos[0],pos[1],blocks[pl])
def gen(ox,oy):
    global blocks
    global cchunks
    global structs
    root = '{0}_{1}.pkl'.format(ox,oy)
    name = 'world/chunks/'+root
    rel = root in os.listdir('world/chunks')
    #rel = False
    if rel:
        cfile = open(name,'rb')
        chunk = pickle.load(cfile)
        cchunks.append([ox,oy])
        blocks.append(chunk)
        return 0
    else:
        cchunks.append([ox,oy])
        cfile = open(name,'wb')
        chunk = []
        blocks.append(chunk)
        spec = world_noise_amp
        for i in range(ws[0]*ws[1]):
            dirs = [
                [
                    [0,0],
                    [0,-1],
                ],
                [
                    [0,0],
                ]
            ]
            cpos = False
            nk = dirs
            for ypk,dirt in enumerate(dirs):
                for pl,k in enumerate(dirt):
                    x = (i%ws[0]+ox)+k[0]
                    y = (i//ws[1]+oy)+k[1]
                    if k == [0,0] and ypk == 0:
                        cpos = [x,y]
                    perams = [1,x*0.1*spec[0],y*0.1*spec[0]]
                    perams[1] *= 1.5
                    perams[2] *= 1.5
                    nk[ypk][pl] = world_gen[ypk].noise2d(x=perams[1],y=perams[2])
            if nk[0][0] > 0:
                if nk[0][1] < 0:
                    dorp_block('base/grass',xover=cpos,dump=0)
                else:
                    if nk[1][0] > 0.4:
                        dorp_block('base/dirt',xover=cpos,dump=0)
                    else:
                        dorp_block('base/stone',xover=cpos,dump=0)
        pickle.dump(chunk, cfile, protocol = -1)
        cfile.close()
    return 0
#block renderer
def rblock(blockin,ter=True,isplayer=False):
    global place
    global size
    global sprt
    x,y,spnam,curchunk = blockin
    mx,my = size[0]+sclx,size[1]+sclx
    ox,oy = x,y
    x,y = (x * sclx + size[0] / 2) - place[0]*sclx, (y * sclx + size[1] / 2)- place[1]*sclx
    if x < mx and x > -sclx and y < my and y > -sclx:
        y = size[1]-y
        sprt[spnam].blit(x,y)
def rtext(pos,word,size=24,ax='center',ay='center'):
    label = pyglet.text.Label(word,
                          font_name='Times New Roman',
                          font_size=size,
                          x=pos[0], y=pos[1],
                          anchor_x=ax, anchor_y=ay)
    label.draw()
#detects if a hitbox has collision
def hitany(hitbox):
    global sblk
    out = {'up':0,'down':0,'left':0,'right':0}
    hx,hy = hitbox
    for chunk in blocks:
        for block in chunk:
            x,y,*ignore = block
            inline = []
            inline.append(x-0.5 < hx < x+0.5)
            inline.append( y-1  < hy < y)
            out['down'] += inline[0] and inline[1]
            inline = inline[:-1]
            inline.append( y  < hy < y+1)
            out['up'] += inline[0] and inline[1]
            inline = inline[1:]
            inline.append(x-1 < hx < x)
            out['left'] += inline[0] and inline[1]
            inline = inline[:-1]
            inline.append(x < hx < x+1)
            out['right'] += inline[0] and inline[1]
    return out
def fallthrough():
    return {'up':0,'down':0,'left':0,'right':0}
class being():
    def __init__(self,place,*args):
        self.place = place
        self.fallspeed = 0
        self.tjump = 0
        self.jumpspeed = 0.1
        self.klr = 0
        self.tjk = 2
        self.grav = 3
        self.flying = False
        self.hits = {'left':False,'right':False}
        self.mov = {'up':False,'down':False,'left':False,'right':False}
        self.accu = 3
        self.justjumped = False
        self.walkspeed = 2
        if len(args) == 0:
            self.color = [255,255,255]
        else:
            self.color = args[0]
        self.fs = 5
    def jump(self):
        global time
        self.justjumped = False
        if self.tjump != 0:
            if self.hits['down']:
                self.fallspeed = 0
                self.fallspeed -= 1 * self.tjump * self.tjk
                self.justjumped = True
                #print(self.fallspeed)
    def move(self):
        self.jump()
        self.lr()
    def lr(self):
        global time
        self.place[0] -= self.klr * time / self.accu * self.walkspeed
    def render(self):
        rblock(self.place+['base/skin']+[[0,0]],ter=False)
    def walk(self):
        if self.mov['left']:
            self.klr += 0.003 * time
        if self.mov['right']:
            self.klr += -0.003 * time
        self.klr *= 0.98
        self.tjump = self.jumpspeed if self.mov['up'] else 0
        #print([self.mov[i] for i in self.mov])
        if self.hits['left'] :
            self.klr = 0.01
        if self.hits['right'] :
            self.klr = -0.01
        if self.hits['down'] or self.hits['up']:
            if self.hits['down'] and self.fallspeed > 0.02:
                pass
                #print(self.fallspeed)
            self.fallspeed = 0
        else:
            jj = False
        self.move()
        if not self.hits['down']:
            self.fallspeed += 0.005 * time * self.grav / self.accu
        self.place[1] += self.fallspeed * time / self.accu
        self.tjump = False
    def mfly(self):
        if self.mov['up']:
            self.place[1] -= 0.5 / self.accu * time
        elif self.mov['down']:
            self.place[1] += 0.5 / self.accu * time
        if self.mov['left']:
            self.place[0] -= 0.5 / self.accu * time
        if self.mov['right']:
            self.place[0] += 0.5 / self.accu * time
    def update(self):
        global time
        self.render()
        for i in range(self.accu):
            self.hits = hitany(place)
            if not self.flying:
                self.walk()
            else:
                self.mfly()
def ostruct(fil):
    name = fil+'.obj'
    obj = open(name).read()
    out = []
    for i in obj.split('\n'):
        j = i.split(' ')
        if len(j) == 3:
            j[0],j[1] = int(j[0]),int(j[1])
            out.append(j)
    return out
def worldseed(seed):
    global world_gen
    random.seed(seed)
    world_gen = [OpenSimplex(seed=rr(10**10)) for i in range(100)]
def re_world():
    global cchunks
    global blocks
    cchunks = []
    blocks = []
    shutil.rmtree('world/chunks')
    os.mkdir('world/chunks')
    init_seed = rr(10**7)
    random.seed(init_seed)
    worldseed(rr(10**7))
def genops():
    global world_seed
    global world_noise_amp
    world_seed = rr(10**7)
    init_seed = 0
    noise_scale_x = .5
    noise_scale_y = .5
    noise_scale = False
    chunk_size = 16
    exec(open('world/gen.txt').read())
    if noise_scale == False:
        world_noise_amp = [noise_scale_x,noise_scale_y]
    else:
        world_nose_amp = noise_scale
    chs = chunk_size
    random.seed(init_seed)
    if open('world/dat/seed.txt').read() != str(world_seed):
        re_world()
    open('world/dat/seed.txt','w').write(str(world_seed))
chs = 12
ws = [chs]*2
place = [i/2 for i in ws]
texture_pack = 'assets'
genops()

size = [800,800]
window = pyglet.window.Window(size[0],size[1],fullscreen=False,resizable=False)
#size = user_io.mouse.screen_size()

blocks = []
cchunks = []
keys = []
scl = 0.2
vscl = (size[0]+size[1])/1800

sclx = 10/scl*vscl
time = 1
pause = False
genday = 0
td = 60
wmiddle = [(i / sclx // 2) for i in size]
wsizeb = [(i / sclx) for i in size]
textures = []
fblocktyps = ['base/wood']
curhold = 0
for direct in  os.listdir(texture_pack):
    if direct[0] == '.':
        continue
    foldasset = texture_pack+'/'+direct
    ilist = os.listdir(foldasset)
    textures += [foldasset+'/'+i for i in ilist if os.path.isfile(foldasset+'/'+i) and i[0] != '.']

player = being(place)
player.fly = False
structs = ['tree','boulder']
#structs = [ostruct(i) for i in structs]
sprt = {}
for img in textures:
    split = img.split('/')
    texture_name = split[1:]
    texture_name[-1] = texture_name[-1].split('.')[0]
    gamn = ''.join(i+'/' for i in texture_name)[:-1]
    sprt[gamn] = pyglet.image.load(img)
    sprt[gamn].texture.width = int(sclx)+1
    sprt[gamn].texture.height = int(sclx)+1
    sprt[split[-1].split('.')[0]] = sprt[gamn]
mpos = [0,0]
mouseEvents = []
buttons = 0
@window.event
def on_resize(width, height):
    global size
    global vscl
    global sclx
    global wmiddle
    global wsizeb
    size = [width,height]
    vscl = (size[0]+size[1])/1800
    sclx = 10/scl*vscl
    wmiddle = [(i / sclx // 2) for i in size]
    wsizeb = [(i / sclx) for i in size]

    clock.sleep(0.1)
def dorp_block(btype,xover=False,dump=True):
    global mpos
    global chs
    global blocks
    if xover == False:
        xe = wmiddle
        x,y = mpos
        ppos = player.place
        mrx = ppos
        mp2 = mpos
        mp2 = [i / sclx - xe[pl] for pl,i in enumerate(mp2)]
        mp3 = mp2
        mp3[0] = mp3[0] + ppos[0]
        mp3[1] = - mp3[1] + ppos[1]
        mp3[1] = mp3[1] // 1 + 1
        mp3[0] = mp3[0] // 1
        mp3[0] = int(mp3[0])
        mp3[1] = int(mp3[1])
    else:
        mp3 = xover
    fl = []
    for pl in mp3:
        h = (pl) // chs * chs
        fl.append(h)
    ind = cchunks.index(fl)
    if ind < len(blocks):
        if len(blocks[ind]) != 0:
            cbl = [i[:2] for i in blocks[ind]]
        else:
            cbl = []
    else:
        return
    if mp3 in cbl:
        bind = cbl.index(mp3)
        tob = blocks[ind][bind][2]
        if not tob in fblocktyps:
            pass
            #fblocktyps.append(tob)
        del blocks[ind][bind]
        root = '%s_%s.pkl' % tuple(fl)
        name = 'world/chunks/'+root
    else:
        global curhold
        typ = btype
        nb = mp3+[typ]+[fl]
        blocks[ind].append(nb)
        root = '%s_%s.pkl' % tuple(fl)
        name = 'world/chunks/'+root
    if dump:
        save_dump(fl[0],fl[1],blocks[ind])

@window.event
def on_key_press(symbol, modifiers):
    global player
    global keys
    if symbol == pyglet.window.key.Q:
        save_all()
        exit()
    elif symbol == pyglet.window.key.R:
        keys = []
    elif symbol == pyglet.window.key.L:
        re_world()
    else:
        if symbol >= 48 and symbol <= 57:
            #print(symbol-48)
            pass
        keys.append(symbol)
    return
@window.event
def on_key_release(symbol, modifiers):
    global keys
    if symbol in keys:
        del keys[keys.index(symbol)]
    return
@window.event
def on_mouse_press(x, y, button, modifiers):
    global mpos
    global mouseEvents
    mouseEvents.append([[x,y],button])
    return
@window.event
def on_mouse_release(x, y, button, modifiers):
    return
def rchunk(chunk):
    for block in chunk:
        rblock(block)
def render():
    global blocks
    for chunk in blocks:
        rchunk(chunk)
def on_draw(xe):
    global td
    global pause
    global window
    global keys
    global buttons
    global mpos
    global mouseEvents
    t = clock.time()
    window.clear()
    render()
    for e in mouseEvents:
        mpos = e[0]
        dorp_block('base/stone')
    mouseEvents = []
    player.mov['up'] = pyglet.window.key.W in keys
    player.mov['down'] = pyglet.window.key.S in keys
    player.mov['left'] = pyglet.window.key.A in keys
    player.mov['right'] = pyglet.window.key.D in keys
    vchs = 60//chs
    for i in range(vchs*vchs):
        x,y = player.place
        x,y = x//chs,y//chs
        xs,ys = i//vchs - int(vchs/2), i%vchs - int(vchs/2)
        x,y = x+xs, y+ys
        x,y = x*chs,y*chs
        if not [x,y] in cchunks:
            if 1:
                gen(x,y)
    threads = []
    for i in cchunks:
        if abs(i[0] - player.place[0]) < 50 and abs(i[1] - player.place[1]) < 50:
            pass
        else:
            inf = cchunks.index(i)
            del blocks[inf]
            del cchunks[inf]
    player.update()
    colt = 0
    global loops
    global tot
    td = int(1/(clock.time()-t))
    rtext([100,80],str(int(td)),size=12)
    return 0
tot = 0
loops = 1
#window.push_handlers(on_key_press, on_mouse_press)
pyglet.clock.schedule_interval(on_draw,1/60.0)
pyglet.app.run()
