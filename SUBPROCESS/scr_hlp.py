#!/usr/bin/env python3
# coding=UTF-8
#extrapecCorrection
import os
import shutil
import sys
import urllib.request
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from SUBPROCESS.usernames import Users, CustomException
from threading import Thread
from zipfile import ZipFile
from SUBPROCESS.database import DB
from datetime import date
from SUBPROCESS import ScrapProxy

def save_current_page(html):
    #scr_hlp.print_if_DEBUG("Saving current page.")
    with open(os.path.join("SUBPROCESS", "current_page.html"), "w", encoding="utf-8") as f:
        f.write(html)
    f.close()
    #scr_hlp.print_if_DEBUG("Current page saved.")



class scr_hlp:
    config = pd.read_excel("Config.xlsx")
    dict_all_var={}
    path_to_check=""
    month = ""
    num_week = 1
    fileLog = ""
    DEBUG = False
    EXTRADEBUG = False
    d = None
    dwnload_dir = ""
    dossier = ""
    file_extract =""
    configFileLog = ""
    prox_i = 0
    useproxy = False
    proxies = [] # ['41.229.253.214:8080', '140.227.65.129:58888', '140.227.62.35:8080', '41.223.119.156:3128', '140.227.66.105:58888']
    list_page_URL = ""
    @staticmethod
    def deleteNan(l):
        l1=[]
        for i in l:
            if type(i) != float:
                l1.append(i)
        return l1
    @staticmethod
    def pause_if_EXTRADEBUG(pausing_msg):
        if not scr_hlp.EXTRADEBUG:
            user_input = input(pausing_msg + " (Enter to continue false to turn off pausing...)")
            if user_input.lower() == "false":
                scr_hlp.EXTRADEBUG = True  # False ancienne valeur
        else:
            scr_hlp.print_if_DEBUG(pausing_msg)

    @staticmethod
    def print_if_DEBUG(log):
        if scr_hlp.DEBUG:
            scr_hlp.logs_verif(log)

    @staticmethod
    def logs_verif(s): # allows to write in files create every week in directory FILES
        if not os.path.isdir(scr_hlp.dossier):
            os.mkdir(scr_hlp.dossier)
        #scr_hlp.num_week = int(scr_hlp.emptyfileLog(os.path.join("SUBPROCESS", scr_hlp.configFileLog)))
        if scr_hlp.num_week == 5:
            scr_hlp.createDirByMonth()
        file = os.path.join(scr_hlp.dossier, scr_hlp.fileLog + ".txt")
        files = open(file, "a", encoding="utf-8")
        files.write(str(s) + "\n")
        files.close()

    @staticmethod
    def get_dwnload_dir_path():
        rep = os.path.join(os.path.dirname(os.path.abspath(__file__)), scr_hlp.dwnload_dir)
        #rep = scr_hlp.dwnload_dir
        return rep

    @staticmethod
    def start_chrome(proxy=""):
        options = Options()

        # Added from SUBPROCESS.IAO
        if not scr_hlp.EXTRADEBUG:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # End editing
        if proxy != "":
            scr_hlp.print_if_DEBUG(f"using proxy for chrome = {proxy}")
            options.add_argument(f'--proxy-server={proxy}')
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "plugins.always_open_pdf_externally": True,
            "download.default_directory": scr_hlp.get_dwnload_dir_path(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        params = {'behavior': 'allow', 'downloadPath': scr_hlp.get_dwnload_dir_path()}
        scr_hlp.d = webdriver.Chrome(options=options)
        #options=options
        scr_hlp.d.set_page_load_timeout = 60

        scr_hlp.d.execute_cdp_cmd('Page.setDownloadBehavior', params)  # a revoir

    @staticmethod
    def close_chrome():
        try:
            scr_hlp.d.quit()
            scr_hlp.print_if_DEBUG("Naviateur fermé avec succès")
        except:
            pass
        finally:
            scr_hlp.d = None

    @staticmethod
    def initialize_browser_setup():
        scr_hlp.close_chrome()
        scr_hlp.print_if_DEBUG(f"Applying proxy = {scr_hlp.proxies[scr_hlp.prox_i]}") if scr_hlp.useproxy == "True" else scr_hlp.print_if_DEBUG(
            "no proxy applied")
        if scr_hlp.useproxy == True:
            proxy = scr_hlp.proxies[scr_hlp.prox_i]
            scr_hlp.start_chrome(proxy)
        else:
            scr_hlp.start_chrome()
        scr_hlp.prox_i += 1
        scr_hlp.load_page(scr_hlp.list_page_URL, count_visit=False, do_handle_login=False)  # ici
        sleep(3)
        scr_hlp.click_element('//*[@id="onetrust-accept-btn-handler"]')#//button[@class='optanon-allow-all accept-cookies-button']

    @staticmethod
    def is_internet_connected():

        try:
            scr_hlp.print_if_DEBUG("checking connection")
            urllib.request.urlopen('https://www.yahoo.com')
            scr_hlp.print_if_DEBUG("Connected")
            return True
        except:
            print("Connection Error")
            return False

    @staticmethod
    def wait_until_connected():
        while True:
            if scr_hlp.is_internet_connected():
                break
            else:
                print("Trying again to connect.")

    @staticmethod
    def load_page(url, count_visit, do_handle_login=True, wait_ele_xpath="", ele_count=1, refresh_also=True):
        count = 0
        while True:
            try:
                scr_hlp.load_page_helper(url, count_visit, do_handle_login, wait_ele_xpath, ele_count, refresh_also)
                sleep(3)
                break
            except Exception as e:
                scr_hlp.pause_if_EXTRADEBUG(f"Error: {e}\nTrying again realoading.")
                count += 1
                if count == 3:
                    scr_hlp.pause_if_EXTRADEBUG(f"Skipping current user")
                    Users.skip_current_user = True
                    count = 0
            finally:
                if(scr_hlp.is_element_exists('//*[@id="cgvAcceptees"]')):
                    checkboxes = scr_hlp.d.find_elements_by_xpath('//*[@id="cgvAcceptees"]')
                    for checkbox in checkboxes:
                        if not checkbox.is_selected():
                            checkbox.click()
                    scr_hlp.d.find_elements_by_xpath('//*[@id="candidapec"]/div/apec-accepter-cgv/div/div/div/div/div/button').click()  
                #html = scr_hlp.d.find_element_by_tag_name("html").get_attribute("outerHTML")
                #Thread(target=save_current_page, args=(html,)).start()

    @staticmethod
    def load_page_helper(url, count_visit, do_handle_login=True, wait_ele_xpath="", ele_count=1, refresh_also=True):
        scr_hlp.print_if_DEBUG(f"load_page(url={url}, do_handle_login={do_handle_login},"
                               f" wait_ele_xpath={wait_ele_xpath}, ele_count={ele_count},"
                               f" refresh_also={refresh_also}, count_visit={count_visit})")
        scr_hlp.wait_until_connected()
        scr_hlp.print_if_DEBUG("loading start")
        scr_hlp.d.get(url)
        scr_hlp.print_if_DEBUG("loading complete")
        if refresh_also:
            scr_hlp.d.refresh()
        if do_handle_login:
            try:
                username, password = Users.get_credentials(count_visit)
                # scr_hlp.pause_if_EXTRADEBUG("Login check")
                while scr_hlp.handle_login(username, password):
                    # scr_hlp.pause_if_EXTRADEBUG("Tried to login")
                    sleep(3)
                    if scr_hlp.is_element_exists("//*[contains(text(),"
                                                 "'Votre identifiant ou votre mot de passe est incorrect.')"
                                                 " and not(contains(@class,'alert-d-none'))]"):
                        command = input(f"Webpage is saying that your credentials are wrong.\n"
                                        f"Recheck the credentials username={username}, password={password}"
                                        f" listed in row num {Users.row_num} and enter y to continue: ")
                        if command.lower() != 'y':
                            scr_hlp.d.quit()
                            sys.exit()
                        else:
                            scr_hlp.d.refresh()
                            username, password = Users.get_credentials(count_visit)
                    else:
                        html = scr_hlp.d.find_element_by_tag_name("html").get_attribute("outerHTML")
                        Thread(target=save_current_page, args=(html,)).start()
                        scr_hlp.print_if_DEBUG("Login success")
                        break
            except CustomException as ce:
                scr_hlp.print_if_DEBUG("\t\tMy Custom Exception: Browser reopened " + str(ce))
                scr_hlp.load_page(url=url, count_visit=count_visit, do_handle_login=do_handle_login,
                                  wait_ele_xpath=wait_ele_xpath, ele_count=ele_count, refresh_also=refresh_also)
                return

        if wait_ele_xpath != "":
            for i in range(0, 30):
                pass
                scr_hlp.print_if_DEBUG(f"Waiting for {wait_ele_xpath}, iteration = {i}")
                if len(scr_hlp.d.find_elements_by_xpath(wait_ele_xpath)) >= ele_count:
                    scr_hlp.print_if_DEBUG(f"Elements found")
                    break

                elif i == 11:
                    # ans = input("Waited too long but page is not loading its dynamic contents."
                    #             " Do you want to try load again? (y)")
                    # if ans.lower() == 'y':
                    
                    scr_hlp.load_page(url=url, count_visit=count_visit, do_handle_login=do_handle_login,
                                      wait_ele_xpath=wait_ele_xpath, ele_count=ele_count, refresh_also=refresh_also)
                elif i % 3 == 0:
                    if len(scr_hlp.d.find_elements_by_xpath(wait_ele_xpath)) != 0:
                        break
                    scr_hlp.print_if_DEBUG(f"Refreshing browser. Because {wait_ele_xpath} not found.")
                    scr_hlp.d.refresh()
                    #scr_hlp.proxies = ScrapProxy.ScrapProxy.createlistProxy()
                    #scr_hlp.prox_i = 0
                    scr_hlp.initialize_browser_setup()
                sleep(5)

    @staticmethod
    def handle_login(username, password):
        while True:
            if len(scr_hlp.d.find_elements_by_xpath('//*[@id="emailid"]')) >= 1:
                break
            # print("moi2", scr_hlp.d.find_elements_by_xpath('//*[@id="emailid"]'), " ",
            #       len(scr_hlp.d.find_elements_by_xpath('//*[@id="emailid"]')))
            sleep(1)
        login_script = f"""
            username_node = document.querySelector("#emailid");
            if(username_node.offsetParent === null)
                return false;
            else
            {{
                password_node = document.querySelector("#password");
                username_node.value = '{username}';
                password_node.value = '{password}';
                document.querySelector("#popin-connexion > div > div:nth-child(2) > div > form > button").click();
                return true;
            }}
            """
        scr_hlp.print_if_DEBUG("login with:" + login_script)
        return scr_hlp.d.execute_script(login_script)

    @staticmethod
    def is_next_page_exists():
        next_page_script = """
        nextpage = document.evaluate("//ul[contains(@class,'pagination')]/li/a[contains(text(),'Suiv.')]",
         document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
        if(nextpage)
        {
           return true;
        }
        else
        {
           return false;
        }
        """
        result = scr_hlp.d.execute_script(next_page_script)
        scr_hlp.print_if_DEBUG("next_page_script result: " + str(result))
        return scr_hlp.d.execute_script(next_page_script)

    @staticmethod
    def handle_download_items(profile_id):
        photo_url = ""
        if not DB.does_id_exists_in_DB(profile_id):
            scr_hlp.click_element("//button[contains(text(),'Autres actions')]")
            pdf_link = scr_hlp.d.find_element_by_xpath("//button[contains(text(),'Autres actions')]//following-sibling"
                                                       "::div/a[contains(text(),'Exporter')]").get_attribute("href")
            path_to_check = os.path.join(scr_hlp.get_dwnload_dir_path(), profile_id)
            params = {'behavior': 'allow', 'downloadPath': path_to_check}
            scr_hlp.d.execute_cdp_cmd('Page.setDownloadBehavior', params)

            scr_hlp.load_page(pdf_link, count_visit=False, refresh_also=False)

            if os.path.isdir(path_to_check):
                scr_hlp.dezippe_file(path_to_check)
                scr_hlp.rename_file(path_to_check, profile_id)
                scr_hlp.print_if_DEBUG("Le fichier" + profile_id +"a été dezzipé avec succès")

        photo_download_script = """
        node = document.evaluate("//*[contains(@id,'photo-profil')]/img[contains(@src,'no-photo.png')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
        if(node === null){
            node = document.evaluate("//*[contains(@id,'photo-profil')]/img", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
            if(node !== null){
                var a = document.createElement('a');
                a.href = node.src;
                a.download = node.src.substring(node.src.lastIndexOf('/') + 1);
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                return node.src;
            }else{
                return "Aucune photo trouvé";
            }
        }
        return "";
        """
        photo_url = scr_hlp.d.execute_script(photo_download_script)
        return photo_url

    @staticmethod
    def add_prefix_to_filename(prefix, time_to_wait=60):
        folder_of_download = scr_hlp.get_dwnload_dir_path()
        time_counter = 0
        while len(os.listdir(folder_of_download)) == 0:
            pass
        while True:
            try:
                filename = max(
                    [f for f in os.listdir(folder_of_download)],
                    key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)))
                break

            except:
                pass
        while '.part' in filename:
            sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:
                scr_hlp.pause_if_EXTRADEBUG("Waited for file to download for 60 sec. Prefix is not added.")
                return
        filename = max([f for f in os.listdir(folder_of_download)],
                       key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)))
        try:
            shutil.move(os.path.join(folder_of_download, filename),
                        os.path.join(scr_hlp.get_dwnload_dir_path(), prefix + "_" + filename))
            scr_hlp.pause_if_EXTRADEBUG("prefix %s added to download file" % id)
        except:
            scr_hlp.pause_if_EXTRADEBUG("prefix %s couldn't added to download file" % id)
            pass

    @staticmethod
    def get_element_text(xpath):
        if scr_hlp.is_element_exists(xpath):
            return scr_hlp.d.find_element_by_xpath(xpath).text
        else:
            return "Not found"

    @staticmethod
    def get_element(xpath):
        if scr_hlp.is_element_exists(xpath):
            return scr_hlp.d.find_element_by_xpath(xpath)
        else:
            return None

    @staticmethod
    def is_element_exists(xpath):
        try:
            scr_hlp.d.find_element_by_xpath(xpath)
            scr_hlp.print_if_DEBUG("Cet element " + xpath + "existe")
            return True
        except:
            scr_hlp.print_if_DEBUG("Cet element " + xpath + "n'existe pas")
            return False

    @staticmethod
    def click_element(xpath, xpath2=""):
        if scr_hlp.is_element_exists(xpath):
            scr_hlp.print_if_DEBUG("Clicking %s" % xpath)
            result = scr_hlp.d.find_element_by_xpath(xpath).is_displayed()
            sleep(5)
            if(xpath == '//*[@id="onetrust-accept-btn-handler"]' or xpath == "button[@class='optanon-allow-all accept-cookies-button']"):
                if(xpath=="button[@class='optanon-allow-all accept-cookies-button']"):
                    scr_hlp.d.execute_script("""var n = document.evaluate("%s", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;n.scrollIntoView();n.click()""" % xpath)
                else:
                    scr_hlp.d.find_element_by_xpath(xpath).click()
            else:
                scr_hlp.d.execute_script("""var n = document.evaluate("%s", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;n.scrollIntoView();n.click()""" % xpath)
            scr_hlp.print_if_DEBUG("Clicking Complete")
            sleep(1)
            return True
        elif scr_hlp.is_element_exists(xpath2):
            scr_hlp.get_element_text(xpath2)
        return False

    @staticmethod
    def get_element_attr(xpath, attr):
        value = ""
        if scr_hlp.is_element_exists(xpath):
            value = scr_hlp.d.find_element_by_xpath(xpath).get_attribute(attr)
        return value if value is not None else "Element non trouvé"

    @staticmethod
    def emptyfileLog(file): # allows to count the number week in current month and create a files in directory LOG
        if not os.path.isfile(file):
            with open(file, 'w', encoding="utf-8") as f:
                f.close()
        with open(file, 'r') as f1:
            if os.path.getsize(file) > 0:
                yearISODay = date.today().isocalendar()[2]
                print("year", yearISODay)
                if yearISODay == 7:
                    scr_hlp.num_week += 1
                    with open(file, 'w') as f2:
                        f2.write(str(scr_hlp.num_week))
                        f2.write(" \n" + str(scr_hlp.month))
                    f2.close()
            else:
                with open(file, 'w', encoding="utf-8") as f2:
                    print("numero week ", scr_hlp.num_week)
                    f2.write(str(scr_hlp.num_week))
                    f2.write(" \n" + str(scr_hlp.month))
                f2.close()
            file = f1.readlines()[0]
        f1.close()
        return int(file.replace(" \n",""))

    def dezippe_file(filename): # allows you to unzip a zip file
        file = os.listdir(filename)
        for f in file:
            if f.endswith('.zip'):
                with ZipFile(os.path.join(filename, f), 'r') as zip:
                    zip.extractall(filename)
                os.remove(os.path.join(filename, f))

    def rename_file(filename, profile_id):# allows you to rename file pdf download in directory FILES/numberIdProfil
        file = os.listdir(filename)
        for f in file:
            if f.endswith('.pdf'):
                if f[0:2] == "CV":
                    name_file = f.split(".pdf")
                    name_file[0] = profile_id
                    new_name_file = ".pdf".join(name_file)
                    os.rename(os.path.join(filename, f), os.path.join(filename, new_name_file))
                    break

    @staticmethod
    def check_all_dezzipe(filename): # check if all directory in FILES are unzip
        for path, subdir, files in os.walk(filename):
            for f in files:
                if f.endswith('.zip'):
                    shutil.rmtree(path)
                    scr_hlp.print_if_DEBUG("Tout les fichiers ont été dezziper avec succès")

    @staticmethod
    def createDirByMonth(): # allows to create a directory every month and contains all files create every week of this month
        with open(os.path.join(scr_hlp.dossier, scr_hlp.fileLog+".txt"), "r") as f:
            file = f.readlines()[1]
            if scr_hlp.month != file and not os.path.isdir(str(scr_hlp.month)):
                os.mkdir(os.path.join(scr_hlp.dossier, str(scr_hlp.month)))
            files = os.listdir(scr_hlp.dossier)
            for f1 in files:
                if f1.split("month")[1].split(".txt")[0] == f.readlines()[1]:
                    shutil.move(f1, (os.path.join(scr_hlp.dossier, str(scr_hlp.month))))
                    scr_hlp.print_if_DEBUG("Le dossier " + scr_hlp.month + " a été créé avec succès")
        f.close()
