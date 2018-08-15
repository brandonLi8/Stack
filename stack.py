import pygame, random, math, sys
import os.path
print(os.path.isfile('KOMIKAX_.ttf')) 
def createBlock(color1, color2, color3, coords):
  colors = [color1, color2, color3]
  w, h = 210, 172
  blockSurface = pygame.Surface((w, h), pygame.SRCALPHA) 
  blockSurface.fill((0,0,0,0))

  for i in range(len(coords)):
    pygame.draw.aalines(blockSurface, (0,0,0), True, coords[i], False)
    pygame.draw.aalines(blockSurface, colors[i], True, coords[i], False)

    pygame.draw.polygon(blockSurface, colors[i], coords[i])
    pygame.draw.lines(blockSurface, colors[i], True, coords[i])
    pygame.draw.lines(blockSurface, (0,0,0), True, coords[i])
    pygame.draw.lines(blockSurface, colors[i], True, coords[i])



    # pygame.draw.line(blockSurface, (0,0,0), (w-1, (h - 18)/2),(w-1, h/2 + 8))
  return blockSurface
def almostEqual(d1, d2): 
    epsilon = 10**-2
    return (abs(d2 - d1) < epsilon)
def almostEqualTuples(tup1, tup2):
    for i in range(len(tup1)):
        if almostEqual(tup1[i],tup2[i]):
            return True
    return False
class block(object):
  def __init__(self, coord, color1, color2, color3, x ,y):
    self.coord = coord
    self.color1, self.color2, self.color3 = color1, color2, color3
    self.block = createBlock(color1,color2,color3, self.coord)
    self.x, self.y = x, y
  def drawBlock(self):
    canvas.blit(self.block, (self.x, self.y+22))
