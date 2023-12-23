#Basic Libraries
import numpy as np
import tqdm 
import pandas as pd
import matplotlib.pyplot as plt
import json
from pyodide.http import open_url
#Pyscript
from pyscript import document, display, when
pd.set_option('display.max_rows', 300)
#Get vacancies
#output for test
output_test = document.querySelector("#output_vacancies")
#get_vacancies function
@when("click", "#get_vacancies")
def get_vacancies(event):
	text=str(document.querySelector("#vacancy_name").value)
	target_url='https://api.hh.ru/vacancies?text='+text
	r = json.loads(open_url(target_url).read())
	p=r['pages'] #Кол-во страниц выдачи
	#требуемые поля выгрузки
	vac = {'id':[],'name':[],'area':[],'salary':[],'address':[],'url':[],'employer':[],'snippet':[]}
	for i in range(0, p):
		page_url=target_url+'&page='+str(i)+'&per_page=20'
		page=open_url(page_url).read()
		page_content=json.loads(page)['items']	
		for j in range(0,len(page_content)):
			for k in vac.keys():
				vac[k].append(page_content[j].get(k))
	df=pd.DataFrame.from_dict(vac, orient='columns')
	output_test.innerText = 'Найдено вакансий:'+str(len(df))
	display(df, target="pandas-output", append=False)