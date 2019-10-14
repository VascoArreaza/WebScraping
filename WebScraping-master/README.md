Test_Mercado

Fast, thorough, XSS in url, using scrapy and selenium.
Give it a URL and it'll crawler  every source-page,frames and robot.txt file for cast
every url and test these.



A) deploy using selenium standalone

1)  run in command prompt or console "java -jar selenium-server-standalone-3.13.0.jar (you can found it, in the folder selenium_standalone)"
2)  uncomment this lines
    '''driver = webdriver.Remote(
                    desired_capabilities=DesiredCapabilities.FIREFOX 
                    #uncomment for use with remote driver
                    command_executor='http://127.0.0.1:4444/wd/hub'
                )
             '''
    
3) ./main.py -u http://example.com

B) deploy using BROWSER DRIVER
1)    driver = webdriver.Chrome(chrome_options=options, executable_path=self.pathselenium +"chromedriver.exe"
      (You can use Firefox the driver is in inside of the folder selenium_standalone)
2)  ./main.py -u http://example.com

C) deploy using docker

1) 
2) 
3) 

D) for test

1) go to folder test or add you own test of selenium pass the url and the dirver you use
2) ./main.py -u http://example.com


Dependencies
wget -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install -r requirements.txt


Copyright (c) 2018, Gustavo Nieves Arreaza All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Dan McInerney nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.