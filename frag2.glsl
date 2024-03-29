#version 300 es
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
    color *= vignette * 0.9;

#else
    vec3 color = texture( Texture, baseUV ).rgb;

#endif

    fragColor = vec4(color, 1.0);
}