class stack(object):

  def __init__(self):
    self.startColor = 0
    self.endColor = 0
    self.currentColor = 0
    self.listOfColors = ((41,41,41),(120,120,120),(70, 69, 122),(213, 175, 213),(201, 105, 92))

    self.gameOverText = self.createText("Game Over",(155,155,155),(20,40,200),57)
    self.restart = self.createText( "press 'r' to restart",(0,0,0),(0,0,0),24)

    pygame.mixer.init(frequency = 60000)
    self.ding = pygame.mixer.Sound('ding.wav')
    self.effect = pygame.mixer.Sound('stack.wav')
    self.effect2 = pygame.mixer.Sound('stack2.wav')
  def restartStack(self):
    self.blockWidth, self.blockHeight, self.blockDepth = 105, 75, 22
    self.fullBlockCoords =[
      [[self.blockWidth, 2*self.blockHeight], 
       [2*self.blockWidth, self.blockHeight], 
       [self.blockWidth, 0], 
       [0, self.blockHeight]
      ],        
      [[self.blockWidth, 2*self.blockHeight + self.blockDepth], 
       [self.blockWidth, 2*self.blockHeight], 
       [0, self.blockHeight] , 
       [0, self.blockHeight+self.blockDepth]
      ],
      [[self.blockWidth, 2*self.blockHeight +self.blockDepth], 
      [self.blockWidth, 2*self.blockHeight], 
      [2*self.blockWidth, self.blockHeight],
      [2*self.blockWidth, self.blockHeight+self.blockDepth]]
      ]
    self.startColor = random.choice(self.listOfColors)
    while True:
      self.endColor = random.choice(self.listOfColors)
      if self.startColor != self.endColor: break
    self.currentColor = self.startColor
    self.blocks = []
    for i in range(15):
      self.addBlock(self.fullBlockCoords, 145, 564-(i*22))
    self.blocks[len(self.blocks)-1].x = -23-3.5
    self.blocks[len(self.blocks)-1].y = 136-2.5
    self.currentBlock = self.blocks[len(self.blocks)-1]

    self.dx = 21/5
    self.dy = 3
    self.turn = True
    self.frame = 0
    self.count = 0
    self.currentCoord = self.fullBlockCoords
    self.gameOver = False
    self.drop = False
    self.dropCount = 0
    self.paused = False
    self.pausedSurface = self.createText("Paused",(0,200,255),(204, 102, 0),57)
    self.unpause = self.createText( "press 'p' to unpause",(0,200,255),(204, 102, 0),24)
    self.score = 0
    self.scoreText = self.createText(str(self.score),(0,0,0),(180,180,180), 60)
    self.perfect = False
    self.perfectCount = 0
  def addBlock(self, coord, x, y):
  
    dR = (self.endColor[0]-self.startColor[0])/6 #delta Red
    dG = (self.endColor[1]-self.startColor[1])/6
    dB = (self.endColor[2]-self.startColor[2])/6
    newColor = list(self.currentColor) #copy to a list becasue tuples are imutable
    newColor[0] += dR
    newColor[1] += dG
    newColor[2] += dB

    if not(214 >= newColor[0] >= 41) or not(214 >= newColor[1] >= 41) or not(214 >= newColor[2] >= 41):
      self.startColor = self.currentColor
      while True:
        self.endColor = random.choice(self.listOfColors)
        if not almostEqualTuples(self.startColor, self.endColor): break
      dR = (self.endColor[0]-self.startColor[0])/6
      dG = (self.endColor[1]-self.startColor[1])/6
      dB = (self.endColor[2]-self.startColor[2])/6
      newColor = list(self.currentColor)
      newColor[0] += dR
      newColor[1] += dG
      newColor[2] += dB
    self.currentColor = tuple(newColor)
    block2Color = [newColor[0] -30,newColor[1] -40,newColor[2] -20]
    block3Color = [newColor[0] +10,newColor[1] +30,newColor[2] +40]
    self.blocks.append(block(coord, self.currentColor, block2Color, block3Color, x, y))
    w, h = 210, 172
    self.perfectSurface = pygame.Surface((w, h), pygame.SRCALPHA)
  def timerFired(self):
    if self.paused or self.gameOver: return True
    self.count += 1
    if not self.gameOver:
      self.frame += 1
      self.blocks[len(self.blocks)-1].x += self.dx
      self.blocks[len(self.blocks)-1].y += self.dy
    if self.currentBlock.x > width-175 or self.currentBlock.x < -29:
      self.dx = -self.dx
      self.dy = -self.dy
    if self.drop and not self.gameOver:
       
      for i in range(0,len(self.blocks)-1):

          self.blocks[i].y += 1
      self.dropCount += 1
      if self.dropCount == 22:
        self.drop = False
        self.dropCount = 0
    if self.perfect: 
      self.perfectCount += 1
      if self.perfectCount <30:
        print("herere")

      else:
        self.perfect = False
        self.perfectCount = 0
      
  def mousePressed(self, event):pass
  def createText(self, msg, color1, color2, size):
    #this returns two surfaces for the 3-D effect
    pygame.font.init()
    myfont = pygame.font.Font('KOMIKAX_.ttf', size)
    text = myfont.render(msg, True, color1)
    text2 = myfont.render(msg, True, color2)  
    return (text, text2)
  def keyPressed(self,event):
    if event.type == pygame.KEYDOWN: 
      if event.key == pygame.K_r:
        self.restartStack()

      if event.key == pygame.K_p:
        self.paused = not self.paused
      if self.paused or self.gameOver: return True

      if event.key == pygame.K_SPACE:

        self.score += 1
        self.scoreText = self.createText(str(self.score),(0,0,0),(180,180,180), 60)

        block = self.blocks[len(self.blocks)-1]

        self.blocks.pop(0)
        # for block in self.blocks:
          # print(block.y)
        self.drop = True
        
        # for block in self.blocks:
          # print(block.y)
        
        # self.turn = not(self.turn)
        if self.turn:
          # print(block.x, block.y)

          x0, y0 = block.coord[1][3][0] + block.x, block.coord[1][3][1]+block.y
          x1, y1 = self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[1][3][0],self.blocks[len(self.blocks)-2].y +self.blocks[len(self.blocks)-2].coord[1][3][1]-22
      
          if (block.coord[1][0][0] + block.x) <=  (self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[1][3][0]):
            self.gameOver = True
          if (block.coord[1][3][0] + block.x) >= (self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[1][0][0]):
            self.gameOver = True
          if math.fabs(x0 - x1) <= 1: 
            self.ding.play()
            self.perfect = True

          elif x0 < x1 and not self.gameOver:
            self.effect.play()
            # one
            self.currentCoord[0][0][0] -= (x1-x0)
            self.currentCoord[0][0][1] -= (y1-y0)
            self.currentCoord[1][1] = self.currentCoord[0][0]
            self.currentCoord[2][1] = self.currentCoord[0][0]

            #two
            self.currentCoord[0][1][0] -= (x1-x0)
            self.currentCoord[0][1][1] -= (y1-y0)
            self.currentCoord[2][2] = self.currentCoord[0][1]
            # five
            self.currentCoord[1][0][0] -= (x1-x0)
            self.currentCoord[1][0][1] -= (y1-y0)
            self.currentCoord[2][0] = self.currentCoord[1][0]
            #seven
            self.currentCoord[2][3][0] -= (x1-x0)
            self.currentCoord[2][3][1] -= (y1-y0)
          elif x0 > x1 and not self.gameOver:
            self.effect.play()
            x0, y0 = block.coord[1][0][0] + block.x, block.coord[1][0][1]+block.y
            x1, y1 = self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[1][0][0],self.blocks[len(self.blocks)-2].y +self.blocks[len(self.blocks)-2].coord[1][0][1]-22
            # six
            self.currentCoord[1][3][0] += (x0-x1)
            self.currentCoord[1][3][1] += (y0-y1)

            #four
            self.currentCoord[0][3][0] += (x0-x1)
            self.currentCoord[0][3][1] += (y0-y1)
            self.currentCoord[1][2] = self.currentCoord[0][3]
            # three
            self.currentCoord[0][2][0] += (x0-x1)
            self.currentCoord[0][2][1] += (y0-y1)
           
          if not self.gameOver:

            self.blocks[len(self.blocks)-1].x = 145
            self.blocks[len(self.blocks)-1].y = 278-22
            block.coord = self.currentCoord
            self.blocks[len(self.blocks)-1] = block
            self.currentBlock.coord = self.currentCoord
            self.currentBlock.block = createBlock(self.currentBlock.color1,self.currentBlock.color2,self.currentBlock.color3, self.currentCoord)
            # self.blocks[len(self.blocks)-1].coord = self.currentCoord
            self.addBlock(self.currentCoord, 313, 136)

            self.dx = -21/5
            self.dy = 3
            self.turn = False
          else:
            for i in range(0,len(self.blocks)):

              self.blocks[i].y -= 22

        else:
          x0, y0 = block.coord[1][0][0] + block.x, block.coord[1][0][1]+block.y
          x1, y1 = self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[1][0][0],self.blocks[len(self.blocks)-2].y +self.blocks[len(self.blocks)-2].coord[1][0][1]-22
          dist = ((x0-x1)**2 + (y0-y1)**2)**0.5
          if (block.coord[1][0][0] + block.x) >=  (self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[0][1][0]):
            self.gameOver = True
          # print(block.coord[1][3][0] + block.x)
          if (block.coord[0][1][0] + block.x) <= (self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[1][0][0]):
            self.gameOver = True
          if math.fabs(x0 - x1) <= 1: 
            self.ding.play()

            self.perfect = True
      
          elif x0 < x1 and not self.gameOver:
            self.effect2.play()

            # seven
            self.currentCoord[2][3][0] -= (x1-x0)
            self.currentCoord[2][3][1] -= (y1-y0)
            #two
            self.currentCoord[0][1][0] -= (x1-x0)
            self.currentCoord[0][1][1] -= (y1-y0)
            self.currentCoord[2][2] = self.currentCoord[0][1]
            #three
            self.currentCoord[0][2][0] -= (x1-x0)
            self.currentCoord[0][2][1] -= (y1-y0)
           
          elif x0 > x1 and not self.gameOver:
            self.effect2.play()

            x0, y0 = block.coord[2][3][0] + block.x, block.coord[2][3][1]+block.y
            x1, y1 = self.blocks[len(self.blocks)-2].x + self.blocks[len(self.blocks)-2].coord[2][3][0],self.blocks[len(self.blocks)-2].y +self.blocks[len(self.blocks)-2].coord[2][3][1]-22
            # one
            self.currentCoord[0][0][0] += (x0-x1)
            self.currentCoord[0][0][1] += (y0-y1)
            self.currentCoord[1][1] = self.currentCoord[0][0]
            self.currentCoord[2][1] = self.currentCoord[0][0]

            #five
            self.currentCoord[2][0][0] += (x0-x1)
            self.currentCoord[2][0][1] += (y0-y1)
            self.currentCoord[1][0] = self.currentCoord[2][0]
            #four
            self.currentCoord[0][3][0] += (x0-x1)
            self.currentCoord[0][3][1] += (y0-y1)
            self.currentCoord[1][2] = self.currentCoord[0][3]

            # six
            self.currentCoord[1][3][0] += (x0-x1)
            self.currentCoord[1][3][1] += (y0-y1)
           
          if not self.gameOver:

            self.blocks[len(self.blocks)-1].x = 145
            self.blocks[len(self.blocks)-1].y = 278-22
            block.coord = self.currentCoord
            self.blocks[len(self.blocks)-1] = block
            self.currentBlock.coord = self.currentCoord
            self.currentBlock.block = createBlock(self.currentBlock.color1,self.currentBlock.color2,self.currentBlock.color3, self.currentCoord)
            # self.blocks[len(self.blocks)-1].coord = self.currentCoord
            self.addBlock(self.currentCoord, -23, 136)

            self.dx = 21/5
            self.dy = 3
            self.turn = True
          else:
            for i in range(0,len(self.blocks)):

              self.blocks[i].y -= 22
            self.score -= 1
            self.scoreText = self.createText(str(self.score),(0,0,0),(180,180,180), 60)

        self.currentBlock = self.blocks[len(self.blocks)-1]
  def drawPaused(self):
    (paused, paused2, unpause, unpause2) = self.pausedSurface[0], self.pausedSurface[1], self.unpause[0], self.unpause[1]
    rect = paused.get_rect()
    rect2 = paused.get_rect()
    rect.midtop = (width/2, 180)
    rect2.midtop = (width/2+1, 181)

    canvas.blit(paused, rect)
    canvas.blit(paused2, rect2)
      
    rect = unpause.get_rect()
    rect2 = unpause2.get_rect()
    rect.midtop = (width/2, 280)
    rect2.midtop = (width/2+1, 281)
    canvas.blit(unpause, rect)
    canvas.blit(unpause2, rect2)
  def drawPerfectHit(self):
    six = (self.blocks[len(self.blocks)-2].x+self.blocks[len(self.blocks)-2].coord[1][2][0]-12, self.blocks[len(self.blocks)-2].y+self.blocks[len(self.blocks)-2].coord[1][3][1]+22)
    five = (self.blocks[len(self.blocks)-2].x+self.blocks[len(self.blocks)-2].coord[1][0][0], self.blocks[len(self.blocks)-2].y+self.blocks[len(self.blocks)-2].coord[1][0][1]+10+22)
    seven = (self.blocks[len(self.blocks)-2].x+self.blocks[len(self.blocks)-2].coord[2][3][0] +12, self.blocks[len(self.blocks)-2].y+self.blocks[len(self.blocks)-2].coord[2][3][1]+22)

    eight = (self.blocks[len(self.blocks)-2].x+self.blocks[len(self.blocks)-2].coord[0][2][0]), (self.blocks[len(self.blocks)-2].y+self.blocks[len(self.blocks)-2].coord[0][2][1]+44-12)
    blockSurface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(blockSurface, (200,200,200,130), [six, five,seven,eight])
    self.perfectSurface = blockSurface
    canvas.blit(self.perfectSurface, (0,0))
    # pygame.draw.line(canvas,(0,0,0), six, five,2)

  def redrawAll(self):

    for i in range(len(self.blocks)):
      # print(i)
      block = self.blocks[i]
      if self.perfect and (i+2 == len(self.blocks)):
        self.drawPerfectHit()
      block.drawBlock()
    
    # pygame.draw.line(canvas,(0,0,0), (250, 55), (250, 100))

    # pygame.draw.line(canvas,(0,0,0), (145,450), (145,450))

    # pygame.draw.line(canvas,(0,0,0), (145,375), (355,375))

    if self.paused:
      self.drawPaused()
    if self.gameOver:
      canvas.blit(self.gameOverText[0], (width/2-180, 200))
      canvas.blit(self.gameOverText[1], (width/2+2-180, 202))
      canvas.blit(self.restart[1], (width/2+1-160, 290))
    rect1 = self.scoreText[0].get_rect()
    rect2 = rect1
    rect1.midtop = (width/2, 110)
    rect2.midtop = (width/2, 112)
    canvas.blit(self.scoreText[1], rect1)

    canvas.blit(self.scoreText[0], rect2)

