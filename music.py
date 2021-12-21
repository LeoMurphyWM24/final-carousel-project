import time
import pygame

class Music:

    def __init__(self):
        pygame.init()

        self.__on = False
        self.__play = True
        self.__tune = 0

        # Add more tunes here
        sound_path = "/media/pi/LEO MURPHY/PHYS 351/Final Project/leo_final_project/Sound/"
        self.__tune_paths = [
            sound_path + "Mario6.mp3",
            sound_path + "Mario1.mp3",
            sound_path + "MarioCM.mp3",
            sound_path + "Mario10.mp3",
            sound_path + "MarioSA.mp3"]
        self.__tune_names = ["Underground",
                             "Main theme",
                             "Coconut Mall",
                             "Jittery",
                             "Sunshine Airport"]
        
        # self.__tune_list = [pygame.mixer.music.load(path) for path in self.__tune_paths]

        # pygame.mixer.music.set_endevent(pygame.event.custom_type())
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

        self.set_volume(1.0)
        
    """
    Music will be queued to play constantly in a loop, unless stopped or skipped
    BUTTONS
    Play/Pause: pauses music if playing, plays music if paused using unpause
    Skip tune: goes to next tune in list
    Previous tune: goes to previous tune in list
    Volume up
    Volume down
    """
    def is_on(self):
        return self.__on
        
##    def on_off(self):
##        if self.__on:
##            
##        else:
##            self.__on = True
##            self.start()

    def turn_on(self):
            self.__on = True
            self.start()

    def turn_off(self):
            self.__on = False
            pygame.mixer.music.stop()

    def play_pause(self):
        if self.__play:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.__play = not self.__play

    def load_current(self):
        pygame.mixer.music.load(self.__tune_paths[self.__tune])
        return self.__tune_names[self.__tune]
    
##    def queue_next(self):
##        pygame.mixer.music.queue(self.__tune_paths[self.__tune])
##        next_name = self.__tune_names[self.__tune]
##        self.advance_tune()
##        return next_name

    def advance_tune(self):
        self.__tune = (self.__tune + 1) % len(self.__tune_paths)

    def decrement_tune(self):
        self.__tune = (self.__tune - 1) % len(self.__tune_paths)

    def get_tune(self):
        return self.__tune_names[self.__tune]
    

    def start(self):
        # print("Starting...")
        while(True):
            song_name = self.load_current()
            pygame.mixer.music.play()
            print("Playing", song_name)
            song_end_event = pygame.mixer.music.get_endevent()
            while pygame.event.wait().type != song_end_event:
                print("Another event occurred")
            # event = pygame.event.wait()
            self.advance_tune()
            # print("Song done\n")

    def set_volume(self, vol):
        pygame.mixer.music.set_volume(vol)

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def volume_up(self):
        self.set_volume(self.get_volume() + 0.1)

    def volume_down(self):
        self.set_volume(self.get_volume() - 0.1)
            
if __name__ == "__main__":

    m = Music()
    m.start()

