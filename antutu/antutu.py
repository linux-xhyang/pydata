from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from distutils.log import warn as printf

from myuilib import *

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
#des['udid'] = '192.168.1.33:5555'
des['udid'] = '10.235.178.230:5555'
des['stopAppOnReset'] = False
des['dontStopAppOnReset'] = True
#des['app'] = "/home/duokan/xhyang/system/vendor/app/TvHome/TvHome.apk"
#des['app'] = "/home/duokan/xhyang/system/app/MiTVSettings2/MiTVSettings2.apk" 
driver = webdriver.Remote('http://localhost:4723/wd/hub', des)

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
    if layout_content_find_text(driver,'开始测试') != None:
        printf('Finding 开始测试...')
        els = layout_content_find_text(driver,'开始测试')
        if els:
            select_by_text(driver,'开始测试')

        return True
    elif layout_content_find_text(driver,'安装测试') != None:
        printf('安装测试...')
        select_by_text(driver,'安装测试')
        els = layout_content_find_text(driver,'下载中')
        if els:
            els.click()
            if driver.wait_activity('.ui.PackageInstallerActivity',200):
                select_by_text(driver,'安装')
                if driver.wait_activity('.ui.InstallAppProgress'):
                    select_by_text(driver,'完成')
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
        pos = find_object_by_image(driver,"image/retest.png")
        if(pos):
            tap_by_position(driver,pos)
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
        print_layout_text(driver)
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

antutu_test()
