try:
    from manager import *
    import struct
    import traceback

    from pygame.locals import *

    import moderngl

    regularFrag = """
    #version 300 es
    precision mediump float;
    uniform sampler2D Texture;
    in vec2 v_text;
    
    out vec3 f_color;
    void main(){
        f_color = texture(Texture,v_text).rgb;
    }
    """

    crtFrag = """#version 300 es
    precision mediump float;
    uniform sampler2D Texture;
    
    #define POST_PROCESS
    
    vec2 CRTCurveUV( vec2 uv, float str )
    {
        uv = uv * 2.0 - 1.0;
        vec2 offset = ( str * abs( uv.yx ) ) / vec2( 6.0, 4.0 );
        uv = uv + uv * offset * offset;
        uv = uv * 0.5 + 0.5;
        return uv;
    }
    
    out vec4 fragColor;
    in vec2 v_text;
    void main() {
        vec2 baseUV = vec2(v_text.x/1.0,v_text.y/1.0);
    
    #ifdef POST_PROCESS
        vec2 uv = CRTCurveUV( baseUV, 0.5 );
    
        // chromatic abberation
        float caStrength    = 0.003;
        vec2 caOffset       = uv - 0.5;
        //caOffset = vec2( 1.0, 0.0 ) * 0.3;
        vec2 caUVG          = uv + caOffset * caStrength;
        vec2 caUVB          = uv + caOffset * caStrength * 2.0;
    
        vec3 color;
        color.x = texture( Texture, uv ).r;
        color.y = texture( Texture, caUVG ).g;
        color.z = texture( Texture, caUVB ).b;
    
    
        uv = CRTCurveUV( baseUV, 1.0 );
        if ( uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0 )
        {
            color = vec3( 0.0, 0.0, 0.0 );
        }
        float vignette = uv.x * uv.y * ( 1.0 - uv.x ) * ( 1.0 - uv.y );
        vignette = clamp( pow( 16.0 * vignette, 0.3 ), 0.0, 1.0 );
        color *= vignette * 1.1;
    
    #else
        vec3 color = texture( Texture, baseUV ).rgb;
    
    #endif
    
        fragColor = vec4(color, 1.0);
    }"""

    usingShader = crtFrag if Cs.CRT else regularFrag

    # try:
    pygame.init()
    clock = pygame.time.Clock()
    VIRTUAL_RES = (1280, 720)
    REAL_RES = (1280, 720)

    screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
    if Cs.WINDOWED:
        pygame.display.set_mode(REAL_RES, DOUBLEBUF | OPENGL)
    else:
        pygame.display.set_mode(REAL_RES, DOUBLEBUF | OPENGL | FULLSCREEN)
    pygame.mouse.set_visible(False)
    player1 = GameEntities.PinkSpaceship(numpy.array([Cs.RESOLUTION[0] / 2. - 400, Cs.RESOLUTION[1] / 2 - 400]), 0,
                                         {'THRUST': pygame.K_w, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d,
                                          'SHOOT': pygame.K_SPACE})
    player2 = GameEntities.BlueSpaceship(numpy.array([Cs.RESOLUTION[0] / 2. + 400, Cs.RESOLUTION[1] / 2 + 400]), 0,
                                         {'THRUST': pygame.K_UP, 'LEFT': pygame.K_LEFT, 'RIGHT': pygame.K_RIGHT,
                                          'SHOOT': pygame.K_RCTRL})
    bulletsPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Bullet')
    bulletImageFilePaths = bulletsPath.rglob('*[0-9].png')
    bulletCache = {pth: pygame.image.load(str(pth)).convert_alpha() for pth in bulletImageFilePaths}
    healthBarCache: Dict[str, imageGroup.ImageGroup] = {
        'Pink': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Pink/Solid'),
                                      lambda n: pygame.image.load(str(n)).convert_alpha()),
        'Blue': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Blue/Solid'),
                                      lambda n: pygame.image.load(str(n)).convert_alpha())}


    def scaler(inSurface: pygame.Surface):
        dim = inSurface.get_rect()
        return pygame.transform.smoothscale(inSurface, (
            floor(dim.w * Cs.healthBarScaleConst[0]), floor(dim.h * Cs.healthBarScaleConst[1])))


    for model in healthBarCache:
        healthBarCache[model].transformAll(scaler)
    if Cs.BLOOM:
        bloomHealthBarCache: Dict[str, imageGroup.ImageGroup] = {
            'Pink': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Pink/Bloom'),
                                          lambda n: pygame.image.load(str(n)).convert_alpha()),
            'Blue': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Blue/Bloom'),
                                          lambda n: pygame.image.load(str(n)).convert_alpha())}
        for model in bloomHealthBarCache:
            bloomHealthBarCache[model].transformAll(scaler)

        man = Manager(screen, bulletCache, healthBarCache, player1, player2, bloomHealthCache=bloomHealthBarCache)
    else:
        man = Manager(screen, bulletCache, healthBarCache, player1, player2)
    done = False

    ctx = moderngl.create_context()

    texture_coordinates = [0, 1, 1, 1,
                           0, 0, 1, 0]

    world_coordinates = [-1, -1, 1, -1,
                         -1, 1, 1, 1]

    render_indices = [0, 1, 2,
                      1, 2, 3]

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

        fragment_shader=usingShader)

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


    while not done:
        if Cs.CRT:
            screen.fill((40, 40, 40))
        else:
            screen.fill((0, 0, 0))
        man.completeCycle()
        render()
        clock.tick(Cs.FPS)
except:
    with open('Traceback.txt', 'w') as file:
        print(traceback.format_exc(), file=file)
    sys.exit()
