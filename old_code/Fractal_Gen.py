from PIL import Image
import numpy as np

height = 3000
width = 3000
channels = 3

array_shape = (height, width, channels)
pixel_buffer = np.full(array_shape, 255, np.uint8)

def complex_matrix(xmin, xmax, ymin, ymax, pixel_density):
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j

def paint_pixel(x, y, color):
    real_x = x
    real_y = y
    pixel_buffer[real_y][real_x] = color
    
#def carthesian_coordinates(x,y):
    #cartesianx = scalefactor * (screenx - (screenwidth / 2))
    #cartesiany = -scalefactor* (screeny - (screenheight / 2))
    
def iterate_fractal(x0, y0, n_iter):
    #vec2 uv = (fragCoord-.5*iResolution.xy)/iResolution.y;
    r_x0 = x0 - ((0.5*width)/height)
    r_y0 = y0 - ((0.5*height)/height)
    r_x0 =  r_x0 + 0.5
    r_x0 = r_x0 * 2
    r_y0 = r_y0 * 2
    #(xn+1, yn+1) = ((x^2-y^2), (2xy)) + (x0, y0)
    n_x = r_x0
    n_y = r_y0
    for a in range(n_iter):
        n_x = ( (n_x*n_x) - (n_y*n_y) ) + r_x0
        n_y = 2 * ( n_x * n_y ) + r_y0
        if n_x < 0 or n_x > width or n_y < 0 or n_y > height:
            return ((a/n_iter*a)*0.5, (a/n_iter*a)*0.5, ((a/n_iter*a)+0.15)*1.4)
    return (0,0,0)
    
def julia_simple(x0, y0, n_iter):
    n_x = 0.1 * (x0 - (width/2))
    n_y = -0.1 * (y0 - (height/2))
    for a in range(n_iter):
        n_x = n_x*n_x
        n_y = n_y*n_y
        exit = a
        if n_x > height or n_y > width:
            break
    if exit >= n_iter-1:
        return (255,0,0)
    else:
        return (0,0,0)
    


for x in range(height):
    for y in range(width):
        color = julia_simple(x,y,1000)
        paint_pixel(x,y,color)

image = Image.frombytes("RGB", (width, height), pixel_buffer)
image.save("image_.png", "PNG")
#image_blank.save(image_filename)

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


fragmentshader = '''
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
        double nzx = zx * zx - zy * zy + cx;
        double nzy = 2 * zx * zy - cy;
        zx = nzx;
        zy = nzy;""",
        """
        double nzx = (2 * zx * zx - zy * zy) + cx;
        double nzy = (2 * zy * zx + zx * zy) + cy;
        zx = nzx;
        zy = nzy;
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