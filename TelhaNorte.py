import scrapy
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import TextResponse
from time import sleep 




class TelhanorteSpider(scrapy.Spider):
    name = 'TelhaNorte'
    allowed_domains = ['www.telhanorte.com.br']
    start_urls = ['http://www.telhanorte.com.br/']


    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def parse(self, response):
        links_categorias = response.css('header nav.x-nav-menu ul.x-nav-menu__list li.x-nav-menu__item a ::attr(href)').getall()

        for link in links_categorias:
            yield response.follow(link,self.categoria)

    def categoria(self,response):
        current_link = response.url

        self.driver.get(current_link)

        total_links_products = []

        html_page = self.driver.page_source

        resp = TextResponse(url = current_link , encoding = 'utf-8', body = html_page) 

        limit_page = int(resp.css('p.x-category__product-qty ::text').get().split()[0]) 

        products_links = []
        while len(products_links) < limit_page:

            products_links = resp.css('div.x-shelf__img-container a.x-shelf__link ::attr(href)').getall()

            try:
                click_load_more = driver.find_element_by_class_name('cf-load-more').click() 
            except:
                print('Não encontrei o botão')
                break
        

        html_page = self.driver.page_source
        resp = TextResponse(url = current_link , encoding = 'utf-8', body = html_page) 
        products_links = resp.css('div.x-shelf__img-container a.x-shelf__link ::attr(href)').getall()

        for product_link in products_links:
            sleep(1)
            yield response.follow(product_link,self.product)
    


    def product(self,response):

        def find_json(key,replace_str = ''):

            start_json_key = key

            total_json = response.css('script ::text').getall()

            total_json = str(total_json)

            start_json = total_json[total_json.find(key):]
            end_json = start_json[:start_json.find(';')]

            
            data_json = end_json.replace(replace_str,'').replace(key,'')
            return data_json
        
        
        
        dims  = find_json('skuJson_0','skuJson_0 = ')
        dims = json.loads(dims)


        descriptions = find_json('vtex.events.addData(',')')
        descriptions = json.loads(descriptions)


        title = response.css('meta[name="Abstract"] ::attr(content)').get()

        