class button(object):
  def __init__(self, type, y, text):
    self.type = type
    if type == "green":
      self.surface, self.surface2 = self.createGreenButton( text)
      self.rect = self.surface.get_rect()
      self.rect2 = self.surface2.get_rect()
      self.rect.midtop = (width/2,y)
      self.rect2.midtop = (width/2,y)
    if type == "home":
      self.surface, self.surface2 = self.createHomeButton()
      self.rect = self.surface.get_rect()
      self.rect2 = self.surface2.get_rect()
    if type == "quit":
      self.surface, self.surface2 = self.createQuitButton(text)
      self.rect = self.surface.get_rect()
      self.rect2 = self.surface2.get_rect()
      self.rect.midtop = (width/2,y)
      self.rect2.midtop = (width/2,y)
  def createQuitButton(self,text):
    buttonSurface = pygame.Surface((140,71),pygame.SRCALPHA) 
    hoverSurface = pygame.Surface((140,71),pygame.SRCALPHA) 
    buttonSurface.fill((2, 3, 5, 0))
    hoverSurface.fill((2, 3, 5, 0))
    buttonImage = pygame.image.load("quit.png")
    hoverImage = pygame.image.load("quit2.png")
    hoverSurface.blit(hoverImage, (0,0))  
    buttonSurface.blit(buttonImage, (0,0))
    buttonText = self.createText(str(text), (25, 25, 112), (250, 250, 255), 20)
    buttonSurface.blit(buttonText[0], (10, 8))
    buttonSurface.blit(buttonText[1], (11, 8))
    hoverSurface.blit(buttonText[0], (10, 8))
    hoverSurface.blit(buttonText[1], (11, 8))
    return (buttonSurface, hoverSurface)
  def createHomeButton(self):
    buttonSurface = pygame.Surface((49, 49),pygame.SRCALPHA) 
    hoverSurface = pygame.Surface((49, 49),pygame.SRCALPHA) 
    buttonSurface.fill((2, 3, 5, 0))
    hoverSurface.fill((2, 3, 5, 0))
    buttonImage = pygame.image.load("HomeButton.png")
    hoverImage = pygame.image.load("HomeButton2.png")
    hoverSurface.blit(hoverImage, (-1, -1))  
    buttonSurface.blit(buttonImage, (-1, -1))
    return (buttonSurface, hoverSurface)
  def createText(self, msg, color1, color2, size):
  
    #this returns two surfaces for the 3-D effect
    pygame.font.init()
    myfont = pygame.font.Font('KOMIKAX_.ttf', size)
    text = myfont.render(msg, True, color1)
    text2 = myfont.render(msg, True, color2)  
    return (text, text2)
  def createGreenButton(self, text):
 
    buttonSurface = pygame.Surface((180,82), pygame.SRCALPHA)  
    hoverSurface = pygame.Surface((180,82), pygame.SRCALPHA)
    buttonImage = pygame.image.load("darkButton.png")
    hoverImage = pygame.image.load("lightButton.png")
    buttonSurface.fill((255, 255, 255, 0))
    buttonSurface.blit(buttonImage, (0,0))
    hoverSurface.fill((255, 255, 255,0))
    hoverSurface.blit(hoverImage, (0, 0))   
    buttonText = self.createText(str(text), (25, 25, 112), (250, 250, 255), 20)
    buttonSurface.blit(buttonText[0], (10, 8))
    buttonSurface.blit(buttonText[1], (11, 8))
    hoverSurface.blit(buttonText[0], (10, 8))
    hoverSurface.blit(buttonText[1], (11, 8))
    return (buttonSurface, hoverSurface)
  def draw(self,pos):
    canvas.blit(self.surface, self.rect)
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      if self.type == "quit":
        canvas.blit(self.surface2, self.rect)
      else: canvas.blit(self.surface2, self.rect2)
      return True
    return False    
