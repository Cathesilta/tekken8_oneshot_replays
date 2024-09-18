import pyautogui
import time

def capture_box(x, y, width, height, save_file):
    # Give time to switch to the game window
    time.sleep(3)

    # Capturing the specified screen region
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    
    # Save the screenshot (optional)
    screenshot.save('./{}'.format(save_file))

    # You can now process this screenshot to check for the box's presence
    # ...

# Replace with the actual coordinates and size of the box
x = 567  # X coordinate of the top-left corner of the box
y = 417  # Y coordinate of the top-left corner of the box
width = 786  # Width of the box
height = 247  # Height of the box

# x = 567  # X coordinate of the top-left corner of the box
# y = 390  # Y coordinate of the top-left corner of the box
# width = 787  # Width of the box
# height = 300  # Height of the box
       
x = 706   
y= 430
width = 605
height = 219           # Tekken Round 1

x = 567   
y= 417
width = 786
height = 247           # street fighter 6 ending box


x = 120   
y= 192
width = 1530
height = 106           # street fighter 6 match box


#481,346        1433,678
x = 481
y = 346
width = 952
height = 332           # connecting error

x = 229
y = 276
width = 1490
height = 701           # tab screen

# x = 83
# y = 153
# width = 1761
# height = 737

save_file = 'CFN_screen.png'

capture_box(x, y, width, height, save_file)
