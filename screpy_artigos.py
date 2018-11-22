import zipf
import math
import pandas as pd
from bs4 import BeautifulSoup
import requests
from time import sleep
from os import listdir
from PdfProcessing import ProcessingFile
import sqlite3

def gofman(list_rept):
	list_1=[]
	for i in list_rept:
		if i[1]==1:
			list_1.append(i)

	return (-1 + math.sqrt(1 + 8 * len(list_1)) / 2)


def sql_consulta(id=None, selection="all"):
	connection = sqlite3.connect("/home/roger/Documentos/Projetos/pesquisa/Pesquisa 18.2/pdf_data.db")
	c = connection.cursor()
	if selection=="all":
		c.execute("""SELECT text FROM pdfs """)
		rows = c.fetchall()
		return rows

	try:
		c.execute("""SELECT * FROM pdfs WHERE ID=(?)""",[str(id)])
		rows = c.fetchall()
		return rows
	except Exception as e:
		return e
def pdf_to_sql(path="/home/roger/Documentos/Projetos/pesquisa/Pesquisa 18.2/pdfs/"):
	files = [x for x in listdir(path)]
	ProObj = ProcessingFile()
	for i in files:
		print("Processing file:{}".format(i))
		try:
			text = ProObj.read_pdf(path+i)
			ProObj.save_On_Sql(text,i)
		except Exception as e:
			return e

def getLinksfromPlanilha():
	date_sheet = pd.read_excel(
		"/home/roger/Documentos/Projetos/pesquisa/Pesquisa 18.2/BRAPCI.xlsx", sheet_name="Documentos Recuperados (407)")
	return ([i.replace("indexp", "index") for i in date_sheet["Link"]], [x for x in date_sheet["Title"]])


def download_pdf(url,pathName):
	sleep(1)
	r = requests.get(url,stream=True)
	try:
		with open(pathName, 'wb') as f:
			f.write(r.content)
	except Exception as e:
		return e
def getlink_pdf(local_url):
	sleep(1)
	try:
		html = requests.get(local_url).content
		soup = BeautifulSoup(html, 'html.parser')
		linkDownload = soup.findAll(class_="col-md-2 col-xs-2 text-right")
		string = str(linkDownload).split('"')[3]
		return string[string.index("http"):-3]
	except Exception as e:
		return e

def ranking(words, zipf):
	wordsInT = []
	limSup = zipf + 5
	limInf = zipf - 5
	if limInf<0:
		limInf=0
	for i in words:
		if i[1]<limSup and i[1]>=limInf:
			wordsInT.append(i)

	return wordsInT





if __name__ == '__main__':
	words = ["gestão", "informação", "textual"]
	media = []
	text =[j for j in sql_consulta(selection="all")]
	for i in text:
		for k in i:
			text = zipf.CounterWords(k,"null")
			pontT= gofman(text)
			rnk = ranking(text,pontT)
			for w in rnk:
				if w[0] in words:
					print(w)