class home(object):
  def __init__(self):
    self.playButton = button("green",180,"        play!")
    self.resumeButton = button("green",280,"      resume")
    self.quitButton = button("quit",380,"     quit")

  def keyPressed(self, event): pass 
  def mousePressed(self, coord): 
    pass
    
  def redrawAll(self):
  
    self.playButton.draw(pygame.mouse.get_pos())
    self.resumeButton.draw(pygame.mouse.get_pos())
    self.quitButton.draw(pygame.mouse.get_pos())
def Quit():
  print("bye")
  pygame.display.quit()
  pygame.quit()
  sys.exit(0) 
class game(object):
  def __init__(self):
    self.homeButton  = button("home",0, None)
    self.backroundSurface = pygame.image.load("backround.png").convert()
    self.stack = stack()
    self.stack.restartStack()
    self.home = home()
    self.mode = 'home'
    self.stackGame = self.homeButton.createText("Stack", (25, 25, 112), (250, 250, 255), 40)
    self.brandon =  self.homeButton.createText("By Brandon Li", (25, 25, 112), (250, 250, 255), 20) 
    self.backroundSurface.blit(self.stackGame[0], (width/2- 55, 20))
    self.backroundSurface.blit(self.stackGame[1], (width/2- 56, 22))
    self.backroundSurface.blit(self.brandon[0], (width/2- 70, 90))
    self.backroundSurface.blit(self.brandon[1], (width/2- 71, 92))
  def mousePressed(self, coord): 
    if self.mode == "home":
      if self.home.playButton.draw(pygame.mouse.get_pos()):
        self.mode = 'stack'
        self.stack.restartStack()
      if self.home.resumeButton.draw(pygame.mouse.get_pos()):
        self.mode = 'stack'
      if self.home.quitButton.draw(pygame.mouse.get_pos()):
        Quit()
    if self.homeButton.draw(pygame.mouse.get_pos()):
      self.mode = "home"
  def keyPressed(self, event):
    if self.mode == 'stack':
      self.stack.keyPressed(event)
    elif self.mode == "home":
      self.home.keyPressed(event)
  def timerFired(self):
    if self.mode == 'stack':
      self.stack.timerFired()
  def redrawAll(self):
    canvas.blit(self.backroundSurface, (0,0))
    if self.mode == 'stack':
      self.stack.redrawAll()
    elif self.mode == "home":
      for i in range(len(self.stack.blocks)-1):
        block = self.stack.blocks[i]
        if self.stack.perfect and (i+2 == len(self.stack.blocks)):
          self.stack.drawPerfectHit()
        block.drawBlock()
      self.home.redrawAll()

    self.homeButton.draw(pygame.mouse.get_pos())
    
    pygame.display.update()

  def run(self, width=300, height=300):
    pygame.init() #initiate pygame
    self.clock = pygame.time.Clock()
    pygame.key.set_repeat()
    self.maxFPS = 64
    pygame.mixer.init()
    self.count2 = 0
    while True: #game loop
      print(self.clock.get_fps())
      self.count2 += 1
      for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          Quit()         
        if event.type == pygame.MOUSEBUTTONDOWN:    
          (x, y) = pygame.mouse.get_pos()
          self.mousePressed((x, y))      
                     
        self.keyPressed(event) #handle key down or key up in key pressed
  

      self.timerFired()

      self.redrawAll()
      self.clock.tick(self.maxFPS)




width = 500 
height = 600 
canvas = pygame.display.set_mode((width, height))
game = game()
game.run(width, height)