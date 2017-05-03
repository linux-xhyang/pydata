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

