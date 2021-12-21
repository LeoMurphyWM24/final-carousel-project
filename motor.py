import RPi.GPIO as gpio
from time import sleep, time

class Motor:

    # Pin order:  A1 A2 B1 B2  (each row in array gives a state)

    full_step = [[1, 0, 0, 1],
                 [1, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 1, 0, 1]]

    half_step = [[1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 1, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 1]]

    # swap pin 19 for 26
    pins = [5, 6, 13, 26]  # A1, A2, B1, B2
    steps_per_cycle = 50  # From experiment, 100 steps caused 2 full rotations

    
    def __init__(self):
        self.__clockwise = False  # cw direction
        self.__delay = 0.05      # seconds
        self.__on = False        # True/False

        self.setup()

        self.off()

    def off(self):
        for pin in self.pins:
            gpio.output(pin, False)

    def setup(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(5, gpio.OUT)
        gpio.setup(6, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(19, gpio.OUT)
        gpio.setup(26, gpio.OUT)
    
        
    def io(self, bit):
        return gpio.HIGH if bit else gpio.LOW  # V_HIGH if state = 1, V_LOW if state = 0


    def fullstep(self, loops, delay, clockwise=True):
        for _ in range(loops):
            for step in range(len(full_step)):
                state = full_step[step] if clockwise else full_step[3 - step]
                for i in range(len(pins)):
                    gpio.output(pins[i], io(state[i]))
                sleep(self.get_delay())


    def halfstep(self, loops, delay, clockwise=True):
        for _ in range(loops):
            for step in range(len(self.half_step)):
                state = self.half_step[step] if clockwise else self.half_step[7 - step] 
                for i in range(len(self.pins)):
                    gpio.output(self.pins[i], self.io(state[i]))
                sleep(self.get_delay()/2)  # Half delay to sync with fullstep bc 2x # of steps 


    def is_on(self):
        return self.__on


    def get_delay(self):
        return self.__delay


    def get_direction(self):
        return self.__clockwise  # 1 is clockwise, 0 counterclockwise
    

    def reverse(self):
        # self.on_off()
        self.__clockwise = not self.__clockwise
        # sleep(0.5)
        # self.on_off()


    def change_speed(self, up=True):
        new_delay = self.__delay + 0.01 if up else self.__delay - 0.01
        if 0.01 <= new_delay <= 0.10:
            self.__delay = new_delay
        # else:
        #     print("Cannot change speed to desired value")

    def speed_up(self):
        self.change_speed(up=False)

    def speed_down(self):
        self.change_speed(up=True)

    def on_off(self):
        self.__on = not self.__on
        if self.is_on():
            self.setup()
        
    
    def turn_halfstep(self):
        # print("Turning")
        while self.is_on():
            self.halfstep(10, self.get_delay(), self.get_direction())
            # print(self.get_delay())

        # print("Motor is off")
        gpio.cleanup()
        

    def __str__(self):
        status = "Motor " + ("on" if self.is_on() else "off")
        status += " in " + ("clockwise" if self.get_direction() else "counterclockwise")
        status += " direction with delay "+ str(self.get_delay())
        return status
    
