from time import time
from time import sleep
from random import randint, sample

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from SUBPROCESS import scr_hlp


class CustomException(Exception):
    pass


class ScrapProxy:
    nb_proxy = 0  # int(sheet.cell(row_num, 1).value)
    print(nb_proxy)
    dispo = 50
    start_time = time()
    # useproxy = True
    # Scrapping
    @staticmethod
    def scrapingProxy():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        proxyScrap = webdriver.Chrome(chrome_options=chrome_options)
        proxyScrap.get("http://free-proxy.cz/fr/proxylist/country/all/https/ping/level1")
        time_stop = randint(5, 6)
        sleep(time_stop)
        #if scr_hlp.scr_hlp.is_element_exists('//*[@id="clickexport"]') :
        tableIP = proxyScrap.find_element_by_xpath('//*[@id="clickexport"]')
        ActionChains(proxyScrap).move_to_element(tableIP).pause(1).click(tableIP).perform()
        sleep(5)
        l = proxyScrap.find_element_by_xpath('//*[@id="zkzk"]').text
        list_proxy = l.split("\n")            
        proxyScrap.close()
        return list_proxy
        #else :
         #   return []

    @staticmethod
    def createlistProxy():
        #print("In scrapingproxy", scr_hlp.scr_hlp.useproxy)
        if scr_hlp.scr_hlp.useproxy == "True":
            listProxy = ScrapProxy.scrapingProxy()
            #print("First", listProxy)
            #scr_hlp.useproxy = True
            if ScrapProxy.nb_proxy <= len(listProxy) and listProxy != []:
                #print(ScrapProxy.nb_proxy)
                #print("Second ", listProxy)
                list_proxy_to_use = sample(listProxy, int(ScrapProxy.nb_proxy))
                scr_hlp.scr_hlp.print_if_DEBUG(f"Proxy télécharger avec succès {list_proxy_to_use}")
                return list_proxy_to_use
            else:
                #print("Else", listProxy)
                #print(ScrapProxy.useproxy)
                #print(scr_hlp.scr_hlp.useproxy)
                # scr_hlp.scr_hlp.print_if_DEBUG("Proxy manuel récupéré avec succès" + scr_hlp.useproxy + scr_hlp.scr_hlp.config["ProxyManuel"].to_list())
                #print("list proxy", scr_hlp.scr_hlp.dict_all_var["tab_proxy_manuel"].split(","))
                return scr_hlp.scr_hlp.dict_all_var["tab_proxy_manuel"].split(",") #scr_hlp.scr_hlp.config["ProxyManuel"].to_list()  # ['140.227.61.25:58888', '36.89.18.217:8080',
            # '195.201.61.51:8000', '159.69.66.224:8080', '140.227.66.105:58888']
        else:
            return []

"""
from time import time
from time import sleep
from random import randint, sample

from selenium import webdriver

from SUBPROCESS import scr_hlp


class CustomException(Exception):
    pass


class ScrapProxy:
    nb_proxy = 0  # int(sheet.cell(row_num, 1).value)
    print(nb_proxy)
    dispo = 50
    start_time = time()
    useproxy = True
    # Scrapping
    @staticmethod
    def scrapingProxy():
        proxyScrap = webdriver.Chrome()
        proxyScrap.get("https://www.freeproxylists.net/fr/?c=&pt=&pr=HTTPS&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=" + str(ScrapProxy.dispo))
        time_stop = randint(5, 6)
        sleep(time_stop)
        tableIP = proxyScrap.find_element_by_css_selector(
            "body > div:nth-child(3) > div:nth-child(2) > table:nth-child(8) > tbody:nth-child(1)")
        allTagTR = tableIP.find_elements_by_tag_name("tr")
        proxy = []
        allTagTR.pop(0)
        for tr in allTagTR:
            time_stop = randint(3, 5)
            sleep(time_stop)
            allTagTD = tr.find_elements_by_tag_name("td")
            if len(allTagTD) >= 2:
                s = str(allTagTD[0].text) + ":" + str(allTagTD[1].text)
                proxy.append(s)
        proxyScrap.close()
        return proxy

    @staticmethod
    def createlistProxy():
        if ScrapProxy.useproxy:
            listProxy = ScrapProxy.scrapingProxy()
            if ScrapProxy.nb_proxy <= len(listProxy) and listProxy != []:
                print(ScrapProxy.nb_proxy)
                print(listProxy)
                list_proxy_to_use = sample(listProxy, int(ScrapProxy.nb_proxy))
                s = "Proxy télécharger avec succès "
                scr_hlp.scr_hlp.print_if_DEBUG(s) + list_proxy_to_use
                return list_proxy_to_use
            else:
                scr_hlp.useproxy = False
                scr_hlp.scr_hlp.print_if_DEBUG("Proxy manuel récupéré avec succès" + scr_hlp.scr_hlp.config["ProxyManuel"].to_list())
                return scr_hlp.scr_hlp.config["ProxyManuel"].to_list()  # ['140.227.61.25:58888', '36.89.18.217:8080',
            # '195.201.61.51:8000', '159.69.66.224:8080', '140.227.66.105:58888']
        else:
            return []"""
            
