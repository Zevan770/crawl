import time

import pandas as pd
from DrissionPage import Chromium
from tqdm import tqdm


class GaokaoCrawler:
    def __init__(self, url, max_pages=13, pause_interval=50, pause_duration=60):
        self.url = url
        self.max_pages = max_pages
        self.pause_interval = pause_interval
        self.pause_duration = pause_duration
        self.contents = []
        self.browser = Chromium()
        self.page = self.browser.latest_tab
        self.page.get(self.url)

    def get_info(self):
        # 页面滚动到底部，方便查看爬到第几页
        time.sleep(2)
        self.page.scroll.to_bottom()
        # 定位包含学校信息的div
        divs = self.page.eles("tag:div@class=school-search_schoolItem__3q7R2")
        # 提取学校信息
        for div in divs:
            # 提取学校名称
            school = div.ele(".school-search_schoolName__1L7pc")
            school_name = school.ele("tag:em")
            # 提取学校城市
            city = div.ele(".school-search_cityName__3LsWN")
            city_level1, city_level2 = self.extract_city_info(city)
            # 提取学校标签
            spans_list = self.extract_tags(div)

            # 信息存到contents列表
            self.contents.append(
                [school_name.text, city_level1, city_level2, spans_list]
            )
        print(
            f"爬取第 {self.current_page} 页，总计获取到 {len(self.contents)} 条大学信息"
        )

        time.sleep(2)

        # 定位下一页，点击下一页
        try:
            next_page = self.page.ele(". ant-pagination-next")
            next_page.click()
        except:
            pass

    def extract_city_info(self, city):
        if len(city.texts()) == 2:
            return city.texts()[0], city.texts()[1]
        elif len(city.texts()) == 1:
            return city.texts()[0], ""
        else:
            return "", ""

    def extract_tags(self, div):
        tags = div.ele(".school-search_tags__ZPsHs")
        spans = tags.eles("tag:span")
        return [span.text for span in spans]

    def crawl(self):
        for self.current_page in tqdm(range(1, self.max_pages + 1)):
            # 每爬指定页数暂停一段时间
            if self.current_page % self.pause_interval == 0:
                self.get_info()
                print(f"暂停{self.pause_duration}秒")
                time.sleep(self.pause_duration)
            else:
                self.get_info()

    def save_to_csv(self):
        # 保存到csv文件
        name = ["school_name", "city_level1", "city_level2", "tags"]
        df = pd.DataFrame(columns=name, data=self.contents)
        df.to_csv(f"高考网大学信息{len(self.contents)}条.csv", index=False)
        print("保存完成")


if __name__ == "__main__":
    crawler = GaokaoCrawler(url="https://www.gaokao.cn/school/search")
    crawler.crawl()
    crawler.save_to_csv()
