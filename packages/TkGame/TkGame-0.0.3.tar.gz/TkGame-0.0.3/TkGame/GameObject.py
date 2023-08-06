from TkGame.GameScreen import *
from tkinter import *


class GameObject:
    def __init__(self, gameScreen, x, y, width, height, color=None, outline=None, tags=None, image=None):
        self.gameScreen = gameScreen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outline = outline
        self.tags = tags
        self.id = None

    def draw(self):
        if self.id is None:
            self.id = self.gameScreen.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color, outline=self.outline, tags=self.tags)

            

    
    
    def moveTo(self, x, y):
        self.x = x
        self.y = y
        self.draw()
    
    def setColor(self, color):
        self.color = color
        self.draw()
    
    def setOutline(self, outline):
        self.outline = outline
        self.draw()
    
    def setTags(self, tags):
        self.tags = tags
        self.draw()
    
    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.draw()
    
    
    
    def setPositionTo(self, x, y):
        self.x = x
        self.y = y
        self.draw()
    
    def setPositionRelative(self, x, y):
        self.x += x
        self.y += y
        self.draw()
    
    
    def setPositionRelativeToObject(self, object, x, y):
        self.x = object.x + x
        self.y = object.y + y
        self.draw()
    
   
    def Text(self, text, font=None, color=None, x=None, y=None, anchor=None, tags=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if anchor is None:
            anchor = "nw"
        if tags is None:
            tags = self.tags
        if font is None:
            font = "Arial"
        if color is None:
            color = "black"
        self.gameScreen.canvas.create_text(x, y, text=text, font=font, fill=color, anchor=anchor, tags=tags)


    def destroy(self):
        self.gameScreen.canvas.delete(self.id)
        self.id = None
    
    def update(self):
        self.gameScreen.canvas.update()
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
    
    def getColor(self):
        return self.color
    
    def getOutline(self):
        return self.outline
    
    def getTags(self):
        return self.tags
    
    def getID(self):
        return self.id

    def getGameScreen(self):
        return self.gameScreen
    

class imageObject(GameObject):
    def __init__(self, gameScreen, x, y, width, height, image, tags=None):
        super().__init__(gameScreen, x, y, width, height, tags=tags)
        self.image = image
        self.id = None
    
    def draw(self):
        if self.id is None:
            self.id = self.gameScreen.canvas.create_image(self.x, self.y, image=self.image, tags=self.tags)
        
    
    def setImage(self, image):
        self.image = image
        self.draw()
    
    def getImage(self):
        return self.image
    
    def getImageID(self):
        return self.id
    
    

