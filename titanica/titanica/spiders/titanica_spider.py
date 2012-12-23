#!/usr/bin/env python
import csv
from string import upper

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


#http://www.encyclopedia-titanica.org/titanic-survivors/
#"http://www.encyclopedia-titanica.org/titanic-victims"
class titanicaSpider(BaseSpider):

    name = "titanica"
    allowed_domains = ["encyclopedia-titanica"]
    start_urls = [
        "http://www.encyclopedia-titanica.org/titanic-survivors"
    ]

    def parse(self, response):

        x = HtmlXPathSelector(response)
        survivors = x.select("//div[@id='mainContent']/table").extract().__str__()

        name_list = self.process_test_csv('../test.csv')

        output_file = open("scrap-temp.csv", "w")

        output_file.write('survived;name\n')

        for name in name_list:
            is_survivor = '1' if name in survivors else '0'
            output_file.write(is_survivor + ';' + name + '\n')
        output_file.close()

    def process_test_csv(self, file_name):

        with open(file_name, 'rb') as csv_file:

            dataset = csv.reader(csv_file, delimiter=',')
            name_list = []

            for row in dataset:
                #excludes the first line (header)
                if row[1] != 'name':
                    full_name_split = row[1].split(',')

                    title = full_name_split[1].split(' ')[1].replace('.', '')

                    if '(' not in full_name_split[1]:
                        first_name = full_name_split[1].split(' ')[2]
                    else:
                        first_name = full_name_split[1].split('(')[1].split(' ')[0].replace(')','')

                    last_name = full_name_split[0]
                    name_list.append(upper(last_name) + ', ' + title + ' ' + first_name)

        csv_file.close()
        return name_list
