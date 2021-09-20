#source activate golfenv for this project
# cd Kaggle Notebooks cd Golf Projects cd golfscraper 
#scrapy crawl golf_final -O golf_final.csv

import scrapy

class GolfScraper(scrapy.Spider):
    name = 'golf_final'
    allowed_domains = ['pgatour.com']
    start_urls = ['https://www.pgatour.com/stats.html']


    def parse(self,response):
        
        for link in response.xpath("*//ul[contains(@class, 'nav-tabs-drop')]/li/a[not(@data-toggle)]/@href")[1:6]:
            stats_page = link.get()
            
            yield response.follow(stats_page, callback=self.pull_stats)
            
            
                
        
        # stats_link = response.xpath("*//ul[contains(@class, 'nav-tabs-drop')]/li/a[not(@data-toggle)]/@href")
        
        # for link in stats_link:
        #    stats_page = link.get()
        #    yield response.follow(stats_page, callback=self.pull_stats)
        # #yield response.follow(stats_link, callback=self.pull_stats)
           

    def pull_stats(self,response):
        for link in response.xpath("*//div[contains(@class, 'table-content')]//a/@href"):
            stats_table = link.get()
            yield response.follow(stats_table, callback=self.parse_table)

        # stats_link = response.xpath("*//div[contains(@class, 'table-content')]//a/@href")[0:1]
    
        # for link in stats_link:
        #     stats_table = link.get()
        #     yield response.follow(stats_table, callback=self.parse_table)
        #yield response.follow(stats_link2, callback=self.parse_table)
    def parse_table(self,response):
         pga = {}

         pga['group'] = response.xpath( "*//ul[contains(@class, 'nav-tabs-drop')]//li[@class='active']/a/text()").get()

         pga['stat_cat'] = response.xpath("*//div[@class='header']/h1/text()").get()
        
         pga['stat_table'] = response.xpath("*//table[@id='statsTable']").get()
         yield pga

