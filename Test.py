import os
import time
import pyautogui

def checkImageExisting(state_click_image_url, timeout=2):
    found_location = None
    last = time.time()
    while found_location == None and time.time()-last < timeout:
        found_location = pyautogui.locateOnScreen(state_click_image_url, confidence= .8)
        # found_location = pyautogui.locateOnScreen(state_click_image_url)

        if found_location:
            return True
            # buttonx, buttony = pyautogui.center(found_location)
            # pyautogui.click(buttonx, buttony)

os.startfile("C:\\Program Files\\XYZprint\\XYZprint.exe")

is_found_error = checkImageExisting('ImageTest/Test.PNG', timeout=15) # เปลี่ยนรูปด้วย
if is_found_error:
    print('++++Yes++++')