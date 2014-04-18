import pyglet
from pyglet.window import key
from pyglet.gl import *
import numpy as np
import serial
from thread import start_new_thread
import math
import time

    
def opengl_init():
    """ Initial OpenGL configuration.
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthFunc(GL_LEQUAL)
    
class camera(object):
    """ A camera.
    """
    mode = 1
    x, y, z = 0, 0, 512
    rx, ry, rz = 30, -45, 0
    w, h = 640, 480
    far = 8192
    fov = 60

    def view(self, width, height):
        """ Adjust window size.
        """
        self.w, self.h = width, height
        glViewport(0, 0, width, height)
        self.mode = 3
        self.perspective()

    def default(self):
        """ Default pyglet projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.w, 0, self.h, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def isometric(self):
        """ Isometric projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.w/2., self.w/2., -self.h/2., self.h/2., 0, self.far)
        glMatrixMode(GL_MODELVIEW)

    def perspective(self):
        """ Perspective projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        glMatrixMode(GL_MODELVIEW)

    def key(self, symbol, modifiers):
        """ Key pressed event handler.
        """
        if symbol == key.F1:
            self.mode = 1
            self.default()
            print "Projection: Pyglet default"
        if symbol == key.NUM_0:
            global correction_rmatrix1, zero_rmatrix, rmatrix1
            correction_rmatrix1 = np.dot(zero_rmatrix, np.linalg.inv(rmatrix1))
        elif symbol == key.F2:
            print "Projection: 3D Isometric"
            self.mode = 2
            self.isometric()
        elif symbol == key.F3:
            print "Projection: 3D Perspective"
            self.mode = 3
            self.perspective()
        elif self.mode == 3 and symbol == key.NUM_SUBTRACT:
            self.fov -= 1
            self.perspective()
        elif self.mode == 3 and symbol == key.NUM_ADD:
            self.fov += 1
            self.perspective()
        else: print "KEY " + key.symbol_string(symbol)

    def drag(self, x, y, dx, dy, button, modifiers):
        """ Mouse drag event handler.
        """
        if button == 1:
            self.x -= dx*2
            self.y -= dy*2
        elif button == 2:
            self.x -= dx*2
            self.z -= dy*2
        elif button == 4:
            self.ry += dx/4.
            self.rx -= dy/4.
         
        #print self.x, self.y, self.z, self.rx, self.ry, self.rz

    def apply(self):
        """ Apply camera transformation.
        """
        glLoadIdentity()
        if self.mode == 1: return
        glTranslatef(-self.x, -self.y, -self.z)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)


def x_array(list):
    """ Converts a list to GLFloat list.
    """
    return (GLfloat * len(list))(*list)

def axis(d=200):
    """ Define vertices and colors for 3 planes
    """
    transp = 0.2
    vertices , colors = [], []   
    #XZ RED 
    vertices.extend([-d, 0, -d, d, 0, -d, d, 0, d, -d, 0, d])
    for i in range (0, 4):
        colors.extend([1, 0, 0, transp])
    #YZ GREEN 
    vertices.extend([0, -d, -d, 0, -d, d, 0, d, d, 0, d, -d])
    for i in range (0, 4):
        colors.extend([0, 1, 0, transp])
    #XY BLUE 
    vertices.extend([-d, -d, 0, d, -d, 0, d, d, 0, -d, d, 0])
    for i in range (0, 4):
        colors.extend([0, 0, 1, transp])
    return x_array(vertices), x_array(colors)

AXIS_VERTICES, AXIS_COLORS = axis()

def draw_vertex_array(vertices, colors, mode=GL_LINES):
    """ Draw a vertex array.
    """
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(4, GL_FLOAT, 0, colors)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glDrawArrays(GL_QUADS, 0, len(vertices)/3)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

def draw_axis():
    """ Draw the 3 planes
    """
    glEnable(GL_DEPTH_TEST)
    draw_vertex_array(AXIS_VERTICES, AXIS_COLORS, GL_QUADS)
    glDisable(GL_DEPTH_TEST)

class SimulationWindow(pyglet.window.Window):
   def __init__(self):
      super(SimulationWindow, self).__init__(resizable=True)
      opengl_init()
      self.cam = camera()
      self.on_resize = self.cam.view
      self.on_key_press = self.cam.key
      self.on_mouse_drag = self.cam.drag
        
      print "Camera -> Drag LMB, CMB, RMB"
      print ""
      print "XZ: RED, YZ: GREEN, XY: BLUE"
      
      pyglet.clock.schedule_interval(self.dummy, 1.0/120.0)
      

   def on_draw(self):
      self.clear()
      self.cam.apply()
      draw_axis()
      self.playground()
   
   p1 = np.array([0,0,0], dtype = 'float')
   p2 = np.array([0,0,0], dtype = 'float')
   p3 = np.array([0,0,0], dtype = 'float')
   p4 = np.array([0,0,0], dtype = 'float')
   drift_over = False
   
   def update_points(self, p1, p2, p3, p4, drift_over):
      self.p1 = p1
      self.p2 = p2
      self.p3 = p3
      self.p4 = p4
      
      self.drift_over = drift_over
   
   def playground(self):
      """ Draw something here, like a white X.
      """

      glLineWidth(2)                    
      glBegin(GL_LINES)
      if self.drift_over: glColor3f (1, 1, 1)
      else: glColor3f (1, 0, 0)
    
    
      glVertex3f(0,0,0);
      glVertex3f(self.p1[1],self.p1[2],-self.p1[0]);
    
      glVertex3f(0,0,0);
      glVertex3f(self.p2[1],self.p2[2],-self.p2[0]);
      
      glVertex3f(0,0,0);
      glVertex3f(self.p3[1],self.p3[2],-self.p3[0]);
    
      glEnd()
      glFlush();
      
   def dummy(self, dt):
      pass

