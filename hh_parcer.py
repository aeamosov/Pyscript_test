#Basic Libraries
import numpy as np
import tqdm 
import pandas as pd
import matplotlib.pyplot as plt
import json
from pyodide.http import open_url
#Pyscript
from pyscript import document
from pyscript import display
#Get vacancies
#output for test
output_test = document.querySelector("#output_vacancies")
#get_vacancies function
def get_vacancies(event):
	text=str(document.querySelector("#vacancy_name").value)
	target_url='https://api.hh.ru/vacancies?text='+text
	r = json.loads(open_url(target_url).read())
	p=r['pages'] #Кол-во страниц выдачи
	vac = []
	#print('Ожидайте, поиск займет до '+str(p*2)+' секунд')
	for i in range(0, p):
		page_url=target_url+'&page='+str(i)+'&per_page=20'
		page=open_url(page_url).read()
		v=json.loads(page)
		vac.append(v)
	#Выгрузка вакансий
	vac_row=[]
	for i in range(0,p):
		l=len(vac[i]['items'])
		for j in range (0,l):
			vac_row.append(vac[i]['items'][j])
	df=pd.DataFrame.from_dict(vac_row, orient='columns')
	print('Вакансий найдено:',len(df.name))
	output_test.innerText = 'Вакансий найдено:'+str(len(df.name))
	
