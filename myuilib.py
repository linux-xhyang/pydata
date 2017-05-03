from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import random
import os,sys
import cv2
import numpy as np
import imutils
# Python 2.x & 3.x compatible
from distutils.log import warn as printf

def find_object_by_image(driver,image):
    directory = '%s/' % os.getcwd()
    file_name = 'tmp.png'
    driver.save_screenshot(directory + file_name)

    img_rgb = cv2.imread('tmp.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    for scale in np.linspace(0.8,1.6,32):
         resized = imutils.resize(template, width = int(template.shape[1] * scale))
         r = img_gray.shape[1] / float(resized.shape[1])

         res = cv2.matchTemplate(img_gray,resized,cv2.TM_CCOEFF_NORMED)
         threshold = 0.8
         loc = np.where( res >= threshold)

         if(len(loc[0]) and len(loc[1])):
              return [(int(loc[1][-1]),int(loc[0][-1]))]

def el_find_by_image_pos(driver,pos,selected):
    el = driver.find_elements_by_class_name('android.widget.ImageView')
    if el != None:
        if(selected):
            select = [x for x in el if x.is_selected()]
        else:
            select = [x for x in el if x.size['width'] > 0 and x.size['height'] > 0]
        for els in select:
            start_x = els.location['x']
            start_y = els.location['y']
            end_x = start_x + els.size['width']
            end_y = start_y + els.size['height']
            x = pos[0][0]
            y = pos[0][1]
            if x > start_x and x < end_x and y > start_y and y < end_y:
                return els
    else:
        return None

def el_find_by_select(driver):
    el = driver.find_elements_by_class_name('android.widget.ImageView')
    if el != None:
        select = [x for x in el if x.is_selected() and x.size['width'] > 0 and x.size['height'] > 0]
        if len(select) == 1:
            return select[0]
        else:
            printf("Multi Select Found")
    else:
        return None

def swipe_by_direction(driver,dir):
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


def select_by_text(driver,text):
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

def tap_by_position(driver,pos):
    printf(pos)
    driver.tap(pos,10)
    time.sleep(1)

def select_by_text(driver,text):
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

def layout_content_find_text(driver,text):
    el = driver.find_elements_by_class_name('android.widget.TextView')
    for els in el:
        if els.text.find(text,0,len(els.text)) >= 0:
            return els
    return None

def print_layout_text(driver):
    el = driver.find_elements_by_class_name('android.widget.TextView')
    for els in el:
        printf(els.text)

def home_select(driver):
    driver.press_keycode(3)
    return driver.wait_activity(".MainActivity",10,1)

def is_player_activity():
    player_activity = ['.PlayerActivity',
                       'com.miui.videoplayer.VideoPlayerActivity',
                       'com.ktcp.video.activity.TVPlayerActivity',
                       'com.starcor.hunan.MplayerV2',
                       'com.sohuott.tv.vod.activity.PlayerSohuActivity']
    activity = driver.current_activity
    if activity in player_activity:
        return activity
    else:
        return None

def playing_video_wait_quit(driver,timeout):
    activity = is_player_activity()
    if activity != None:
        while True:
            if(timeout <= 0):
                if driver.wait_activity(activity,5,1):
                    driver.press_keycode(4)
                    driver.press_keycode(4)
                    time.sleep(1)
                    return True
                else:
                    return True
            else:
                timeout = timeout - 5
                time.sleep(5)
    else:
        return False

       
