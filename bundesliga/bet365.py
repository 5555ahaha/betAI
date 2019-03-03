import scrapy

class BetSpider(scrapy.Spider):
    name = 'bet365'
    start_urls = ['http://www.wincomparator.com/it-it/quote/calcio/germania/bundesliga-296/']
    def parse(self, response):
         for href in response.xpath('//div[@class="ma "][position()<=10]//a[@class="btn_list_ma cotes_3W"]/@href').extract():
             yield response.follow(href, self.parse_quote)
      
    def parse_quote(self, response):
        def case(argument):
                switcher = {
                    'Lipsia': 'RB Leipzig',
                    'Hannover': 'Hannover',
                    'Borussia Dortmund': 'Dortmund',
                    'Eintracht Francoforte': 'Ein Frankfurt',
                    'Hertha BSC': 'Hertha',
                    'Wolfsburg': 'Wolfsburg',
                    'Norimberga': 'Nurnberg',
                    'Werder Bremen': 'Werder Bremen',
                    'Bayer Leverkusen': 'Leverkusen',
                    'Bayern Monaco': 'Bayern Munich',
                    'Hoffenheim': 'Hoffenheim',
                    'Fortuna Dusseldorf': 'Fortuna Dusseldorf',
                    'Schalke 04': 'Schalke 04',
                    'Augsburg': 'Augsburg',
                    '1. Fsv Mainz 05': 'Mainz',
                    'Stocarda': 'Stuttgart',
                    'Friburgo': 'Freiburg'
           
                }
                return switcher.get(argument, "M'gladbach")
        yield {
            'home': case(response.xpath('//div[@id="headband"]//div[@id="team1"]//text()').extract_first()),
            'away': case(response.xpath('//div[@id="headband"]//div[@id="team2"]//text()').extract_first()),
            '1': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[1].re('\d+.\d+')[0],
            'X': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[3].re('\d+.\d+')[0],
            '2': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[5].re('\d+.\d+')[0]
        }
