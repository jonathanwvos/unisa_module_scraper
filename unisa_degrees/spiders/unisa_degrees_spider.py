import json
import os
import re
import scrapy

class UnisaDegreesSpider(scrapy.Spider):
    base_uri = 'https://www.unisa.ac.za/sites/corporate/default/Register-to-study-through-Unisa/Undergraduate-&-honours-qualifications/Find-your-qualification-&-choose-your-modules/All-qualifications/{degree}'
    name = 'unisa_degrees'
    start_urls = [
        base_uri.format(degree='Bachelor-of-Science-Applied-Mathematics-and-Statistics-Stream-(98801-%E2%80%93-AMS)'),
        base_uri.format(degree='Bachelor-of-Science-Applied-Mathematics-and-Physics-Stream-(98801-%E2%80%93-AMP)'),
        base_uri.format(degree='Bachelor-of-Science-Chemistry-and-Physics-Stream-(98801-%E2%80%93-CAP)'),
        base_uri.format(degree='Bachelor-of-Science-Chemistry-and-Statistics-Stream-(98801-%E2%80%93-CAS)'),
        base_uri.format(degree='Bachelor-of-Science-General-(98801-%E2%80%93-GEN)'),
        base_uri.format(degree='Bachelor-of-Science-Statistics-and-Physics-Stream-(98801-%E2%80%93-STP)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-(Biochemistry-and-Botany-Stream)-(98053-%E2%80%93-BAB)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-(Biochemistry-and-Microbiology-Stream)-(98053-%E2%80%93-BAM)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-(Biochemistry-and-Physiology-Stream)-(98053-%E2%80%93-BAP)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-(Microbiology-and-Physiology-Stream)-(98053-%E2%80%93-MAP)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-Biomedical-Sciences-(98053-%E2%80%93-BMI)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-Biotechnology-Stream-(98053-%E2%80%93-BIT)'),
        base_uri.format(degree='Bachelor-of-Science-in-Life-Sciences-Genetics-and-Zoology-(or-Botany,-Microbiology,-Physiology-or-Biochemistry)-(98053-%E2%80%93-GZB)')
    ]

    def parse(self, response):
        with open('modules.manifest', 'a') as f:
            modules = {}

            for tr in response.css(".table-responsive table tbody tr:not([class='active'])"):
                module = []

                for td in tr.css('td'):
                    td_texts = td.css('*::text').getall()

                    for i in td_texts:
                        tmp = re.sub('[\\n|\\t]', '', i)
                        tmp = tmp.replace(' '*80, '')

                        if tmp:
                            module.append(tmp)

                if module:
                    entry = {}

                    for i, v in enumerate(module):
                        if i == 0:
                            code, desc = module[i].split(' - ', maxsplit=1)

                            entry['code'] = code
                            entry['desc'] = desc

                        if re.match('Pre-requisite:', module[i]):
                            entry['pre'] = module[i].replace('Pre-requisite:', '')

                        if re.match('Co-requisite:', module[i]):
                            co = module[i].replace('Co-requisite:', '')
                            co = co.replace('Any two of the following: ', '(2) ')
                            entry['co'] = co

                    f.write(json.dumps(entry) + '\n')
