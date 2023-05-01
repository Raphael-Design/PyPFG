vertex_shader_src = '''
#version 410 core
layout(location = 0) in vec3 vertexPosition_modelspace;

// Output data ; will be interpolated for each fragment.
out vec2 fragmentCoord;

void main(){
  gl_Position = vec4(vertexPosition_modelspace, 1);
  fragmentCoord = vec2(vertexPosition_modelspace.x, vertexPosition_modelspace.y);
}
'''

intro = '''
#version 410 core

in vec2 fragmentCoord;
out vec3 color;

uniform dmat3 transform;

uniform int max_iters = 1000;


vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}


vec3 map_color(int i, float r, float c) {
    float di = i;
    float zn = sqrt(r + c);
    float hue = (di + 1 - log(log2(abs(zn))))/max_iters;
    return hsv2rgb(vec3(hue, 0.8, 1));
}

void main(){
    dvec3 pointCoord = dvec3(fragmentCoord.xy, 1);
    pointCoord *= transform;
    double cx = pointCoord.x;
    double cy = pointCoord.y;
    int iter = 0;
    double zx = 0;
    double zy = 0;
    while (iter < max_iters) {

'''
end = '''
        if (zx*zx + zy*zy > 4.0) {
            break;
        }
        iter += 1;
    }
    if (iter == max_iters) {
        color = vec3(0,0,0);
    } else {
        color = map_color(iter, float(zx*zx), float(zy*zy));
    }
}
'''

types = ["""
        double nzx = zx * zx - zy * zy + cx;
        double nzy = 2 * zx * zy - cy;
        zx = nzx;
        zy = nzy;""",
        """
        double nzx = (2 * zx * zx - zy * zy) + cx;
        double nzy = (2 * zy * zx + zx * zy) + cy;
        zx = nzx;
        zy = nzy;
""",
"""
        double nzx = zx * zx - zy * zy + cx;
        double nzy = abs(zx) * zy * 2 + cy;
        zx = nzx;
        zy = nzy;
"""]