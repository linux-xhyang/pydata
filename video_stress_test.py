import unittest
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import os,sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
# Python 2.x & 3.x compatible
from distutils.log import warn as printf

backlight = 2
des = {}
des['platformName'] = 'Android'
des['platformVersion'] = '6.0'
des['deviceName'] = '10.235.178.230:5555'
#des['deviceName'] = '192.168.1.33:5555'
des['newCommandTimeout'] = 0
des['appPackage'] = "com.mitv.tvhome" #"com.xiaomi.mitv.settings"
#des['appActivity'] = "com.xiaomi.mitv.settings.entry.MainActivity"
des['appActivity'] = "com.mitv.tvhome.MainActivity"
des['noReset'] = True
des['udid'] = '10.235.178.230:5555'
#des['udid'] = '192.168.1.33:5555'
des['stopAppOnReset'] = False
des['dontStopAppOnReset'] = True
#des['app'] = "/home/duokan/xhyang/system/vendor/app/TvHome/TvHome.apk"
#des['app'] = "/home/duokan/xhyang/system/app/MiTVSettings2/MiTVSettings2.apk" 
driver = webdriver.Remote('http://localhost:4723/wd/hub', des)
#el = driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')

def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

def home_select():
    driver.press_keycode(3)
    return driver.wait_activity(".MainActivity",10,1)

def backlight_view():
    command = 'adb -s 10.235.178.230:5555 shell am broadcast -a com.xiaomi.mitv.settings.BACKLIGHT_MODE_POPUP'
    os.system(command)


def backlight_set(brightness):
    try:
        if brightness == 0:
            printf("节能模式")
            driver.find_element_by_android_uiautomator('new UiSelector().text("节能模式")').click()
            driver.find_element_by_android_uiautomator('new UiSelector().text("节能模式")').click()
        elif brightness == 1:
            printf("标准模式")
            driver.find_element_by_android_uiautomator('new UiSelector().text("标准模式")').click()
            driver.find_element_by_android_uiautomator('new UiSelector().text("标准模式")').click()
        else :
            printf("高亮模式")
            driver.find_element_by_android_uiautomator('new UiSelector().text("高亮模式")').click()
            driver.find_element_by_android_uiautomator('new UiSelector().text("高亮模式")').click()
        time.sleep(1);
        driver.press_keycode(4)
    except NoSuchElementException:
        return

def backlight_test():
    els = None
    while True:
        backlight_view()
        try:
            els = driver.find_element_by_android_uiautomator('new UiSelector().text("节能模式")')
            backlight =  random.randint(0, 2)
            backlight_set(backlight)
            time.sleep(5)
        except NoSuchElementException:
            time.sleep(1)

def find_object_by_image(image):
    directory = '%s/' % os.getcwd()
    file_name = 'tmp.png'
    driver.save_screenshot(directory + file_name)

    img_rgb = cv2.imread('tmp.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    printf(w)
    printf(h)
    found = None

    printf(template)
    for scale in np.linspace(0.8,1.6,32):
         resized = imutils.resize(template, width = int(template.shape[1] * scale))
         r = img_gray.shape[1] / float(resized.shape[1])

         res = cv2.matchTemplate(img_gray,resized,cv2.TM_CCOEFF_NORMED)
         threshold = 0.8
         loc = np.where( res >= threshold)

         if(len(loc[0]) and len(loc[1])):
              return [(int(loc[1][-1]),int(loc[0][-1]))]

def el_find_by_image_pos(pos):
     el = driver.find_elements_by_class_name('android.widget.ImageView');
     if el != None:
          for els in el:
               if
     else:

def swipe_by_direction(dir):
     width = driver.get_window_size()['width']
     height = driver.get_window_size()['height']
     if dir == 'right':
          driver.swipe(0.20, height*0.50, width*0.80, height*0.50, 1000)
     elif dir == 'left':
          driver.swipe(width*0.80, height*0.50, width*0.20, height*0.50, 1000)
     elif dir == 'up':
          driver.swipe(width*0.50, height*0.70, width*0.50, height*0.30, 1000)
     else:
          driver.swipe(width*0.50, height*0.30, width*0.50, height*0.70, 1000)


def select_by_text(text):
    try:
        cstr = 'new UiSelector().text("%s")' % text
        printf(cstr)
        els = driver.find_element_by_android_uiautomator(cstr)
        if(els):
            els.click();
            time.sleep(1)
            if(els.is_selected()):
                return True
            else:
                return False
        else:
            return False
    except NoSuchElementException:
        return False

def select_and_play_by_text(text):
    try:
        cstr = 'new UiSelector().text("%s")' % text
        printf(cstr)
        els = driver.find_element_by_android_uiautomator(cstr)
        if(els):
            els.click();
            time.sleep(1)
            if(driver.current_activity == 'com.miui.videoplayer.VideoPlayerActivity'):
                printf("found video and play")
                return True
            else:
                printf("not found video and play")
                return False
        else:
            return False
    except NoSuchElementException:
        return False

def layout_content_find_text(text):
    el = driver.find_elements_by_class_name('android.widget.TextView')
    for els in el:
        printf(els.text)
        if els.text.find(text,0,len(els.text)) >= 0:
            return els
    return None

def tap_by_position(pos):
    printf(pos)
    driver.tap(pos,10)
    time.sleep(1)

def on_detail_activity():
    if(select_by_text('播放') or select_by_text('继续')):
        return True
    pos = find_object_by_image("image/Play.png")
    if pos != None:
        tap_by_position(pos)
        return True
    else:
        return False

def on_main_activity():
    if layout_content_find_text('电影') != None:
        layout_content_find_text('电影').click()
        pos = find_object_by_image("image/ambition_dianying.png")
        if pos != None:
            tap_by_position(pos)

method_key = {'.DetailsActivity' : on_detail_activity, '.MainActivity' : on_main_activity}

global next_index
def find_next_video_to_play():
    global next_index
    i = next_index;
    while i > 0:
        driver.press_keycode(22)
        i = i - 1
    next_index = next_index + 1
    printf('next_index:')
    printf(next_index)
    time.sleep(1)

def video_stress_test():
    global next_index
    next_index = 0
    while True:
        if(home_select() == False):
            printf("Home not found")
            time.sleep(2)
            continue
        else:
            if(select_by_text("电影")):
                pos = find_object_by_image("image/ambition_dianying.png")
                if(pos):
                    tap_by_position(pos)
                    time.sleep(1)
                    find_next_video_to_play()
                    if(find_and_play_video()):
                        printf("play video 100s")
                        time.sleep(100)
                    else:
                        driver.press_keycode(66)
                        time.sleep(1)
                        if(find_and_play_video()):
                            printf("play video 200s")
                            time.sleep(200)
        

