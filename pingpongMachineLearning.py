import sys
import time
import math
from numpy import zeros

try:
    import numpy as np
except:
    print("ERROR: Numpy not installed properly.")
    sys.exit()
try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("ERROR: PyOpenGL not installed properly.")
    sys.exit()

class GameGL(object):
    config = None
    def __init__(self, config = None):
        self.config = config
    '''
    Is needed for the OpenGL-Library because standard strings are not allowed.
    '''
    def toCString(self, string):
        return bytes(string, "ascii")

class BasicGame(GameGL):

    windowName = "PingPong"
    # 30px
    pixelSize = 30

    # this initializes s , the first Zustand
    xBall      = 5
    yBall      = 6
    xSchlaeger = 5
    xV         = 1.5
    yV         = 1
    xMax       = 10
    yMax       = 10
    xVMax      = 10
    yVMax      = 10
    schlaegerMax = 10
    score      = 0
    reward = 0
    Q_array = zeros([3, 4000])  # zeros([n, size])
    teta = 0.9  # the discount factor
    alpha = np.random.random()  # ist die Learn rate


    def __init__(self, name, width = 360, height = 360):
        super
        self.windowName = name
        self.width      = width
        self.height     = height


        # schläger positions
        self.schlaegerAction = [-1, 0, 1]

        # initialize the Q_array with random numbers
        # TODO how to initialize the Q_array? with the fixed size or dynamic
        #for s in range( 4000 ):
        for a in range( 3 ):
            # random array of ones or nulls
            self.Q_array[a] = np.random.random( size=4000 )
            #self.initial_population[x] = np.random.random( size=10 )

    def Q_learning(state, value):
        return

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            sys.exit(0)

    def display(self):
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # reset position
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

        #choose an action randomly
        #action = 2.0 * np.random.random() - 1.0
        action = 0


        print(self.Q_array)

        # calculate current state
        s = ((((self.yBall * self.yMax + self.xBall) * self.schlaegerMax + self.xSchlaeger) * self.xVMax + self.xV) * self.yVMax + self.yV)
        i = 1
        best_action = 0

        # Q_learning Algorithm itself to choose the best action
        while i < 1000:

            best_action = self.choose_best_action(s)

            """
            for xBall in range(xMax):
                for yBall in range(yMax):
                    for xSchlaeger in range(xMax):
                        for xV in range(xVMax):
                            for yV in range(yVMax):
                                #calculate current state
                                s = (((( yBall * yMax + yBall ) * schlaegerMax + xSchlaeger ) * xVMax + xV ) * yVMax + yV)
                                self.Q_array[s][a] += self.alpha * ( self.reward + self.teta * self.Q_array[new_s][new_a] - self.Q_array[s][a] )
                                s = new_s
                                print s
            """
        i += 1

        action = best_action

        if action == 0:  # don't move the bat
            self.xSchlaeger += 0
        if action == 1:  # move the bat to the left
            self.xSchlaeger -= 1
        if action == 2:  # move the bat to the right
            self.xSchlaeger += 1

        """
        if action < -0.3:
            self.xSchlaeger -= 1
        if action >  0.3:
            self.xSchlaeger += 1
        """

        # don't allow puncher to leave the pitch
        if self.xSchlaeger < 0:
            self.xSchlaeger = 0
        if self.xSchlaeger > 9:
            self.xSchlaeger = 9

        # move the ball
        self.xBall += self.xV
        self.yBall += self.yV

        # change direction of ball if it's at wall
        if (self.xBall > 10 or self.xBall < 1):
            self.xV = -self.xV
        if (self.yBall > 10 or self.yBall < 1):
            self.yV = -self.yV

        # calculate next state
        s_next = self.calculate_next_state()

        # check whether ball on bottom line
        if self.yBall == 0:
            # check whther ball is at position of player
            if (self.xSchlaeger == self.xBall 
                or self.xSchlaeger == self.xBall -1
                or self.xSchlaeger == self.xBall -2):
                print("positive reward")
                self.reward = +1
                self.learn(s, s_next, action)
                #  update Q-value back to adapt the next action, good action
            else:
                print("negative reward")
                self.reward = -1
                # bad action, do nothing
                self.learn(s, s_next, action)

        # repaint
        self.drawBall()
        self.drawComputer()
        
        # timeout of 100 milliseconds
        time.sleep(0.1)
        
        glutSwapBuffers()
    
    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))
        #self.init()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.onResize)
        glutIdleFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutMainLoop() 

    # is useless

    def updateSize(self):
        self.width  = glutGet(GLUT_WINDOW_WIDTH)
        self.height = glutGet(GLUT_WINDOW_HEIGHT)
    
    def onResize(self, width, height):
        self.width  = width
        self.height = height
    
    def drawBall(self, width = 1, height = 1, x = 5, y = 6, color = (0.0, 1.0, 0.0)):
        x = self.xBall
        y = self.yBall
        xPos = x * self.pixelSize
        yPos = y * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height))
        glEnd()
    
    def drawComputer(self, width = 3, height = 1, x = 0, y = 0, color = (1.0, 0.0, 0.0)):
        x = self.xSchlaeger
        xPos = x * self.pixelSize
        # set a bit away from bottom
        yPos = y * self.pixelSize# + (self.pixelSize * height / 2)
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height / 4))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height / 4))
        glEnd()

    def calculate_next_state(self):
        state = ((((self.yBall * self.yMax + self.xBall) * self.schlaegerMax + self.xSchlaeger) * self.xVMax + self.xV) * self.yVMax + self.yV)
        return state

    def learn(self, s, next_state, best_action):
        if best_action == -1:
            best_action = 0
        self.Q_array[s][best_action] = self.Q_array[next_state][best_action]

    def choose_best_action(self, s):
        bewertung_funktion_value = 0
        # take the action that has the largest Q_array[s][a] value
        for x in range(len(self.schlaegerAction)):

            action_to_try = self.schlaegerAction[x]  # new action
            if action_to_try == -1:
                action_to_try = 0

            for y in range(len(self.Q_array)):

                self.Q_array[s][action_to_try] = self.alpha * (
                            self.reward + self.teta * self.Q_array[s][action_to_try] - self.Q_array[s][action_to_try])
                if self.Q_array[s][action_to_try] > bewertung_funktion_value:
                    action = action_to_try  # take that action
        return action


game = BasicGame("PingPong")
game.start()