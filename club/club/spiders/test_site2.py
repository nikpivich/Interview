import json, requests
from bs4 import BeautifulSoup
import scrapy
import re
# import start_site

start_site = 'https://omsk.yapdomik.ru/'

class TestSite1Spider(scrapy.Spider):
    name = "test_site2"
    allowed_domains =[f'{start_site[start_site.find("//") + 2 : start_site.rfind("/")]}']
    start_urls = [f'{start_site}']
    soup = BeautifulSoup(requests.get(f'{start_site}').text, 'lxml')
    links_site = soup.find('div',class_ = 'city-select__list').find_all('a')
    for link in links_site:
        allowed_domains.append(link.get('href')[link.get('href').find('//') + 2:])
        start_urls.append(link.get('href'))

    def parse(self, response):
        link_about = response.xpath("//div[@class='menu__pages']//a/@href")[1].get()
        yield response.follow(link_about, callback=self.parse_data)


    def parse_data(self,response):

        data = re.findall(r"window.initialState =(.+?)</script>", response.xpath("//script")[-3].get(), re.S)
        name = response.xpath("//a[@class='site-logo']//img/@alt").get()
        phone = response.xpath("//a[@class='link link--black link--underline']/text()").get()
        city = response.xpath("//a[@class='city-select__current link link--underline']/text()").get()
        data_set = json.loads(data[0].strip())
        for i in data_set.get('shops'):
            yield {
                'name': name,
                'address':f"{city},{i.get('address')}",
                'latloon':[i.get('coord').get("latitude"),i.get("coord").get("longitude")],
                'phones':[phone],
                'working_hours':[f"Пн-Вс {i.get('schedule')[0].get('openTime')}-{i.get('schedule')[0].get('closeTime')}"]
            }



