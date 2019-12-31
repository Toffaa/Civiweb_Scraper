# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class CiviwebSpider(scrapy.Spider):
    name = 'civiweb'
    allowed_domains = ['civiweb.com']
    start_urls = ['https://www.civiweb.com/FR/offre/133902.aspx/', 'https://www.civiweb.com/FR/offre/137233.aspx']
    first_job = 100000
    last_job = 133902

    def start_requests(self):
        for i in range(self.first_job, self.last_job):
            yield Request('https://www.civiweb.com/FR/offre/%d.aspx/' % i,callback=self.parse )

    def parse(self, response):

        offer_details = {
            'NumberOfJobs' : response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oNumberOfJobs"]/text()').get(),
            'DesiredExperience' : response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oDesiredExperience"]/text()').get(),
            'EducationLevel' : response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oEducation"]/text()').get(),
            'Languages' : response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oLanguages"]/text()').get(),
            
        }

        return offer_details
