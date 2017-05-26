from appium import webdriver
from distutils.log import warn as printf
import time
from myuilib import *

device_id = '10.235.178.245:5555'
des = {}
des['platformName'] = 'Android'
des['platformVersion'] = '6.0'
des['deviceName'] = device_id
# des['deviceName'] = '192.168.1.33:5555'
des['newCommandTimeout'] = 0
des['appPackage'] = "com.mitv.tvhome"  # "com.xiaomi.mitv.settings"
# des['appActivity'] = "com.xiaomi.mitv.settings.entry.MainActivity"
des['appActivity'] = "com.mitv.tvhome.MainActivity"
des['noReset'] = True
# des['udid'] = '192.168.1.33:5555'
des['udid'] = device_id
des['stopAppOnReset'] = False
des['dontStopAppOnReset'] = True
des['disableAndroidWatcher'] = False
# des['app'] = "/home/duokan/xhyang/system/vendor/app/TvHome/TvHome.apk"
# des['app'] = "/home/duokan/xhyang/system/app/MiTVSettings2/MiTVSettings2.apk"
driver = webdriver.Remote('http://localhost:4723/wd/hub', des)


def on_main_activity(activity):
    els = layout_content_find_text(driver, '电影')
    if els is not None:
        els.click()
        pos = find_object_by_image(driver, "image/ambition_dianying.png")
        if pos is not None:
            els = el_find_by_image_pos(driver, pos, False)
            if els is not None:
                if not els.is_selected():
                    els.click()
                    els.click()
                    time.sleep(1)


def on_channel_activity(activity):
    driver.press_keycode(22)
    time.sleep(1)
    driver.press_keycode(66)
    time.sleep(1)


def on_milist_activity(activity):
    if layout_content_find_text(driver, '系统维护中'):
        printf('播放视频失败,退出')
        driver.press_keycode(4)
        time.sleep(1)
        return False
    pre = el_find_by_select(driver)
    if pre == None:  # 收藏
        printf("Not select found")
        driver.press_keycode(20)
        time.sleep(1)
        driver.press_keycode(66)
    else:
        driver.press_keycode(22)
        time.sleep(1)
        post = el_find_by_select(driver)
        if pre == post:  # last
            driver.press_keycode(20)
            time.sleep(1)
            pre = el_find_by_select(driver)
            if pre == post:
                driver.press_keycode(4)
        else:
            driver.press_keycode(66)
    time.sleep(1)


def on_detail_activity(activity):
    if layout_content_find_text(driver, '系统维护中'):
        printf('播放视频失败,退出')
        driver.press_keycode(4)
        time.sleep(1)
        return False
    if select_by_text(driver, '播放') or select_by_text(
            driver, '继续') or select_by_text(driver, '试看') or select_by_text(
                driver, '预告片'):
        time.sleep(1)
    else:
        pos = find_object_by_image(driver, "image/Play.png")
        if pos is not None:
            tap_by_position(driver, pos)
            time.sleep(1)

            if driver.current_activity == activity:  # 防止进入a选集界面
                driver.press_keycode(66)
                time.sleep(1)
                return False
            else:
                return True
        elif select_by_text(driver, '选集'):
            printf("选集:")
            time.sleep(3)
            if driver.current_activity == activity:
                if find_select_count(driver):
                    printf("Now Play:")
                    driver.press_keycode(66)
                    driver.press_keycode(66)
                else:
                    printf("No Select Found,return")
                    driver.press_keycode(4)
                time.sleep(1)
                return False
            else:
                return True
        else:
            driver.press_keycode(4)
            time.sleep(1)
            return False


def is_detail_activity():
    detail = ['.DetailsActivity', 'com.starcor.hunan.NewDetailedPageActivity']
    activity = driver.current_activity
    if activity in detail:
        return True
    else:
        return False


def turn_screen(driver):
    driver.press_keycode(26)
    time.sleep(2)
    driver.long_press_keycode(22)
    el = layout_content_find_text(driver, '关屏')
    if el is not None:
        el.click()
        time.sleep(10)
        driver.long_press_keycode(4)
    else:
        driver.long_press_keycode(22)


global play_count


def on_player_activity(activity):
    global play_count
    play_count += 1
    turn_screen(driver)
    playing_video_wait_quit(driver, 100)
    while is_detail_activity():
        driver.press_keycode(4)
        time.sleep(1)
    printf("%s:%d" % (time.ctime(), play_count))


method_key = {
    '.MainActivity': on_main_activity,
    '.ChannelActivity': on_channel_activity,
    '.MiListActivity': on_milist_activity,
    '.DetailsActivity': on_detail_activity,
    'com.starcor.hunan.NewDetailedPageActivity': on_detail_activity,
    'com.miui.videoplayer.VideoPlayerActivity': on_player_activity,
    '.PlayerActivity': on_player_activity,
    'com.ktcp.video.activity.TVPlayerActivity': on_player_activity,
    'com.starcor.hunan.MplayerV2': on_player_activity,
    'com.sohuott.tv.vod.activity.PlayerSohuActivity': on_player_activity
}


def run_method():
    if driver.current_activity in method_key:
        printf("Current Activity:%s" % driver.current_activity)
        method_key[driver.current_activity](driver.current_activity)
        time.sleep(1)
    else:
        if driver.current_activity == None:
            driver.press_keycode(66)
            driver.press_keycode(4)
            printf("Maybe Anr Found")
        else:
            printf("Unknown Activity:%s" % driver.current_activity)
        time.sleep(1)


def video_stress_test():
    global play_count
    play_count = 0

    # while True:
    #      if(home_select(driver) == False):
    #           printf("Home not found")
    #           time.sleep(2)
    #           continue
    #      else:
    #           break

    while True:
        run_method()


video_stress_test()
