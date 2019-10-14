import requests
import sys
from listUrl import MySpider
from lxml.html import soupparser, fromstring
import lxml.etree
import lxml.html
from scrapy.http import FormRequest, Request
from urllib.parse import urlparse
from scrapy.spiders import CrawlSpider
from scrapy.http.cookies import CookieJar
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
import shlex
import base64
import inspect, os
from scrapy.http import HtmlResponse
from selenium.webdriver.firefox.options import Options



class AntiXSS:

    def __init__(self):
        ''' uncomment the next line for run with manually entry '''
        response = input("enter a valid url").strip()
        self.start_server() # comment this line for run with standalone
        self.baseurl = response
        reqs = []
        reqs.append(self.process_request(Request(self.baseurl)))
        if requests.get(self.baseurl).status_code == 200 :
            #Disable the security Header , for avoid
            reqs[0]= self.disableantixxs(reqs[0])
            # ask to the user about add cookies
            ncookies = int(input("enter a number bigger of 0 for add  cookies"))
            if ncookies > 0:
                reqs[0]=self.add_cookies(reqs[0],ncookies)
            self.parse_resp (reqs[0])
        else:
            print("url not valid")
            sys.exit()


    def add_robot(self, response):
        #add the robot link to the request and the error page
        reqs = []
        robots_url = response.url + '/robots.txt'
        robot_req = Request(robots_url, callback=self.robot_parser)
        fourohfour_url = response.url + '/requestXaX404'
        fourohfour_req = Request(fourohfour_url, callback=self.parse_resp)
        #orden no logico reqs = self.parse_resp(response)
        reqs.append(robot_req)
        reqs.append(fourohfour_req)
        return reqs

    def disableantixxs(self,response):
        #looking the security header and Disable these
        if  'X-XSS-Protection' in  response.headers :
            response.headers['X-XSS-Protection'] = "0"
        if 'Content-Security-Policy' in response.headers :
            response.headers = {'Content-Security-Policy': 'reflected-xss:allow'}
        if 'Referer' in  response.headers:
            response.headers['Referer']= "*"
        print('header disables:')
        reqs= Request(response.url, headers=response.headers, dont_filter=True)
        if reqs.headers != response.headers:
            return reqs
        else:
            return response


    def add_cookies(self,response,ncookies):
        #add cookies to the request , but without take the other cookies
        cookiedictionary = {}
        for i in range(0, ncookies):
            key =  input("key of the cookie:").lower()
            value = input("value of the cookie:").lower()
            if key and value != "" :
                cookiedictionary[key] = value
        if len(cookiedictionary)> 0:
            reqsCookies= Request(response.url, cookies=cookiedictionary, meta={'dont_merge_cookies': True,  'cookiejar':CookieJar(), 'dont_redirect': True,}, dont_filter=True)
            print('Number of cookies added: '+ str(ncookies))
            return reqsCookies
        else:
            print('no cookies added, error input the key or value of the cookie ')
            return response


    def robot_parser(self, response):
        ''' Parse the robots.txt file and create Requests for the disallowed domains '''
        disallowed_urls = set([])
        for line in response.body.splitlines():
            if 'disallow: ' in line.lower():
                try:
                    address = line.split()[1]
                except IndexError:
                    # In case Disallow: has no value after it
                    continue
                disallowed = self.base_url+address
                disallowed_urls.add(disallowed)
        reqs = [Request(u, callback=self.parse_resp) for u in disallowed_urls if u != self.base_url]
        for r in reqs:
            self.log('Added robots.txt disallowed URL to our queue: '+r.url)
        return reqs



    def detec_xss(self, response):
        #looking in a file all the posible xss have in a file , if a found one write in the payload
        url = urlparse(response.url,keep_blank_values=True)
        querys = urlparse.query.split("&")
        if querys!="":
            #open the file with the string with xss , be saved before
            f = open('invalid', 'r')
            list_of_lines = f.readlines()
            for line in list_of_lines:
                if line != "":
                    for query in querys:
                        for x in range(0, len(self.decode(query))):
                            if line == self.decode(query)[x]:
                                if(int(print("parameter danger validate please check "+query +"press 1 and enter for save, and 2 for continue")))==1:
                                    f.write(self.encode(query)[x])
            f.close()



    def url_xss(self,url):
        for link in url :
            link.split("&")
            if link!="":
                new_query = "&".join([ "{}{}".format(query, self.payload()) for query in link])
                parsed = link._replace(query=new_query)
                url_new= urlparse.urlunparse(parsed)
            else:
                parsed = url + '/' + self.payload()
                url_new= urlparse.urlunparse(parsed)
            #url_new.read().find('text/javascript') == 0:



    def encode(self,value):
        #encode the url parameter with to diferent format
        array = [value.encode('utf-8'),base64.b64encode(bytes(value, 'utf-8')),value.encode('unicode_escape')]
        return array

    def decode(self,value):
        #decode the url parameter to diferent parameter
        array = [value.decode('utf-8'),base64.b64encode(bytes(value, 'utf-8')),value.decode('unicode_escape')]
        return array

    def payload (self):
        f = open('invalid', 'r')
        arrapayload=[]
        list_of_lines = f.readlines()
        for line in list_of_lines:
            if len(line.strip()) != 0:
                arrapayload.append(line.rstrip())
                #arrapayload.append(self.decode(line.rstrip()))
                arrapayload.append(self.encode(line.rstrip()))
        f.close()
        return arrapayload


    #para correrlo en modo instalacion standalone

    def get_user_agent(self, header, payload):
        if header == 'User-Agent':
            return payload
        else:
            return ''

    def start_server(self):
        pathproject=os.path.dirname(__file__)
        self.pathselenium= pathproject + "/selenium_standalone/"
        subprocess.Popen(["java", "-jar", self.pathselenium.strip()+ "selenium-server-standalone-3.13.0.jar"])


    def parse_resp(self, response):
        ''' The main response parsing function, called on every response from a new URL
        Checks for XSS in headers and url'''
        reqs = []
        orig_url = response.url

        doc= self.get_body(self.driver)
        form= doc.xpath('//form')

        #Grab the url of our initial robot
        robot_reqs = self.add_robot(response)
        if robot_reqs:
            reqs += robot_reqs

        #Grab the url of our form of the initial url
        url_reqs = MySpider(CrawlSpider).link_reqs(self.driver)
        if url_reqs:
            reqs=url_reqs

        # Grab iframe source urls if they are part of the start_url page
        iframe_reqs = MySpider(CrawlSpider).make_iframe_reqs(doc, response.url)
        if iframe_reqs:
            reqs=iframe_reqs

        form_reqs = MySpider(CrawlSpider).make_form_reqs(response.url, form, self.payload())
        if form_reqs:
            url_xss= form_reqs


        ###########XSS visit the url two times##################
        visit_same = input("you want visit the same url? input yes")
        if visit_same.strip().lower() == "yes":
            reqs.append(response.url)
            # for link in the_counter :
            for link in reqs:
                o=urlparse(link.url)
                self.driver.get( o.scheme + "://" + o.netloc + o.path)
                reqs+= MySpider(CrawlSpider).link_reqs(self.driver)
                form= doc.xpath('//form')
                reqs+=  MySpider(CrawlSpider).make_iframe_reqs(self.get_body(self.driver),o.scheme + "://" + o.netloc + o.path)
                MySpider(CrawlSpider).make_form_reqs(o.scheme + "://" + o.netloc + o.path,form,self.payload())
        else:
            for link in self.removeDuplicates(reqs):
                o=urlparse(link.url)
                self.driver.get( o.scheme + "://" + o.netloc + o.path)
                reqs+= MySpider(CrawlSpider).link_reqs(self.driver)
                reqs+= MySpider(CrawlSpider).make_iframe_reqs(self.get_body(self.driver), o.scheme + "://" + o.netloc + o.path)
                form= doc.xpath('//form')
                MySpider(CrawlSpider).make_form_reqs(o.scheme + "://" + o.netloc + o.path,form,self.payload())

        self.tear_down()
        # Each Request here will be given a specific callback relative to whether it was URL variables or form inputs that were XSS payloaded

    def removeDuplicates(self,listofElements):
        # Create an empty list to store unique elements
        uniqueList = []

        # Iterate over the original list and for each element
        # add it to uniqueList, if its not already there.
        for elem in listofElements:
            if elem not in uniqueList:
                uniqueList.append(elem)

        # Return the list of unique elements
        return uniqueList

    def tear_down(self):
        self.driver.stop_client()
        self.driver.close()
        print("scan complete, thanks for use this tool")
        sys.exit()

    def get_body(self,driver):
        body = driver.page_source
        try:
            doc = lxml.html.fromstring(body, driver.current_url)
            return doc
        except lxml.etree.ParserError:
            print('ParserError from lxml on %s' % driver.current_url)
            return []
        except lxml.etree.XMLSyntaxError:
            print('XMLSyntaxError from lxml on %s' % driver.current_url)
            return []

    def process_request(self, request):
        options = Options()
        driver = webdriver.Chrome(chrome_options=options, executable_path=self.pathselenium +"chromedriver.exe")
                   #     REMOTE DRIVER
                   #      driver = webdriver.Remote(
                   #      #uncomment for use with docker
                   #     #command_executor='http://hub:4444/wd/hub',
                   #      desired_capabilities=DesiredCapabilities.FIREFOX
                   #     #uncomment for use with remote driver
                   #    command_executor='http://127.0.0.1:4444/wd/hub'

        self.driver=driver
        driver.get(request.url)
        body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


if __name__ == '__main__':
    #uncomment the next line for run mannualy
    #my_car = AntiXSS()
    my_car = AntiXSS()