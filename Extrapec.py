#!/usr/bin/env python3
# coding=UTF-8
#extrapecCOrrection
from SUBPROCESS.scr_hlp import scr_hlp, os
from SUBPROCESS.xlsx_hlp import xlsx_hlp
from datetime import datetime
from SUBPROCESS.usernames import Users
from SUBPROCESS.database import DB
from SUBPROCESS.ScrapProxy import ScrapProxy
print("************************************ DEBUT ********************************")
scr_hlp.dict_all_var = dict(zip(scr_hlp.config["variables"].to_list(),scr_hlp.config["valeur"].to_list()))# allow to retrieve the value in file Config.xlsx
#print("dictionnaire",scr_hlp.dict_all_var)
DB.SAVE_ON = True
#//*[@id="candidapec"]/div/apec-accepter-cgv/div/div/div/div/div/button

#//*[@id="cgvAcceptees"]

scr_hlp.DEBUG = True

#scr_hlp.EXTRADEBUG = scr_hlp.dict_all_var["EXTRADEBUG"]
#print("Extradebug",scr_hlp.EXTRADEBUG)

scr_hlp.EXTRADEBUG = True  # use for pausing on some places

# scr_hlp.dwnload_dir = "downloads" + datetime.now().strftime("%d%m%y")
# ScrapProxy.useproxy = 

scr_hlp.EXTRADEBUG = scr_hlp.dict_all_var["EXTRADEBUG"]
scr_hlp.useproxy= scr_hlp.dict_all_var["useproxy"] # False
#print("le proxy",scr_hlp.useproxy)

Users.nb_visits_avt_pause = int(scr_hlp.dict_all_var['nb_visite_avt_pause'])# this variable allow to pause when scraping to launch 
#print("nb_avt_pause",Users.nb_visits_avt_pause)
ScrapProxy.nb_proxy = int(scr_hlp.dict_all_var["nb_proxy"])
#print("nb_proxy", ScrapProxy.nb_proxy)
Users.visitslimit = int(scr_hlp.dict_all_var["nb_visits"])  # 4# nombre de visite# number visits who can do a one user
#print("visite limit", Users.visitslimit)
scr_hlp.dwnload_dir = scr_hlp.dict_all_var["downloadPDF"]
scr_hlp.dossier = scr_hlp.dict_all_var["dossierLogs"]
Users.list_loop = Users.list_looper(Users.visitslimit, Users.nb_visits_avt_pause) # this list allow contains the different values where the program should stop a few seconde and resume
#print("liste des loop",Users.list_loop)
#list_sheet_extracted = []
# this should be 800 after some days

xlsx_hlp.folder_name = scr_hlp.dict_all_var["dossierBdd"]
xlsx_hlp.filename = "apec_" + "20" + datetime.now().strftime("%y%m%d")
scr_hlp.fileLog = scr_hlp.dict_all_var["fichierDebugInLogDir"]
scr_hlp.configFileLog = scr_hlp.dict_all_var["configfileLog"] # file contains the current month and number of week of current month
scr_hlp.month = datetime.now().strftime("%B")
scr_hlp.num_week = scr_hlp.emptyfileLog(os.path.join("SUBPROCESS", scr_hlp.configFileLog))# this variable contains the number of the week of current month
#print("numero week ", scr_hlp.num_week)
scr_hlp.fileLog = scr_hlp.fileLog + str(scr_hlp.num_week) + "_month" + scr_hlp.month
datasource = "Apec"
# Filters
Fonctions = scr_hlp.dict_all_var["fonction"].split(",")#scr_hlp.deleteNan(
    #scr_hlp.config["Fonctions"].to_list())  # ['&fonctions=101829', '&fonctions=101828', '&fonctions=101830', ]
print("fonction", Fonctions)
lieux = scr_hlp.dict_all_var["lieux"].split(",")#scr_hlp.deleteNan(scr_hlp.config["Lieux"].to_list())  # ['&lieux=77', '&lieux=91', '&lieux=75', ]
print("lieux ", lieux)
secteursActivite = scr_hlp.dict_all_var["secteurAct"].split(",") #scr_hlp.deleteNan(scr_hlp.config["SecteurActivite"].to_list())# ['&secteursActivite=101755', '&secteursActivite=101753', '&secteursActivite=101757', ]
print("secteur activité ", secteursActivite)

