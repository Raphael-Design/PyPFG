import glfw
import OpenGL.GL as gl
import numpy
import old_code.shader as sh
from PIL import Image
import time
from multiprocessing import Pool


def make_shader(shader_type, src):
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, src)
    gl.glCompileShader(shader)
    status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if status == gl.GL_FALSE:
        # Note that getting the error log is much simpler in Python than in C/C++
        # and does not require explicit handling of the string buffer
        strInfoLog = gl.glGetShaderInfoLog(shader).decode('ascii')
        strShaderType = ""
        if shader_type is gl.GL_VERTEX_SHADER:
            strShaderType = "vertex"
        elif shader_type is gl.GL_GEOMETRY_SHADER:
            strShaderType = "geometry"
        elif shader_type is gl.GL_FRAGMENT_SHADER:
            strShaderType = "fragment"

        raise Exception("Compilation failure for " + strShaderType + " shader:\n" + strInfoLog)

    return shader


def make_program(shader_list):
    program = gl.glCreateProgram()

    for shader in shader_list:
        gl.glAttachShader(program, shader)

    gl.glLinkProgram(program)

    status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if status == gl.GL_FALSE:
        # Note that getting the error log is much simpler in Python than in C/C++
        # and does not require explicit handling of the string buffer
        strInfoLog = gl.glGetProgramInfoLog(program)
        raise Exception("Linker failure: \n" + strInfoLog)

    for shader in shader_list:
        gl.glDetachShader(program, shader)

    return program

def main():
    
    #Initialize Lib
    if not glfw.init():
        return
    
    #Configurations
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.DOUBLEBUFFER, gl.GL_FALSE)
    glfw.window_hint(glfw.SAMPLES, 32)
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    width = 1920
    height = 1080
    aspect = 1.0 * width / height

    #Create Window
    window = glfw.create_window(width, height, "TCC", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    fragment_shader_src = sh.intro + sh.types[0] + sh.end
    vertex_shader = make_shader(gl.GL_VERTEX_SHADER, sh.vertex_shader_src)
    fragment_shader = make_shader(gl.GL_FRAGMENT_SHADER, fragment_shader_src)

    program = make_program([vertex_shader, fragment_shader])

    
    vert_values = numpy.array([-1, -1 * aspect, 0,
                               1, -1 * aspect, 0,
                               -1, 1 * aspect, 0,
                               -1, 1 * aspect, 0,
                               1, -1 * aspect, 0,
                               1, 1 * aspect, 0,
                               ], dtype='float64')
    
    
    vert_array = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vert_array)

    vert_buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vert_buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vert_values, gl.GL_STATIC_DRAW)
    
    gl.glUseProgram(program)    

    gl.glEnableVertexAttribArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vert_buffer)
    gl.glVertexAttribPointer(0, 3, gl.GL_DOUBLE, gl.GL_FALSE, 0, None)
    
    transform_loc = gl.glGetUniformLocation(program, 'transform')
    max_iters_loc = gl.glGetUniformLocation(program, 'max_iters')
    
    state = {
        'zoom': 1,
        'pos_x': -0.7600189058857209,
        'pos_y': 0.0799516080512771,
        'max_iters': 100,
        'tipo': 1
    }
    
    time_before = glfw.get_time()
    

    for x in range(len(sh.types)):
        
        fragment_shader_src = sh.intro + sh.types[x] + sh.end
        vertex_shader = make_shader(gl.GL_VERTEX_SHADER, sh.vertex_shader_src)
        fragment_shader = make_shader(gl.GL_FRAGMENT_SHADER, fragment_shader_src)

        new_program = make_program([vertex_shader, fragment_shader])
        gl.glUseProgram(new_program)
            
        zoom = state['zoom']
        pos_x = state['pos_x']
        pos_y = state['pos_y']
            
        gl.glUniformMatrix3dv(transform_loc, 1, False,
                                numpy.array([aspect * zoom, 0, pos_x, 0, 1 * zoom, pos_y, 0, 0, 1 * zoom], dtype='float64'))
        gl.glUniform1i(max_iters_loc, int(state['max_iters']))
            
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, int(len(vert_values) / 3))
            
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        gl.glReadBuffer(gl.GL_FRONT)
        data = gl.glReadPixels(0,0,width,height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, outputType=None)
        file = open("image_" + str(x) + ".txt", "w")
        for a in data:
            file.write(str(a))
        file.close()
        image = Image.frombytes("RGB", (width, height), data)
        image.save("image_" + str(x) + ".png", "PNG")
            
        gl.glFlush()

        
    time_t = glfw.get_time()
    print("frame render time", time_t - time_before)
    
    glfw.terminate()

if __name__ == '__main__':
    main()
    