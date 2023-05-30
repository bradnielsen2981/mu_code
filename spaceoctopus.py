from pgzhelper import *

class SpaceOctopus(Actor):


    def __init__(self, image):
        super().__init__(image)
        self.count = 0
        return
    
    def update(self, pos):
        self.move_in_direction(1)
        self.count += 1
        
        if self.count%180 == 0:
            self.direction += 90
        return