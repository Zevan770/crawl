#!/usr/bin/env python
# -*- coding:utf-8 -*-

# DrissionPage 库 文档地址 http://g1879.gitee.io/drissionpagedocs/

import csv
from typing import Any

import DrissionPage
from DrissionPage import Chromium, SessionPage
from DrissionPage._base.base import DrissionElement
from DrissionPage._elements.session_element import SessionElement
from DrissionPage._pages.mix_tab import MixTab
from DrissionPage.common import Settings
from fontTools.ttLib import ttFont
from loguru import logger

from font_utils import map_text, process_font_file, save_woff_file

font_file = "./texts/font.woff"
data_file = "./texts/interns.csv"
# Click next page and fetch information again for a specified number of rounds
rounds = 4  # Specify the number of rounds to loop


# -创建配置对象
Settings.set_raise_when_ele_not_found(False)
Settings.set_raise_when_click_failed(False)

# -创建浏览器
tab = Chromium().latest_tab
tab.set.NoneElement_value(None, True)

# 开始监听网络请求
tab.listen.start(targets="rand", method="GET", res_type="Font")

# 访问目标页面
tab.get("https://www.shixiseng.com/interns?keyword&city=%E5%85%A8%E5%9B%BD&type=intern")


res = tab.listen.wait(timeout=2)
logger.info(f"font-url:{ res.url }")

save_woff_file(res, font_file)
font_map = process_font_file(font_file)
logger.info(f"font_map:{font_map}")

# 确定
ele = tab("tag:input@@class=form--button", timeout=1)
if ele:
    ele.click()
# 下面叉号
ele = tab("tag:img@@class=footer-login__close", timeout=1)
if ele:
    try:
        ele.click()
    except Exception:
        pass

# Write CSV header
fields = [
    "title",
    "title href",
    "day",
    "city",
    "font",
    "tip 2",
    "font 2",
    "title 2",
    "ellipsis",
    "font 3",
    "company src",
    "company-label",
] + [
    f"intern-label {i}" for i in range(5)
]  # 动态添加 intern-label 字段

with open(data_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()


def fetch_internship_info(tab: MixTab | str, font_map):
    """
    Fetch internship information from the current page and write it to a CSV file.

    Args:
        tab (Chromium): The Chromium tab object.
        font_map (dict): The font map for decoding scrambled text.
    """
    # Open CSV file to append data
    with open(data_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        # Get all internship information elements
        interns = tab.eles("tag:div@@class=intern-wrap interns-point intern-item")

        intern: DrissionElement | SessionElement
        # Iterate over each internship information element
        for intern in interns:
            intern_labels = intern.eles("@@class=intern-label")
            title_ele = intern.ele("tag:a@@class=title ellipsis font")
            data = {
                "title": title_ele.text,
                "title href": title_ele.attr("href"),
                "day": intern("@@class=day font").text,
                "city": intern("@@class=city ellipsis").text,
                "font": intern("@@class=font").text,
                "tip 2": intern("@@class=tip").text,
                "font 2": intern("@@class=font").text,
                "title 2": intern("@@class=title ellipsis").text,
                "ellipsis": intern("@@class=ellipsis").text,
                "font 3": intern("@@class=font").text,
                "company src": intern("@@class=company").attr("src"),
                "company-label": intern("@@class=company-label").text,
            }
            title_ele.click.middle()

            # Apply map_text to all fields
            data = {key: map_text(value, font_map) for key, value in data.items()}

            # Dynamically add intern-label data
            for i in range(min(5, len(intern_labels))):
                data[f"intern-label {i}"] = intern_labels[i].text

            writer.writerow(data)
        logger.info(f"Fetched {len(interns)} internship information items.")


# Fetch internship information from the first page
fetch_internship_info(tab, font_map)

for _ in range(rounds):
    next_button = tab.eles(
        "tag:i@@class=el-icon el-icon-arrow-right"
    ).filter_one.clickable()
    if next_button:
        next_button.click()
        fetch_internship_info(tab, font_map)
    else:
        break  # Exit the loop if there is no next button
