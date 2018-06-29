#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
import matplotlib.pyplot as plt

print("Starting")
global headers
totals = []
details = []
colors = [
    "cornflowerblue", "purple", "orangered", "orange", "yellowgreen",
    "lightseagreen", "mediumpurple", "orchid", "crimson", "silver"
]


def parse_framestats(line, valid_only=False):

    # http://developer.android.com/preview/testing/performance.html#fs-data-format

    # Default values. This keeps the data aligned with gfxinfo.
    start = 0
    handle_input = 0
    animations = 0
    traversals = 0
    draw = 0
    sync = 0
    gpu = 0

    if len(line[:len(line) - 1].split(',')) == 16:
        # Strip trailing comma
        framestats = list(map(float, line[:len(line) - 1].split(',')))
        if len(framestats) > 0 and framestats[0] == 0 and len(
                framestats) == 16:
            # HANDLE_INPUT_START - INTENDED_VSYNC
            start = (framestats[headers.index('HandleInputStart')] -
                     framestats[headers.index('IntendedVsync')]) / 1000000

            # ANIMATION_START - HANDLE_INPUT_START
            handle_input = (
                framestats[headers.index('AnimationStart')] -
                framestats[headers.index('HandleInputStart')]) / 1000000

            # PERFORM_TRAVERSALS_START - ANIMATION_START
            animations = (
                framestats[headers.index('PerformTraversalsStart')] -
                framestats[headers.index('AnimationStart')]) / 1000000

            # DRAW_START - PERFORM_TRAVERSALS_START
            traversals = (
                framestats[headers.index('DrawStart')] -
                framestats[headers.index('PerformTraversalsStart')]) / 1000000

            # SYNC_START - DRAW_START
            draw = (framestats[headers.index('SyncStart')] -
                    framestats[headers.index('DrawStart')]) / 1000000

            # ISSUE_DRAW_COMMANDS_START - SYNC_START
            sync = (framestats[headers.index('IssueDrawCommandsStart')] -
                    framestats[headers.index('SyncStart')]) / 1000000

            # FRAME_COMPLETED - ISSUE_DRAW_COMMANDS_START
            gpu = (
                framestats[headers.index('FrameCompleted')] -
                framestats[headers.index('IssueDrawCommandsStart')]) / 1000000

        elif valid_only:
            raise ValueError("Invalid frame.")

    return [start, handle_input, animations, traversals, draw, sync, gpu]


for j in range(1, 2):
    global headers
    headers = []
    time.sleep(1)
    print("开始执行第" + str(j) + "遍")
    # 重置所有计数器并汇总收集的统计信息
    os.popen("adb shell dumpsys gfxinfo com.google.android.tvlauncher reset")
    print("清理帧信息回到初始状态")

    # 模拟滑动页面操作
    for i in range(1, 3):
        print("执行滑动页面操作" + str(i) + "次")
        os.system("adb shell input swipe 600 600 100 100 200")
        time.sleep(1)
        os.system("adb shell input swipe 100 100 600 600 200")

    # 过滤、筛选精确的帧时间信息
    command = "adb shell dumpsys gfxinfo com.google.android.tvlauncher framestats | grep -A 120 'Flags'"
    r = os.popen(command)
    info = r.readlines()

    # 数据处理中
    print("缓存数据中......")
    for line in info:  #按行遍历
        eachline = line.strip()

        if len(headers) == 0:
            headers = eachline.split(',')
            if headers[-1] == '':
                headers.pop()

            print(headers)
        else:
            result = parse_framestats(eachline)
            details.append(result)
            totals.append(sum(result))

# frame series
if len(totals) > 0 and len(details) > 0:
    time = range(len(totals))
    threshold = 16.67
    fig, ax = plt.subplots()
    for i, (detail, column, color) in enumerate(
            zip(details, [
                "start", "input", "animations", "traversals", "draw", "sync",
                "gpu"
            ], colors)):
        ax.bar(
            time,
            detail,
            label=column,
            color=color,
            linewidth=0,
            bottom=[0] * len(detail)
            if i == 0 else list(map(sum, zip(*details[:i]))))
    ax.plot([0, len(totals)], [threshold, threshold], color="limegreen")
    plt.title(title + " Frame Series")
    plt.xlabel("Frame Number")
    plt.xlim([0, len(totals)])
    plt.ylabel("Time (ms)")
    ax.legend()

    plt.subplots_adjust(hspace=0.35)
    plt.show()
