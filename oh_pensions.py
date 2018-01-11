import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

#--------------------define variables-------------------
OUTPUT_FILE = 'oh_pensions.csv'
#-------------------------------------------------------

#--------------------define global functions------------

# -----------------------------------------------------------------------------------------------------------------------
class OhpensionsScraper:
    def __init__(self,
                 base_url='http://www.tos.ohio.gov/PensionSalary.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

    def GetPensionSystemList(self):
        return [
            'Ohio Public Employees Retirement System'
        ]

    def GetYearList(self):
        return [
            '2014',
            '2015',
            '2016'
        ]

    def GetPageData(self, pension_system, year):
        # set get data
        params = {}
        params['first_name'] = ''
        params['last_name'] = ''
        params['year'] = year
        params['retirement_system'] = pension_system
        params['from'] = ''
        params['to'] = ''
        # params['_'] = '1515511021792'

        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            if len(ret.text) > 0:
                return ret.json()['employees']
            else:
                return ''
        else:
            print('fail to get page data')

    def WriteHeader(self):
        # set headers
        header_info = []
        header_info.append('year')
        header_info.append('name')
        header_info.append('job_title')
        header_info.append('recruitment_system')
        header_info.append('salary')

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def Start(self):
        # write header into output csv file
        self.WriteHeader()

        # get pension system list
        print('getting pension system list')
        pension_system_list = self.GetPensionSystemList()
        print(pension_system_list)

        for pension_system in pension_system_list:
            # get year list
            print('getting year list for %s ...' % (pension_system))
            year_list = self.GetYearList()
            print(year_list)

            for year in year_list:
                # get and save page data
                print('processing for %s:%s ...' % (pension_system, year))
                employees = self.GetPageData(pension_system, year)
                print(employees)

                for employee in employees:
                    # get data
                    data = [
                        employee['year'],
                        employee['full_name'],
                        employee['title'],
                        employee['retirement_system'],
                        '$' + str(employee['salary'])
                    ]

                    # write data into output csv file
                    self.WriteData(data)

                    # break
            #     break
            # break



#------------------------------------------------------- main -------------------------------------------------------
def main():
    # create scraper object
    scraper = OhpensionsScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()
