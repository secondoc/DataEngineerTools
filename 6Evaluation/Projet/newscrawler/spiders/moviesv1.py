import scrapy
import json
import os
import numpy as np
import pandas as pd
from scrapy import Request
from ..items import ArticleItem
import unicodedata


class MovieSpider1(scrapy.Spider):
    name = "moviesv1"
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    allowed_domains = ["www.allocine.fr", "www.boxofficemojo.com"]
    start_urls = ["https://www.allocine.fr/film/meilleurs/?page="+str(i) for i in range (1, 31)]

    def checkbudget(self, budget):
        if ("Budget" in budget):
            return (budget[budget.index('Budget')+1])
        else: 
            return (np.NaN)
        
    def researchlink(self, title, titleint, catinfo):
        titlesearch = titleint
        if (catinfo != ' Titre original '):
                titlesearch = title
        titlesearch = unicodedata.normalize('NFD', titlesearch).encode('ascii', 'ignore').decode('utf-8')
        link = "https://www.boxofficemojo.com/search/?q="+titlesearch.replace(" ", "+")
        return(link)
    
    
    def parse(self, response):
        all_titlelinks = {
            name:response.urljoin(url) for name, url in zip(
                response.css("#content-layout .meta-title").css("a::text").extract(),
                response.css("#content-layout .meta-title").css("a::attr(href)").extract()
            )
        }
        for link in all_titlelinks.values():
            yield Request(link, callback=self.parse_movieinfo)
    
    def parse_movieinfo(self, response):
        title = response.css("#content-layout .titlebar-title.titlebar-title-lg::text").extract()[0]
        titleint = response.css(".ovw-synopsis-info .that::text")[0].extract() 
        catinfo = response.css(".ovw-synopsis-info .what.light::text")[0].extract()
        synop = " ".join(response.css("#synopsis-details .content-txt::text").extract()).strip()
        date = response.css(".meta-body").css("span::text").extract_first().strip()
        duree = response.css(".meta-body-item.meta-body-info::text").extract()[3].strip()
        genre = response.css(".meta-body-item.meta-body-info").css("span::text")[3:].extract()
        cast = response.css(".section.ovw").css(".card.person-card").css("a::text").extract()
        real = response.css(".meta-body-item.meta-body-direction").css("span::text").extract()[1]
        nbrnote = response.css(".stareval").css(".stareval-review::text")[1].extract().split(" ")[1]
        nbrcrit = response.css(".stareval").css(".stareval-review::text")[1].extract().split(" ")[4]
        notepub = response.css(".stareval").css(".stareval-note::text")[1].extract()
        notepre = response.css(".stareval-note::text")[0].extract()
        linksearch = self.researchlink(title, titleint, catinfo)   
        
        yield Request(linksearch, callback=self.parse_boxsearch, meta=
            {
                "title":title,
                "titleint":titleint,
                "catinfo":catinfo,
                "synop":synop,
                "genre":genre,
                "date":date,
                "duree":duree,
                "cast":cast,
                "real":real,
                "nbrnote":nbrnote,
                "nbrcrit":nbrcrit,
                "notepub":notepub,
                "notepre":notepre
            })
        
    def parse_boxsearch(self, response):
        title = response.meta['title']
        titleint = response.meta['titleint']
        catinfo = response.meta['catinfo']
        synop = response.meta['synop']
        genre = response.meta['genre']
        date = response.meta['date']
        duree = response.meta['duree']
        cast = response.meta['cast']
        real = response.meta['real']
        nbrnote = response.meta['nbrnote']
        nbrcrit = response.meta['nbrcrit']
        notepub = response.meta['notepub']
        notepre = response.meta['notepre']
        movielinks = "https://www.boxofficemojo.com" + response.css(".a-section.mojo-gutter .a-fixed-left-grid")[0].css("a::attr(href)")[1].extract()
                      
        yield Request(movielinks, callback=self.parse_box, meta=
            {
                "title":title,
                "titleint":titleint,
                "catinfo":catinfo,
                "synop":synop,
                "genre":genre,
                "date":date,
                "duree":duree,
                "cast":cast,
                "real":real,
                "nbrnote":nbrnote,
                "nbrcrit":nbrcrit,
                "notepub":notepub,
                "notepre":notepre
        })
 
    def parse_box(self, response):
        title = response.meta['title']
        titleint = response.meta['titleint']
        catinfo = response.meta['catinfo']
        synop = response.meta['synop']
        genre = response.meta['genre']
        date = response.meta['date']
        duree = response.meta['duree']
        cast = response.meta['cast']
        real = response.meta['real']
        nbrnote = response.meta['nbrnote']
        nbrcrit = response.meta['nbrcrit']
        notepub = response.meta['notepub']
        notepre = response.meta['notepre']
        titleen = response.css(".a-fixed-left-grid-col .a-section .a-size-extra-large::text").extract()[0]
        budget = self.checkbudget((response.css(".mojo-gutter .mojo-hidden-from-mobile .a-section").css("span::text").extract()))
        boxdom = response.css(".a-section .a-size-medium").css("span::text").extract()[-8]  
        boxint = response.css(".a-section .a-size-medium").css("span::text").extract()[-5].strip()  
        boxtot = response.css(".a-section .a-size-medium").css("span::text").extract()[-2]
        
        yield {
            "title":title,
            "titleint":titleint,
            "catinfo":catinfo,
            "synop":synop,
            "genre":genre,
            "date":date,
            "duree":duree,
            "cast":cast,
            "real":real,
            "nbrnote":nbrnote,
            "nbrcrit":nbrcrit,
            "notepub":notepub,
            "notepre":notepre,
            "titleen":titleen,
            "budget":budget,
            "boxdom":boxdom,
            "boxint":boxint,
            "boxtot":boxtot
        }               
        
        
    
    
        
        
