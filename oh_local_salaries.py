import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

#--------------------define variables-------------------
OUTPUT_FILE = 'oh_local_salaries.csv'
#-------------------------------------------------------

#--------------------define global functions------------

# -----------------------------------------------------------------------------------------------------------------------
class OhlocalScraper:
    def __init__(self,
                 base_url='http://www.tos.ohio.gov/LocalSalary.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

    def GetEntityType(self):
        return [
            {'Text': 'City', 'Value': '1'},
            {'Text': 'County', 'Value': '2'},
            {'Text': 'Library', 'Value': '7'},
            {'Text': 'Special District', 'Value': '4'},
            {'Text': 'Township', 'Value': '5'},
            {'Text': 'Village', 'Value': '6'}
        ]

    def GetEntityList(self, entity_type_value):
        # set get data
        params = {}
        params['entityTypeID'] = entity_type_value

        # set url
        url = 'http://www.tos.ohio.gov/Transparency_Local.aspx/PopulateEntities'

        # get request
        ret = self.session.post(url, json=params)

        if ret.status_code == 200:
            return ret.json()['d']
        else:
            print('fail to get page data')

    def GetPageData(self, entity_type_value, entity_value, start):
        # set get data
        params = {}
        params['first_name'] = ''
        params['last_name'] = ''
        params['year'] = '0'
        params['entity_type'] = entity_type_value
        params['entity_name'] = entity_value
        params['from'] = ''
        params['to'] = ''
        params['order_by'] = 'full_name,year desc'
        params['start'] = start

        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            if len(ret.text) > 0:
                # print(ret.json())
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
        header_info.append('position')
        header_info.append('gross_wage')
        header_info.append('hourly_rate')
        header_info.append('overtime')
        header_info.append('entity_type')
        header_info.append('entity_name')

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

        # get entity type list
        print('getting entity type list')
        entity_type_list = self.GetEntityType()
        print(entity_type_list)

        for entity_type in entity_type_list:
            entity_type_value = entity_type['Value']
            entity_type_text = entity_type['Text']

            # get entity list
            print('getting entity list for %s ...' % (entity_type_text))
            entity_list = self.GetEntityList(entity_type_value)
            print(entity_list)

            for entity in entity_list:
                entity_value = entity['Value']
                entity_text = entity['Text']

                # get and save page data
                print('processing for %s:%s ...' % (entity_type_text, entity_text))
                start = 0
                while(True):
                    print('from %s' % (start))
                    employees = self.GetPageData(entity_type_value, entity_value, start)
                    # print(employees)

                    if employees == None or len(employees) == 0: break
                    for employee in employees:
                        # get data
                        data = [
                            employee['year'],
                            employee['full_name'],
                            employee['job_title'],
                            '$' + employee['total_gross_wages'],
                            employee['hourly_rate'],
                            employee['overtime'],
                            entity_type_text,
                            entity_text
                        ]

                        # write data into output csv file
                        self.WriteData(data)

                    start += 500

                    # break
            #     break
            # break



#------------------------------------------------------- main -------------------------------------------------------
def main():
    # create scraper object
    scraper = OhlocalScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()
