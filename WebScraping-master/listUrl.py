from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse


class MySpider(CrawlSpider):

    handle_httpstatus_list = [x for x in range(0, 300)] + [x for x in range(400, 600)]
    rules = (Rule(LinkExtractor(), callback='parse_resp', follow=True), )

    def link_reqs(self, driver):
        #Retornar los link como array of this fuction
        link_reqs = []
        for url in driver.find_elements_by_xpath("//a[@href]"):
         if(url.startswith('http://') or url.startswith('https://')):
            link_reqs.append(Request(url))
        return link_reqs

    def url_valid(self, url, orig_url):
        # Make sure there's a form action url
        if url == None:
            self.log('No form action URL found')
            return


    def make_form_reqs(self, orig_url, forms, payload):
        ''' Payload each form input in each input's own request '''
        reqs = []
        #vals_urls_meths = []
        for form in forms:
            if form.inputs:
                method = form.method
                form_url = form.action or form.base_url
                for x in range(0, len(payload)):
                    for i in form.inputs:
                        if i.name:
                            if type(i).__name__ not in ['InputElement', 'TextareaElement']:
                                continue
                            if type(i).__name__ == 'InputElement':
                                # Don't change values for the below types because they
                                # won't be strings and lxml will complain
                                nonstrings = ['checkbox', 'radio', 'submit']
                                if i.type in nonstrings:
                                    continue
                            orig_val = form.fields[i.name]
                            if orig_val == None:
                                orig_val = ''
                            try:
                                form.fields[i.name] = str(payload[x])
                            except ValueError as e:
                                self.log('Error: '+str(e))
                                continue
                            xss_param = i.name
                            values = form.form_values()
                            req= FormRequest(orig_url,
                                             formdata=values,
                                             method=method,
                                             meta={'payload': str(payload[x]),
                                                   'xss_param':xss_param,
                                                   'orig_url':orig_url,
                                                   'xss_place':'form',
                                                   'POST_to':orig_url,
                                                   'dont_redirect': True,
                                                   'handle_httpstatus_list' : range(300,309)},
                                             dont_filter=True)

                            self.is_alert_visible(payload[x])

                            reqs.append(req)
                            # Reset the value
                            try:
                                form.fields[i.name] = orig_val
                            except ValueError as e:
                                self.log('Error: '+str(e))

        #if len(reqs) > 0:
            return  orig_url
        #else:
        #   return []


    def make_iframe_reqs(self, doc, orig_url):
        ''' Grab the <iframe src=...> attribute and add those URLs to the
        queue should they be within the start_url domain '''

        parsed_url = urlparse(orig_url)
        iframe_reqs = []
        iframes = doc.xpath('//iframe/@src')
        frames = doc.xpath('//frame/@src')

        all_frames = iframes + frames

        url = None
        for i in all_frames:
            if type(i) == 'unicode':
                i = str(i).strip()
            # Nonrelative path
            if '://' in i:
                # Skip iframes to outside sources
                try:
                    if orig_url in i[:len(orig_url)+1]:
                        url = i
                except IndexError:
                    continue
            # Relative path
            else:
                url = urljoin(orig_url, i)

            if url:
                iframe_reqs.append(Request(url))

        if len(iframe_reqs) > 0:
            return iframe_reqs
        else:
            return []



    def is_alert_visible(self,payload):
        # catch if a popup display for a call to the web server usin xss o other string
         try:
          alert = self.driver.switch_to_alert()
          self.write_file(payload)
         except:
           pass



    def write_file(self, value):
        # write the value to trigger the xss in the payload file
     file = open("invalid.txt",'a')
     file.write(value)
     file.close()

