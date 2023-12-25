#Basic Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn as sns
from pyodide.http import open_url
#Pyscript
from pyscript import document, display, when
pd.set_option('display.max_rows', 2000)

#output mapping
output_test = document.querySelector("#output_vacancies")

#conversion functions for salary
conversion_rates = {
    'USD': 90,
    'EUR': 110,
    'KZT': 0.20
}
def convert_to_rur(value, currency):
    if value is None or currency == 'RUR':
        return value
    return value * conversion_rates.get(currency, 1) 

def process_salary(salary_data):
    from_value = salary_data.get('from')
    to_value = salary_data.get('to')
    from_value = convert_to_rur(from_value, salary_data['currency'])
    to_value = convert_to_rur(to_value, salary_data['currency'])
    return {
        'from': from_value,
        'to': to_value,
        'currency': 'RUR',
        'gross': salary_data['gross']
    }
def calculate_single_number(data_dict):
    if data_dict is not None:
        from_value = data_dict.get('from')
        to_value = data_dict.get('to')

        if from_value is None and to_value is None:
            return None
        elif from_value is not None and to_value is not None:
            return (from_value + to_value) / 2
        elif from_value is not None:
            return from_value
        else:
            return to_value
#Очистка городов, работодателей, URL
def get_city(area):
	city=area.get('name')
	return city
	
def get_employer(employer):
	name=employer.get('name')
	return name
	
def clean_url(hh_url):
	url='https://spb.hh.ru/vacancy/'
	for i in hh_url:
		if i.isdigit():
			url+=str(i)
	return url
#Получение вакансий
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
	#Очищаем названия городов,работодателей, URL
	df['area']=df['area'].apply(get_city)
	df['employer']=df['employer'].apply(get_employer)
	df['url']=df['url'].apply(clean_url)
	#Фильтруем вакансии по зп и обрабатываем их
	df = df[df['salary'].notna()].reset_index(drop=True)
	df['salary_RUR']=df['salary'].apply(process_salary)
	df['single_number_RUR']= df['salary_RUR'].apply(calculate_single_number)
	df.loc[df['salary_RUR'].apply(lambda x: not x['gross']), 'single_number_RUR'] /= 0.87
	df['salary_gross_RUR']=df['single_number_RUR'].apply(round)
	#df=df.sort_values(by='salary_gross_RUR',ascending=False) Сортировка по ЗП
	df=df[['name','area','url','employer','salary_gross_RUR']].reset_index(drop=True)
	#Вывод пользователю таблицы	
	output_test.innerText = 'Найдено вакансий с открытыми ЗП:'+str(len(df))
	display(df, target="pandas-output", append=False)
	#Гистограмма
	plt.clf()
	ax=sns.histplot(df['salary_gross_RUR'],bins=int(len(df)/2))
	salary_hist=ax.get_figure()
	display(salary_hist, target="statistics", append=False)