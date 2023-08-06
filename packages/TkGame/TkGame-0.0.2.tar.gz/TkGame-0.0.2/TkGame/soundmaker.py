from playsound import playsound

class MakeSound:
    def __init__(self, sound):
        self.sound = sound
    
    def play(self):
        playsound(self.sound)
        
    
    def playLoop(self):
        playsound(self.sound, True)
    
    def stop(self):
        playsound.stop_all()
    
    def pause(self):
        playsound.pause_all()
    
    def resume(self):
        playsound.resume_all()
    

    