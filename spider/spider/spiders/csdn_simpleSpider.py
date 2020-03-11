import scrapy


class CsdnSimpleSpider(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "csdnSimpleSpider"  # 定义蜘蛛名
    start_urls = [
        'https://www.csdn.net/nav/python'
    ]

    def parse(self, response):
        filename = 'python-blogs.txt'
        f = open(filename, 'wb')
        blog_items = response.css('ul li[data-type="blog"] a[data-report-query]')
        if blog_items is not None:
            self.log('保存文件: %s' % filename)  # 打个日志
            for blog_item in blog_items:
                blog_name = blog_item.css('a::text').extract_first().strip()
                f.write(bytes(blog_name, 'utf-8'))
                f.write(bytes('\n', 'utf-8'))

            # 开始获取下一页内容
            next_page = 'https://www.csdn.net/api/articles?type=more&category=python&shown_offset=0'
            yield scrapy.Request(next_page, callback=self.parse_next_page)

    def parse_next_page(self, response):
        encode = response.encoding
        filename = 'python-next-blogs.txt'
        next_articles = response.body.decode('cp1252').encode('utf-8')
        f = open(filename, 'wb')
        f.write(next_articles)
        self.log('保存文件: %s' % filename)  # 打个日志


