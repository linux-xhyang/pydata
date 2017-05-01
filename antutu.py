import unittest
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import os,sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
# Python 2.x & 3.x compatible
from distutils.log import warn as printf


des = {}
des['platformName'] = 'Android'
des['platformVersion'] = '6.0'
#des['deviceName'] = '10.235.178.230:5555'
des['deviceName'] = '192.168.1.33:5555'
des['newCommandTimeout'] = 0
des['appPackage'] = "com.mitv.tvhome" #"com.xiaomi.mitv.settings"
#des['appActivity'] = "com.xiaomi.mitv.settings.entry.MainActivity"
des['appActivity'] = "com.mitv.tvhome.MainActivity"
des['noReset'] = True
des['udid'] = '192.168.1.33:5555'
des['stopAppOnReset'] = False
des['dontStopAppOnReset'] = True
#des['app'] = "/home/duokan/xhyang/system/vendor/app/TvHome/TvHome.apk"
#des['app'] = "/home/duokan/xhyang/system/app/MiTVSettings2/MiTVSettings2.apk" 
driver = webdriver.Remote('http://localhost:4723/wd/hub', des)


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
        return [(int(loc[1][-1]),int(loc[0][-1]))]
    else:
        return None

def tap_by_position(pos):
    printf(pos)
    driver.tap(pos,10)
    time.sleep(1)

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

def layout_content_find_text(text):
    el = driver.find_elements_by_class_name('android.widget.TextView')
    for els in el:
        if els.text.find(text,0,-1) >= 0:
            return els
    return None

def print_layout_text():
    el = driver.find_elements_by_class_name('android.widget.TextView')
    for els in el:
        printf(els.text)

def antutu_start():
    printf('antutu_start')
    if driver.is_app_installed('com.antutu.ABenchMark'):
        driver.start_activity('com.antutu.ABenchMark','.ABenchMarkStart')
        if driver.wait_activity('com.antutu.benchmark.activity.MainActivity',10):
            return True
        else:
            return False
    else:
        #TODO:install aututu app
        printf('Not install aututu App')

def antutu_setup():
    printf("antutu_setup")
    if layout_content_find_text('开始测试') != None:
        printf('Finding 开始测试...')
        els = layout_content_find_text('开始测试')
        if els:
            select_by_text('开始测试')

        return True
    elif layout_content_find_text('安装测试') != None:
        printf('安装测试...')
        select_by_text('安装测试')
        els = layout_content_find_text('下载中')
        if els:
            els.click()
            if driver.wait_activity('.ui.PackageInstallerActivity',200):
                select_by_text('安装')
                if driver.wait_activity('.ui.InstallAppProgress'):
                    select_by_text('完成')
                    if driver.wait_activity('com.antutu.benchmark.activity.MainActivity',100) == False:
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        printf('Finding 重新测试...')
        pos = find_object_by_image("image/retest.png")
        if(pos):
            tap_by_position(pos)
            return True
        else:
            printf('Not found 开始测试')
            return False

def antutu_3dtest():
    printf('antutu_3dtest')
    while True:
        if driver.wait_activity('.UnityPlayerActivity',3) == False:
            return True

def antutu_scoretest():
    printf('antutu_scoretest')
    while True:
        if driver.wait_activity('com.antutu.benchmark.activity.ScoreBenchActivity',3) == False:
            return True

def antutu_resulttest():
    printf('antutu_resulttest')
    if driver.wait_activity('com.antutu.benchmark.activity.TestResultActivity',300):
        print_layout_text()
        driver.press_keycode(4)
        return True
    else:
        return False

method_key = {'com.antutu.benchmark.activity.MainActivity' : antutu_setup, '.UnityPlayerActivity' : antutu_3dtest,
              'com.antutu.benchmark.activity.ScoreBenchActivity' : antutu_scoretest,
              'com.antutu.benchmark.activity.TestResultActivity' : antutu_resulttest}

def run_antutu_method():
    method_key[driver.current_activity]()

def antutu_test():
    if antutu_start():
        while True:
            run_antutu_method()


