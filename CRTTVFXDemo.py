import struct
import pygame
from pygame.locals import *

import moderngl
from math import sin
from time import time

pygame.init()
START = time()
FPS = 250
clock = pygame.time.Clock()

VIRTUAL_RES = (640, 360)
REAL_RES = (1280, 720)

screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
pygame.display.set_mode(REAL_RES, FULLSCREEN | DOUBLEBUF | OPENGL)

ctx = moderngl.create_context()

texture_coordinates = [0, 1, 1, 1,
                       0, 0, 1, 0]

world_coordinates = [-1, -1, 1, -1,
                     -1, 1, 1, 1]

render_indices = [0, 1, 2,
                  1, 2, 3]
with open('frag2.glsl', 'r') as File:
    frag = File.read()
oldFrag = '''
#version 300 es
precision mediump float;
uniform sampler2D Texture;

out vec4 color;
in vec2 v_text;
void main() {
  vec2 center = vec2(0.5, 0.5);
  vec2 off_center = v_text - center;

  off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(2.5));

  vec2 v_text2 = center+off_center;

  if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
      v_text2.y > 1.0 || v_text2.y < 0.0){
    color=vec4(0.0, 0.0, 0.0, 1.0);
  } else {
    color = vec4(texture(Texture, v_text2).rgb, 1.0);
    float fv = fract(v_text2.y * float(textureSize(Texture,0).y));
    fv=min(1.0, 0.8+0.5*min(fv, 1.0-fv));
    color.rgb*=fv;
  }
}
'''
prog = ctx.program(
    vertex_shader='''
#version 300 es
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}
''',

    fragment_shader=frag)

# prog['iResolution'].value = 1280.,720.
# print(prog['iResolution'].value)

screen_texture = ctx.texture(
    VIRTUAL_RES, 3,
    pygame.image.tostring(screen, "RGB", 1))

screen_texture.repeat_x = False
screen_texture.repeat_y = False

vbo = ctx.buffer(struct.pack('8f', *world_coordinates))
uvmap = ctx.buffer(struct.pack('8f', *texture_coordinates))
ibo = ctx.buffer(struct.pack('6I', *render_indices))

vao_content = [
    (vbo, '2f', 'vert'),
    (uvmap, '2f', 'in_text')
]

vao = ctx.vertex_array(prog, vao_content, ibo)


def render():
    
    texture_data = screen.get_view('1')
    screen_texture.write(texture_data)
    ctx.clear(14 / 255, 40 / 255, 66 / 255)
    screen_texture.use()
    vao.render()
    pygame.display.flip()


# MAIN LOOP

done = False
st = time()

while not done:
    t = time() - st
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
    x = 50 * sin(2500 * t)

    screen.fill((0, 20, 255))
    pygame.draw.circle(screen, (0, 0, 0), (int(100 + x), 100), 20)
    pygame.draw.circle(screen, (0, 0, 200), (0, 0), 10)
    pygame.draw.circle(screen, (200, 0, 0), (160, 120), 30)
    pygame.draw.line(screen, (250, 250, 0), (0, 120), (160, 0))

    render()
    print(clock.get_fps())
    clock.tick(FPS)
