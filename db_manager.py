import sqlite3
from pyscript import document
db_status = document.querySelector("#db_status")
def create_db(event):
	conn = sqlite3.connect('request_log.db') 
	c = conn.cursor()
	
	c.execute('''
			  CREATE TABLE IF NOT EXISTS requests
			  ([request_id] INTEGER PRIMARY KEY, 
			  [vacancy_name] TEXT, 
			  [vacancies_found] INTEGER)
			  ''')
			  
	c.execute('''
          	INSERT INTO requests (request_id, vacancy_name)

                VALUES
                (1,'Test_name'),
				(2,'Test_name_2')
          ''')
	conn.commit()
	db_status.innerText = "DB is ready"