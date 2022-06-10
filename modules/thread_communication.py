import serial
import warnings
import serial.tools.list_ports
import time
import threading

class ThreadSettings:
    def __init__(self, run = True, threshold = 500) -> None:
        self.run = run
        self.threshold = threshold
        self.left_voltage = 0
        self.right_voltage = 0

def arduino_communication(left_key, right_key, settings : ThreadSettings, pygame, publish_volt = False):
    arduino_ports = [ p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
    chosen_port = arduino_ports[0]
    
    serial_ = serial.Serial(chosen_port, baudrate=9600, timeout=1)
    print("Connected to: ", chosen_port)
    
    last_left_state, last_right_state = 0, 0
    left_voltage, right_voltage = 0, 0
    left_state, right_state = 0, 0

    time.sleep(0.1)
    while settings.run:
        # bytesToRead = serial_.inWaiting()
        raw_msg = serial_.readline()
        serial_.flush()
        msg = raw_msg[:-2].decode() if raw_msg else ''
        splitted_msg = msg.split(',')
        if len(splitted_msg) > 1:
            
            if splitted_msg[0] and splitted_msg[1]:
                try:
                    left_voltage, right_voltage = tuple([float(voltage) for voltage in splitted_msg])
                except ValueError:
                    print("ERORR. msg is:", msg)
                # print(threading.get_ident(), "GOT:",left_voltage, right_voltage)
                left_state = 1 if left_voltage > settings.threshold else 0
                right_state = 1 if right_voltage > settings.threshold else 0

                if left_state == 0 and last_left_state == 1:  # left: high -> low (unpressed)
                    low_left_event = pygame.event.Event(pygame.KEYUP, {'key': left_key})
                    pygame.event.post(low_left_event)

                elif left_state == 1 and last_left_state == 0:  # left: low -> high (pressed)
                    high_left_event = pygame.event.Event(pygame.KEYDOWN, {'key': left_key})
                    pygame.event.post(high_left_event)

                elif right_state == 0 and last_right_state == 1:  # right: high -> low (unpressed)
                    low_left_event = pygame.event.Event(pygame.KEYUP, {'key': right_key})
                    pygame.event.post(low_left_event)

                elif right_state == 1 and last_right_state == 0:  # right: low -> high (pressed)
                    high_left_event = pygame.event.Event(pygame.KEYDOWN, {'key': right_key})
                    pygame.event.post(high_left_event)

                last_left_state, last_right_state = left_state, right_state
                if publish_volt:
                    settings.left_voltage, settings.right_voltage = left_voltage, right_voltage

    # print("exitted arduino func")

