
import numpy as np
import time
from datetime import datetime
from pynput.keyboard import Key, Controller
import os
import sys

script_dir = os.path.dirname(__file__)  # Gets the directory of the current script
parent_dir = os.path.dirname(script_dir)  # Gets the parent directory
parent_of_parent_dir = os.path.dirname(parent_dir)  # Gets the parent directory
sys.path.append(parent_of_parent_dir)





if __name__ == "__main__":
    
    time.sleep(2)
    keyboard = Controller()
    
    
    keyboard.press('j')
    time.sleep(0.03)
    keyboard.release('j')
    time.sleep(0.8)
    keyboard.press('w')
    time.sleep(0.03)
    keyboard.release('w')
    time.sleep(0.3)
    keyboard.press('j')
    time.sleep(0.03)
    keyboard.release('j')
    time.sleep(0.7)
    keyboard.press('w')
    time.sleep(0.03)
    keyboard.release('w')
    time.sleep(0.3)
    keyboard.press('j')
    time.sleep(0.03)
    keyboard.release('j')
    time.sleep(1.2)
    
    while(True):
        keyboard.press('j')
        time.sleep(0.03)
        keyboard.release('j')
        time.sleep(0.8)        
        keyboard.press('j')
        time.sleep(0.03)
        keyboard.release('j')
        time.sleep(0.7)
        keyboard.press('w')
        time.sleep(0.03)
        keyboard.release('w')
        time.sleep(0.3)
        keyboard.press('j')
        time.sleep(0.03)
        keyboard.release('j')    
        time.sleep(1.2)