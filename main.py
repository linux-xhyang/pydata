import unittest
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

backlight = 2
des = {}
des['platformName'] = 'Android'
des['platformVersion'] = '6.0'
des['deviceName'] = '10.235.178.230:5555'
des['newCommandTimeout'] = 0
des['appPackage'] = "com.mitv.tvhome" #"com.xiaomi.mitv.settings"
#des['appActivity'] = "com.xiaomi.mitv.settings.entry.MainActivity"
des['appActivity'] = "com.mitv.tvhome.MainActivity"
des['noReset'] = True
des['udid'] = '10.235.178.230:5555'
des['stopAppOnReset'] = False
des['dontStopAppOnReset'] = True
#des['app'] = "/home/duokan/xhyang/system/vendor/app/TvHome/TvHome.apk"
#des['app'] = "/home/duokan/xhyang/system/app/MiTVSettings2/MiTVSettings2.apk" 
driver = webdriver.Remote('http://localhost:4723/wd/hub', des)
#el = driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')

def home_select():
    driver.press_keycode(3)
    return driver.wait_activity(".MainActivity",10,1)

def backlight_view():
    command = 'adb -s 10.235.178.230:5555 shell am broadcast -a com.xiaomi.mitv.settings.BACKLIGHT_MODE_POPUP'
    os.system(command)


def backlight_set(brightness):
    try:
        if brightness == 0:
            print "节能模式"
            driver.find_element_by_android_uiautomator('new UiSelector().text("节能模式")').click()
            driver.find_element_by_android_uiautomator('new UiSelector().text("节能模式")').click()
        elif brightness == 1:
            print "标准模式"
            driver.find_element_by_android_uiautomator('new UiSelector().text("标准模式")').click()
            driver.find_element_by_android_uiautomator('new UiSelector().text("标准模式")').click()
        else :
            print "高亮模式"
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

def do_test():
    while True:
        time.sleep(1)
        home_select()
        time.sleep(5)

def find_object_by_image(image):
    directory = '%s/' % os.getcwd()
    file_name = 'tmp.png'
    driver.save_screenshot(directory + file_name)

    img_rgb = cv2.imread('tmp.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)

    # for debug
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    # cv2.imwrite('res.png',img_rgb)
    if(len(loc[0]) and len(loc[1])):
        return [(loc[1][-1],loc[0][-1])]
    else:
        return None

def select_by_text(text):
    try:
        cstr = 'new UiSelector().text("%s")' % text
        print cstr
        els = driver.find_element_by_android_uiautomator(cstr)
        if(els):
            els.click();
            if(els.is_selected()):
                return True
            else:
                return False
        else:
            return False
    except NoSuchElementException:
        return False

def tap_by_position(pos):
    pre = driver.current_activity
    driver.tap(pos,10)
    time.sleep(1)
    post = driver.current_activity
    if(pre == post):
        driver.press_keycode(66)

def find_and_play_video():
    pos = find_object_by_image("image/Play.png")
    if(pos):
        tap_by_position(pos)
        return True
    else:
        return False

global next_index
def find_next_video_to_play():
    global next_index
    i = next_index;
    while i > 0:
        driver.press_keycode(22)
        i = i -1
    next_index = next_index + 1
    time.sleep(1)

def video_stress_test():
    global next_indexdex
    next_index = 0
    while True:
        if(home_select() == False):
            print "Home not found"
            time.sleep(2)
            continue
        else:
            if(select_by_text("电影")):
                pos = find_object_by_image("image/ambition_dianying.png")
                if(pos):
                    tap_by_position(pos)
                    time.sleep(1)
                    find_and_play_video()
                    if(find_and_play_video()):
                        time.sleep(1000)
                    else:
                        driver.press_keycode(66)
                        time.sleep(1)
                        find_and_play_video()
                        if(find_and_play_video()):
                            time.sleep(20)
