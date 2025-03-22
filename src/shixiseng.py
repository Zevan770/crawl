
#!/usr/bin/env python
# -*- coding:utf-8 -*-

# DrissionPage 库 文档地址 http://g1879.gitee.io/drissionpagedocs/

from DrissionPage import ChromiumPage,ChromiumOptions
import csv


#-创建配置对象
co=ChromiumOptions()

#-启动配置





#-创建浏览器
page = ChromiumPage(addr_or_opts=co)
# 初始化ChromiumPage对象

# 访问目标页面
page.get('https://www.shixiseng.com/interns?keyword&city=%E5%85%A8%E5%9B%BD&type=intern')


# 获取所有实习信息元素
interns = page.eles('tag:div@@class=interns')
print()
# 定义字段列表
fields = ["title", "title href", "day", "city", "font", "tip 2", "font 2", "title 2", "ellipsis", "font 3", "company src", "intern-label", "intern-label 2", "intern-label 3", "company-label", "intern-label 4", "intern-label 5"]

# 打开CSV文件准备写入
with open('interns.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    
    # 遍历每个实习信息元素
    for intern in interns:
        data = {
            "title": intern.ele('tag:a@@class=title ellipsis font').text,
            "title href": intern.ele('tag:a@@class=title ellipsis font').attr('href'),
            "day": intern.ele('@@class=day font').text,
            "city": intern.ele('@@class=city ellipsis').text,
            "font": intern.ele('@@class=font').text,
            "tip 2": intern.ele('@@class=tip').text,
            "font 2": intern.ele('@@class=font').text,
            "title 2": intern.ele('@@class=title ellipsis').text,
            "ellipsis": intern.ele('@@class=ellipsis').text,
            "font 3": intern.ele('@@class=font').text,
            "company src": intern.ele('@@class=company').attr('src'),
            "intern-label": intern.ele('@@class=intern-label').text,
            "company-label": intern.ele('@@class=company-label').text,
            "intern-label 4": intern.ele('@@class=intern-label').text,
            "intern-label 5": intern.ele('@@class=intern-label').text,
        }
        writer.writerow(data)

print(interns.get.texts())