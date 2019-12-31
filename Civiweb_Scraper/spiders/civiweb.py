# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import dateparser


class CiviwebSpider(scrapy.Spider):
    name = 'civiweb'
    allowed_domains = ['civiweb.com']
    first_job = 127293
    last_job = 133902

    def start_requests(self):
        for i in range(self.first_job, self.last_job):
            yield Request('https://www.civiweb.com/FR/offre/%d.aspx/' % i,callback=self.parse )

    def parse(self, response):
        offer_details = {}

        ## MAIN BAR
        offer_details['Reference'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oVIM"]/text()').get()
        if offer_details['Reference'] is "N/A":
            return 
        offer_details['Title'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oTitle"]/text()').get()

        ## HEADER
        offer_details['Country'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oContry"]/text()').get()
        offer_details['City'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oCity"]/text()').get()

        offer_details['StartDate'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oStartDate"]/text()').get()
        offer_details['StartDate'] = dateparser.parse(offer_details['StartDate'])
        
        offer_details['EndDate'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oEndDate"]/text()').get()
        offer_details['EndDate'] = dateparser.parse(offer_details['EndDate'])

        offer_details['NumberOfMonths'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oNumberOfMonths"]/text()').get()
        offer_details['Organization'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oOrganization"]/text()').get()

        offer_details['Salary'] = response.xpath('//*[@id="ContenuPrincipal_BlocA1_m_oIndemnite"]/text()').get()
        offer_details['Salary'] = offer_details['Salary'].split()[0].replace('€', '')

        ## APPLICANT PROFILE BOX
        offer_details['NumberOfJobs'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oNumberOfJobs"]/text()').get()

        offer_details['DesiredExperience'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oDesiredExperience"]/text()').get()
        
        offer_details['EducationLevel'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oEducation"]/text()').get()
        if 'bac ,' in offer_details['EducationLevel']:
            offer_details['EducationLevel'] = 0
        else:
            for i in range(1,6):
                if f'bac+{i}' in offer_details['EducationLevel']:
                    offer_details['EducationLevel'] = i
                    break

        offer_details['Languages'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oLanguages"]/text()').get()
        offer_details['Languages'] = offer_details['Languages'].split(' , ')
        offer_details['Languages'].sort()

        offer_details['Competence'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oCompetence"]/text()').get()
        offer_details['Competence'] = offer_details['Competence'].split(' , ')
        offer_details['Competence'].sort()
        offer_details['Diploma'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oEducationLevel"]/text()').get()

        ## PUBLISHER BOX
        offer_details['PublicationDate'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oPublicationDate"]/text()').get()
        offer_details['PublicationDate'] = dateparser.parse(offer_details['PublicationDate'])

        offer_details['PublisherCity'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oCity2"]/text()').get()
        
        offer_details['TypeOfContract'] = response.xpath('//*[@id="ContenuPrincipal_BlocB1_m_oTypeMission"]/text()').get()

        return offer_details
