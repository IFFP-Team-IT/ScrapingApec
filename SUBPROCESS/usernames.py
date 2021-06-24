import os
from datetime import datetime, timedelta
from time import sleep
from random import randint, sample
import pandas as pd
import xlrd
import xlsxwriter
from SUBPROCESS import xlsx_hlp

from SUBPROCESS import scr_hlp
from SUBPROCESS import ScrapProxy
list_sheets = ["etat_civil_candidats", "compétences", "langues", "atouts", "nb_moments_cles"]


class CustomException(Exception):
    pass

#extrapecCorrection
class Users:
    loop = 0
    row_num = 1
    proxy_row_num = 1
    filename = "usernames.xlsx"
    wb = None
    ws = None
    headers = ["username", "password", "totalvisits"]
    visitslimit = 21
    skip_current_user = False
    list_loop = []
    nb_visits_avt_pause = 1
    #for i in range(nb_visits_avt_pause, visitslimit, nb_visits_avt_pause):
    #    list_loop.append(i)
    cpt_loop = 0
    file_extract = ""
    
    def list_looper(v_limit, nb_v_avt_pause):
        looper = []
        for i in range(nb_v_avt_pause, v_limit, nb_v_avt_pause):
            looper.append(i)
        if looper[len(looper)-1] != v_limit:
            looper.append(v_limit)
        return looper

    @staticmethod
    def convert_visits_to_zero(cell):
        return 0

    @staticmethod
    def create_csv(file, list_sheets):
        for sheet in list_sheets:
            if (sheet == "etat_civil_candidats"):
                data = pd.read_excel(file, sheet_name="main")
            elif sheet == "langues":
                data = pd.read_excel(file, sheet_name="lang")
            else:
                data = pd.read_excel(file, sheet_name=sheet)
            data.to_csv(file.replace(".xlsx", "-" + sheet) + ".csv", index=False, encoding='UTF-8')

    @staticmethod
    def get_credentials(count_visit):

        wait = False
        filename = os.path.join("SUBPROCESS", Users.filename)
        # SUBPROCESS.scr_hlp.scr_hlp.print_if_DEBUG("Opening an existing sheet named = %s" % filename)
        wbRD = xlrd.open_workbook(filename)
        sheet = wbRD.sheets()[0]
        Users.wb = xlsxwriter.Workbook(filename)
        ws = Users.ws = Users.wb.add_worksheet(sheet.name)
        if not Users.row_num < sheet.nrows:
            wait = True
            Users.row_num = 1
        lastvisit = sheet.cell(Users.row_num, 3).value
        time_diff = (datetime.strptime(lastvisit, "%Y-%m-%d %H:%M:%S.%f") + timedelta(days=1)) - datetime.now()
        if count_visit:
            scr_hlp.scr_hlp.pause_if_EXTRADEBUG(
                f"({datetime.strptime(lastvisit, '%Y-%m-%d %H:%M:%S.%f')}"
                f" + {timedelta(days=1)}) - {datetime.now()}"
                f"= {time_diff}")

        if lastvisit != "" and time_diff.days == 0:
            if wait:
                scr_hlp.scr_hlp.print_if_DEBUG(
                    f"All users reached to their limits. Applied wait for {time_diff.total_seconds()} seconds."
                    f"\nShould be end at {datetime.now() + time_diff}")
                # sleep(time_diff.total_seconds())

                # Users.create_csv(scr_hlp.scr_hlp.file_extract, list_sheets)
                # f2 = os.listdir(str(xlsx_hlp.xlsx_hlp.folder_name))
                # for f in f2:
                #     if not os.path.isdir("BDD_" + str(xlsx_hlp.xlsx_hlp.folder_name.upper())):
                #         os.mkdir("BDD_" + str(xlsx_hlp.xlsx_hlp.folder_name.upper()))
                #     os.path.join("BDD_" + str(xlsx_hlp.xlsx_hlp.folder_name.upper()), f)

                scr_hlp.scr_hlp.check_all_dezzipe(scr_hlp.scr_hlp.get_dwnload_dir_path())
                totalvisits = 0
                data = pd.read_excel("SUBPROCESS/usernames.xlsx", "Sheet1", converters={
                    "visits": Users.convert_visits_to_zero
                })
                data.to_excel("SUBPROCESS/usernames.xlsx", sheet_name="Sheet1", index=False)

                sleep(0)
                scr_hlp.scr_hlp.print_if_DEBUG(
                    "************************ FIN DU SCRAPING POUR LE " + datetime.now().strftime(
                        "%d %B 20%y") + "**************************")
                print("************************************ FIN ********************************")
                scr_hlp.scr_hlp.close_chrome()
                exit("rather Finish")
            else:
                totalvisits = int(sheet.cell(Users.row_num, 2).value)

                if totalvisits == Users.list_loop[Users.cpt_loop]:
                    #scr_hlp.scr_hlp.print_if_DEBUG("wait bro")
                    Users.cpt_loop += 1
                    #t = randint(180, 300)
                    #sleep(t)
                    scr_hlp.scr_hlp.proxies = ScrapProxy.ScrapProxy.createlistProxy()
                    scr_hlp.scr_hlp.prox_i = 0
        else:
            totalvisits = 0
        if Users.skip_current_user:
            totalvisits = Users.visitslimit
            scr_hlp.scr_hlp.pause_if_EXTRADEBUG("Trying to skip user")
            Users.skip_current_user = False
        if not totalvisits < Users.visitslimit:
            scr_hlp.scr_hlp.pause_if_EXTRADEBUG(
                f"This user has reached its limit. Total visits {totalvisits}. Trying other user.")
            scr_hlp.scr_hlp.proxies = ScrapProxy.ScrapProxy.createlistProxy()
            scr_hlp.scr_hlp.prox_i = 0
            Users.cpt_loop = 0
            scr_hlp.scr_hlp.initialize_browser_setup()
            Users.row_num += 1
            
            if scr_hlp.scr_hlp.useproxy:
                scr_hlp.scr_hlp.prox_i = 0
                Users.cpt_loop = 0
                scr_hlp.scr_hlp.initialize_browser_setup()
                raise CustomException("No need to continue the caller function.")
            else:
                return Users.get_credentials(count_visit)
        else:
            scr_hlp.scr_hlp.pause_if_EXTRADEBUG(f"totalvisits = {totalvisits}, Users.visitslimit = {Users.visitslimit}")

        for row in range(sheet.nrows):
            for col in range(sheet.ncols):
                ws.write(row, col, sheet.cell(row, col).value)
        if count_visit:
            ws.write(Users.row_num, 2, totalvisits + 1)
            ws.write(Users.row_num, 3, str(datetime.now()))
        else:
            ws.write(Users.row_num, 2, totalvisits)
            ws.write(Users.row_num, 3, lastvisit)
        Users.wb.close()
        uname = sheet.cell(Users.row_num, 0).value
        passw = sheet.cell(Users.row_num, 1).value
        if count_visit:
            scr_hlp.scr_hlp.pause_if_EXTRADEBUG(
                f"Username = {uname}\t pass = {passw}\t total visits = {totalvisits + 1}")
        return uname, passw
