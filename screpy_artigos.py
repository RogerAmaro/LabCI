import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import  urlopen
from time import sleep
import os
import sqlite3
import PyPDF2


def getLinksfromPlanilha():
        date_sheet = pd.read_excel("/home/lab-pesquisa/Documentos/BRAPCI.xlsx",
        sheet_name= "Documentos Recuperados (407)")

        return ([i.replace("indexp","index") for i in date_sheet["Link"]], [x for x in date_sheet["Title"]])



def getlink_pdf(local_url):
    sleep(2)
    try:
        html = requests.get(local_url).content
    except Exception as erro:
        print(erro)
    soup = BeautifulSoup(html,'html.parser')
    linkDownload = soup.find_all(id='download')
    recover_url = str(linkDownload[0]).split('"')[3]
    print("url recuperada :",recover_url)
    return recover_url




def save_file(url,loc,name):
    path = loc+name+".pdf"
    try:
        r = requests.get(url, allow_redirects=True)
    except requests.exceptions.ConnectionError:
        return False

    print(r.content)

    try:
        open(path, 'wb').write(r.content)
    except OSError:
        return save_file(url,loc,name[:60]+"...")

    return "pdf salvo"


def chose_folder():
    folder = input("Folder location :")
    print("Iniciando o processo de extração...")
    return folder

def ExtractTextfromPdf(path_to_file):
    pages =''
    pdf_file = open(path_to_file, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    if read_pdf.isEncrypted:
        try:
            read_pdf.decrypt('')
        except NotImplementedError:
            return False
    number_of_pages = read_pdf.getNumPages()
    for pageNum in range(number_of_pages):
        page = read_pdf.getPage(pageNum)
        page_content = page.extractText()
        pages += page_content
    return pages




def mount_sql(path_name ="/home/lab-pesquisa/Documentos/pdfs/"):
    files = [f for f in os.listdir(path_name)]
    conn = sqlite3.connect("/home/lab-pesquisa/Documentos/data_files.db")
    cursor = conn.cursor()
    for pdf_name in files:
        text = ExtractTextfromPdf(path_name+pdf_name)
        cursor.execute("""INSERT INTO dados(artigos, texto) VALUES (?,?)""",(path_name,text))
        conn.commit()
        print("inserted to data")
    return "process finished"




# if __name__ == '__main__':
#     folder_loc = chose_folder()
#     pdfs_names = [str(x).replace('/'," ") for x in getLinksfromPlanilha()[1]]
#
#     all_links = getLinksfromPlanilha()[0]
#     for link,name in zip(all_links,pdfs_names):
#         # if os.path.isfile(folder_loc+name+".pdf"):
#         #     print("O arquivo ja existe na pasta")
#         # else:
#         save_file(getlink_pdf(link),folder_loc,name)
#
#
#
#

mount_sql()



