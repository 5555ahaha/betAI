#coding=utf8
import scrapy

class BetSpider(scrapy.Spider):
    name = 'bet365'
    start_urls = ['http://www.wincomparator.com/it-it/quote/calcio/spagna/prima-divisione-93/']
    def parse(self, response):
         for href in response.xpath('//div[@class="ma "][position()<=10]//a[@class="btn_list_ma cotes_3W"]/@href').extract():
             yield response.follow(href, self.parse_quote)
      
    def parse_quote(self, response):

        def case(argument):
                        switcher = {
                            'Real Madrid': "Real Madrid",
                            'Deportivo Alaves Sad': 'Alaves',
                            'Eibar': "Eibar",
                            'Girona':'Girona',
                            'Betis': "Betis",
                            'Atletico Madrid': "Ath Madrid",
                            'Villarreal': "Villarreal",
                            'Espanyol ': "Espanol",
                            'Rayo Vallecano': 'Vallecano',
                            'Leganés': "Leganes",
                            'Barcellona': "Barcelona",
                            'Valencia': "Valencia",
                            'Celta Vigo': "Celta",
                            'Siviglia': "Sevilla",
                            'SD Huesca': "Huesca",
                            'Valladolid': "Valladolid",
                            'Levante': "Levante",
                            'Getafe': "Getafe",
                            'Real Sociedad': "Sociedad",
                            'Athletic Bilbao': "Ath Bilbao",
                        }
                        return switcher.get(argument, "Leganes")

        yield {
            'home': case(response.xpath('//div[@id="headband"]//div[@id="team1"]//text()').extract_first()),
            'away': case(response.xpath('//div[@id="headband"]//div[@id="team2"]//text()').extract_first()),
            '1': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[1].re('\d+.\d+')[0],
            'X': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[3].re('\d+.\d+')[0],
            '2': response.xpath('//table[@class="odds_table bet_type_3W "]/tr/td/div/text()')[5].re('\d+.\d+')[0]
        }
