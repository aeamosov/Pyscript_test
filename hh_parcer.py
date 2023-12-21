#Basic Libraries
import numpy as np
import requests
import tqdm 
import pandas as pd
import matplotlib.pyplot as plt
import pyodide
#Pyscript
from pyscript import document
from pyscript import display
#Get vacancies
text=str(document.querySelector("#vacancy_name"))
def get_vacancies(event):
	target_url='https://api.hh.ru/vacancies?text='+text
	response = pyodide.http.open_url(target_url)
	r =response.json()
	print(r)
	p=r['pages'] #Кол-во страниц выдачи
	vac = []
	#print('Ожидайте, поиск займет до '+str(p*2)+' секунд')
	for i in tqdm(range(0, p)):
		v=pyodide.http.open_url(target_url+'?page='+i+'?per_page=20')
		vac.append(v.json())
	#Выгрузка вакансий
	vac_row=[]
	for i in range(0,p):
		l=len(vac[i]['items'])
		for j in range (0,l):
			vac_row.append(vac[i]['items'][j])
	df=pd.DataFrame.from_dict(vac_row, orient='columns')
	print('Вакансий найдено:',len(df.name))