list_page_URL = scr_hlp.dict_all_var["url"]
scr_hlp.list_page_URL = list_page_URL
#print("url", scr_hlp.list_page_URL)
scr_hlp.proxies = ScrapProxy.createlistProxy()
#print("voila la liste de proxies",scr_hlp.proxies)
Program_File = scr_hlp.dict_all_var["LastPageFile"]
scr_hlp.print_if_DEBUG("************************************ DEBUT ********************************")
scr_hlp.print_if_DEBUG("************************ DEBUT DU SCRAPING POUR LE " + datetime.now().strftime("%d %B 20%y") + "**************************")

if not os.path.isdir(scr_hlp.get_dwnload_dir_path()):
    os.mkdir(scr_hlp.get_dwnload_dir_path())
    scr_hlp.pause_if_EXTRADEBUG("Download : FILES created with success")


def get_last_page():  # permet de recupéré la dernière page
    if not os.path.isfile(os.path.join("SUBPROCESS", Program_File)):
        return 0
    f = open(os.path.join("SUBPROCESS", Program_File), "r")
    page = int(f.readline())
    scr_hlp.pause_if_EXTRADEBUG(f"Got Last Page = {page}")
    f.close()
    return page


def save_last_page(page):
    f = open(os.path.join("SUBPROCESS", Program_File), "w")
    f.write(str(page))
    f.close()


