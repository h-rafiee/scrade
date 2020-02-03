import scrapy
from scrapy.crawler import CrawlerProcess
import sys, getopt, shlex, datetime
import glob, os
import wget

pdfaddress = ''

class DiplobotSpider(scrapy.Spider):
    name = 'diplobot'
    start_urls = ['https://teheran.diplo.de/ir-fa/service/visa-einreise/-/2074660']

    def parse(self, response):
        pdf = response.css('a.rte__anchor.i-pdf::attr(href)').extract_first()
        global pdfaddress
        pdfaddress = pdf


def main(argv):
    path = '/var/tmp/scrapy-de'
    try:
        opts, args = getopt.getopt(argv,"h",['help', 'path='])
    except getopt.GetoptError :
        print('run.py --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print("Backup version 0.1b by Hossein Rafiee <h.rafiee91@gmail.com> - [help]\n")
            print('run.py --path=<optional: path>')
            print("-------------------------------------")
            print("• default path: /var/tmp/scrapy-de\n")
            sys.exit(2)
        elif opt == '-p' or opt == '--path':
            path = arg
    doScrapy(path)

def doScrapy(path):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    if os.path.isdir(path) is not True :
         os.makedirs(path)
    process = CrawlerProcess({
        'LOG_LEVEL':'ERROR'
    })
    process.crawl(DiplobotSpider)
    process.start()
    filepath = path + '/' + now + '.pdf'
    wget.download(pdfaddress, filepath)

    
    
    

if __name__ == "__main__":
    main(sys.argv[1:])