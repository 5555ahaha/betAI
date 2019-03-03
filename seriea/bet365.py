import scrapy

class BetSpider(scrapy.Spider):
    name = 'bet365'
    start_urls = ['http://www.wincomparator.com/it-it/quote/calcio/italia/serie-a-100/']
    def parse(self, response):
         for href in response.xpath('//div[@class="ma "][position()<=10]//a[@class="btn_list_ma cotes_3W"]/@href').extract():
             yield response.follow(href, self.parse_quote)
      
    def parse_quote(self, response):
        
        yield {
            'home': response.xpath('//div[@id="headband"]//div[@id="team1"]//text()').extract_first(),
            'away': response.xpath('//div[@id="headband"]//div[@id="team2"]//text()').extract_first(),
            '1': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[1].re('\d+.\d+')[0],
            'X': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[3].re('\d+.\d+')[0],
            '2': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[5].re('\d+.\d+')[0]
        }