for fonc in Fonctions:
    for loc in lieux:
        for sec in secteursActivite:
            page_num = get_last_page()
            list_page_URL = list_page_URL + fonc + loc + sec
            xlsx_hlp.create_wb()
            scr_hlp.initialize_browser_setup()  # ici

            while True:
                save_last_page(page_num)
                """if(scr_hlp.is_element_exists('//*[@id="offres-colonnes"]/div[2]/div/apec-pagination/div/ul/li[1]/a')):
                    scr_hlp.d.find_elements_by_xpath('//*[@id="offres-colonnes"]/div[2]/div/apec-pagination/div/ul/li[1]/a').click() 
                    break 
                if(scr_hlp.is_element_exists("//a[@class='actualLink' and contains(@href,'/detailProfil/')]")):"""
                scr_hlp.load_page(list_page_URL % page_num, count_visit=False, wait_ele_xpath="//a[@class='actualLink' and contains(@href,'/detailProfil/')]", ele_count=20)
                candidates_nodes = scr_hlp.d.find_elements_by_xpath(
                    "//a[@class='actualLink' and contains(@href,'/detailProfil/')]")
                scr_hlp.print_if_DEBUG("Total candidates on this page are: " + str(len(candidates_nodes)))
                is_next_exists = scr_hlp.is_next_page_exists()
                scr_hlp.print_if_DEBUG("is_next_exists = %r" % scr_hlp.is_next_page_exists())
                c_page_URLs = []
                # save all urls in current page
                for i in range(0, len(candidates_nodes)):
                    c_URL = candidates_nodes[i].get_attribute("href")
                    # scr_hlp.print_if_DEBUG(str(i) + ": Candidate link: " + c_URL)
                    c_page_URLs.append(c_URL)

                scr_hlp.print_if_DEBUG("Total candidates on page_num = %i are %i" % (page_num, len(c_page_URLs)))
                # load those urls
                for j in range(0, len(c_page_URLs)):
                    scr_hlp.print_if_DEBUG("%i url" % (j + 1))
                    profile_id = c_page_URLs[j].split("/")[-1].split("?")[0]
                    if DB.does_id_exists_in_DB(profile_id):
                        scr_hlp.print_if_DEBUG(f"Skipping profile {profile_id} as it is already in DB")
                        continue
                    scr_hlp.load_page(c_page_URLs[j], count_visit=True,
                                      wait_ele_xpath='//*[@id="visit-top-content"]/div/div[1]', ele_count=1)
                    xpath_button_email_tel1 = "//button[normalize-space()='Afficher ses coordonnées']"
                    xpath_button_email_tel2 = "//p[@class='anonyme ng-star-inserted']"

                    scr_hlp.click_element(xpath_button_email_tel1,
                                          xpath_button_email_tel2)  # button hiding tel and mail
                    photo_url = scr_hlp.handle_download_items(profile_id)
                    row_main = []
                    row_main.append(datasource)  # datasource
                    row_main.append(xlsx_hlp.filename)
                    row_main.append(c_page_URLs[j])  # profile_link
                    row_main.append(profile_id)  # id
                    row_main.append(
                        scr_hlp.get_element_text('//*[@id="profil-infos"]/div[1]').replace("Mis à jour le",
                                                                                           "").strip())  # date_maj
                    row_main.append(
                        scr_hlp.get_element_text('//*[@id="profil-infos"]/span[1]').replace("Profil consulté",
                                                                                            "").replace("fois",
                                                                                                        "").strip())  # nb_consult
                    row_main.append(scr_hlp.get_element_text('//*[@id="profil-infos"]/span[2]').replace(
                        "Dernière consultation :", "").strip())  # date_der
                    row_main.append(photo_url)  # photo_url
                    row_main.append(scr_hlp.get_element_text("//*[@id='name']"))  # name
                    row_main.append(scr_hlp.get_element_text('//*[@id="poste"]'))  # poste
                    row_main.append(scr_hlp.get_element_text('//*[@id="experience"]'))  # exp
                    row_main.append(scr_hlp.get_element_text('//*[@id="title"]'))  # title
                    row_main.append(scr_hlp.get_element_text('//*[@id="dispo"]'))  # dispo

                    row_main.append(
                        scr_hlp.get_element_attr('//*[@id="adress-container"]/div/a',
                                                 "href"))  # file url
                    row_main.append(
                        scr_hlp.get_element_attr('//*[@id="action-buttons"]/div/ul/li/a',
                                                 "href"))  # file_dd_url
                    row_main.append(scr_hlp.get_element_attr("//*[contains(@id,'linkedin-icon')]/parent::a",
                                                             "href"))  # linkedin url
                    row_main.append(scr_hlp.get_element_text('//*[@id="visite-reseaux"]/div[2]/a[1]'))  # tell
                    row_main.append(scr_hlp.get_element_text('//*[@id="visite-reseaux"]/div[2]/a[2]'))  # mail
                    row_main.append(scr_hlp.get_element_text(
                        "//*[contains(text(),'Objectif et Souhaits professionnels')]/following-sibling::*"))  # obj
                    # row_main.append(scr_hlp.d.execute_script("""var fonc = document.evaluate("//*[contains(text(),'Fonctions :')]/parent::*/following-sibling::*", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;if(fonc){fonc = fonc.children;}else{return ""}str = "";for( i = 0;i<fonc.length;i++){str += fonc[i].innerText +";";}return str;"""))  # fonc
                    row_main.append(scr_hlp.get_element_text('//*[@id="box-souhaits"]/div[1]/div[2]'))
                    row_main.append(scr_hlp.get_element_text(
                        "//*[contains(text(),'Salaire souhaité :')]/parent::*/following-sibling::*"))  # sal
                    try:
                        lieux = scr_hlp.d.execute_script(
                            """var nodes = document.evaluate("//*[contains(text(),'Lieux :')]/parent::*/following-sibling::*", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue.children;str = "";for( i = 0;i<nodes.length;i++){str += nodes[i].innerText +";";}return str;""")
                    except:
                        lieux = ""
                    row_main.append(lieux)  # Lieux
                    # scr_hlp.print_if_DEBUG(row_main)
                    scr_hlp.print_if_DEBUG(
                        "Fiche contact du candidats" + profile_id + "were added in sheet main")

                    for k in range(0, len(row_main)):
                        xlsx_hlp.ws_main.write(xlsx_hlp.row_num_main, k, row_main[k])
                    xlsx_hlp.row_num_main += 1
                    DB.addtoDB(xlsx_hlp.headers_main, row_main, "main")
                    scr_hlp.print_if_DEBUG("Candidate contact form" + profile_id + "were added in bdd main")

                    scr_hlp.click_element(
                        "//section[contains(@class,'section-competences')]/*[contains(text(),'Voir les autres compétences (1)')]")
                    comp_eles = scr_hlp.d.find_elements_by_xpath(
                        "//*[@class='competence-name' and ./parent::div/following-sibling::div[@class='col-md-8']]/parent::div/parent::div")
                    for e in comp_eles:
                        stars_eles = e.find_elements_by_xpath(
                            ".//*[@class='competence-name']/following-sibling::div[contains(@class,'stars')]/*")
                        total_stars = 0
                        for se in stars_eles:
                            if "xstar-yellow.png" in se.value_of_css_property("background-image"):
                                total_stars += 1
                        row_comp = []
                        row_comp.append(profile_id)
                        row_comp.append(e.find_element_by_xpath(".//*[@class='competence-name']").text)  # comp
                        row_comp.append(str(total_stars))  # total stars
                        row_comp.append(e.find_element_by_xpath(".//*[@class='competence-level']").text)  # comp level
                        row_comp.append(e.find_element_by_xpath(
                            ".//*[@class='competence-name']/parent::div/following-sibling::div").text)  # comp desc
                        # scr_hlp.print_if_DEBUG("row_comp: " + str(row_comp))
                        scr_hlp.print_if_DEBUG(
                            "skills of candidates" + profile_id + "were added to the sheetmain")
                        for l in range(0, len(row_comp)):
                            xlsx_hlp.ws_comp.write(xlsx_hlp.row_num_comp, l, row_comp[l])
                        xlsx_hlp.row_num_comp += 1
                        DB.addtoDB(xlsx_hlp.headers_comp, row_comp, "compétences")
                        scr_hlp.print_if_DEBUG(
                            "skills of candidates" + profile_id + "were added in bdd competences")

                    lang_eles = scr_hlp.d.find_elements_by_xpath(
                        "//*[@class='competence-name' and not(./parent::div/following-sibling::div[@class='col-md-8'])]/parent::div")
                    for e in lang_eles:
                        stars_eles = e.find_elements_by_xpath(
                            ".//*[@class='competence-name']/following-sibling::div[contains(@class,'stars')]/*")
                        total_stars = 0
                        for se in stars_eles:
                            if "xstar-yellow.png" in se.value_of_css_property("background-image"):
                                total_stars += 1
                        row_lang = []
                        row_lang.append(profile_id)
                        row_lang.append(e.find_element_by_xpath(".//*[@class='competence-name']").text)  # lang
                        row_lang.append(str(total_stars))  # total stars
                        row_lang.append(e.find_element_by_xpath(".//*[@class='competence-level']").text)  # lang level
                        # scr_hlp.print_if_DEBUG("row_lang: " + str(row_lang))
                        scr_hlp.print_if_DEBUG(
                            "The languages speak by the candidates" + profile_id + "were added to the sheet lang")
                        for l in range(0, len(row_lang)):
                            xlsx_hlp.ws_lang.write(xlsx_hlp.row_num_lang, l, row_lang[l])
                        xlsx_hlp.row_num_lang += 1
                        DB.addtoDB(xlsx_hlp.headers_lang, row_lang, "lang")
                        scr_hlp.print_if_DEBUG(
                            "The languages speak by the candidates " + profile_id + "were added in bdd lang")

                    for e in scr_hlp.d.find_elements_by_xpath("//*[contains(@class,'list-atouts')]/p"):
                        row_atouts = []
                        row_atouts.append(profile_id)
                        row_atouts.append(e.text)
                        # scr_hlp.print_if_DEBUG("row_atouts: " + str(row_atouts))
                        scr_hlp.print_if_DEBUG(
                            "Assets by the candidate" + profile_id + "were added to the sheetatouts")
                        for l in range(0, len(row_atouts)):
                            xlsx_hlp.ws_atouts.write(xlsx_hlp.row_num_atouts, l, row_atouts[l])
                        xlsx_hlp.row_num_atouts += 1
                        DB.addtoDB(xlsx_hlp.headers_atouts, row_atouts, "atouts")
                        scr_hlp.print_if_DEBUG(
                            "Assets for the candidate" + profile_id + "were added in bdd atouts")

                    count = 0

                    for e in scr_hlp.d.find_elements_by_xpath(
                            "//section[contains(@class,'section-moments')]//ngu-tile"):
                        if (count > 0 and count % 3 == 0):
                            scr_hlp.click_element("//button[@class='slick-next hidden-xs']")
                        count += 1
                        dd_df = e.find_element_by_xpath(".//h4[contains(@class,'date')]").text.replace("De", "").split(
                            "à")
                        row_nb_mom = []
                        row_nb_mom.append(profile_id)
                        row_nb_mom.append(dd_df[0].strip())  # dd
                        if len(dd_df) > 1:
                            row_nb_mom.append(dd_df[1].strip())  # df
                        else:
                            row_nb_mom.append('')  # df
                        row_nb_mom.append(
                            scr_hlp.get_element_text("//ngu-tile[1]//div[1]//div[1]//div[1]//p[1]"))  # type
                        row_nb_mom.append(scr_hlp.get_element_text('//*[@id="box-moments-cles"]/section/div/apec'
                                                                   '-carousel/div/ngu-carousel/div/div['
                                                                   '1]/div/ngu-tile[1]/div/div/div[2]/h3'))  # title
                        row_nb_mom.append(scr_hlp.get_element_text('//*[@id="box-moments-cles"]/section/div/apec'
                                                                   '-carousel/div/ngu-carousel/div/div['
                                                                   '1]/div/ngu-tile[1]/div/div/div[2]/h5'))  # tagline
                        row_nb_mom.append(
                            scr_hlp.get_element_text(".//div[contains(@class,'companyName')]/span"))  # comp
                        row_nb_mom.append(scr_hlp.get_element_text('//*[@id="box-moments-cles"]/section/div/apec'
                                                                   '-carousel/div/ngu-carousel/div/div['
                                                                   '1]/div/ngu-tile[1]/div/div/div[2]/div/div[1]/span'))  # location
                        row_nb_mom.append(
                            scr_hlp.get_element_text('//*[@id="box-moments-cles"]/section/div/apec-carousel/div/ngu'
                                                     '-carousel/div/div[1]/div/ngu-tile[1]/div/div/div[2]/div/span'))  # desc
                        # scr_hlp.print_if_DEBUG("row_nb_mom: " + str(row_nb_mom))
                        scr_hlp.print_if_DEBUG(
                            "nb_moments_cles for the candidate" + profile_id + "were added to the sheet nb_moments_cles")
                        for l in range(0, len(row_nb_mom)):
                            xlsx_hlp.ws_nb_moments.write(xlsx_hlp.row_num_nb_moments, l, row_nb_mom[l])
                        xlsx_hlp.row_num_nb_moments += 1
                        DB.addtoDB(xlsx_hlp.headers_nb_moments, row_nb_mom, "nb_moments_cles")
                        scr_hlp.print_if_DEBUG(
                            "nb_moments_cles for the candidate" + profile_id + "were added in bdd nb_moments_cles")
                    xlsx_hlp.save_wb()  # delete if slow speed and uncomment below save_wb()
                    scr_hlp.pause_if_EXTRADEBUG("Data saved after profile visit")
                # xlsx_hlp.save_wb()# saves after a page
                scr_hlp.pause_if_EXTRADEBUG("Going to add page")
                if not is_next_exists:
                    break
                scr_hlp.pause_if_EXTRADEBUG("page added")
                page_num += 1
            xlsx_hlp.wb.close()
            scr_hlp.close_chrome()
            scr_hlp.print_if_DEBUG("finish adebo")
