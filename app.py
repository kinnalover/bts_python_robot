import sqlite3

from job_functions import start_job,  start_new_job


from model import create_companies_db, create_table, delete_all_info_companies

#Запускаем чтоб начать новую работу
#start_new_job()


#Запускаем, чтоб продолжить работу
start_job()
# conn = sqlite3.connect('tasks.db')
# cur = conn.cursor()
# cur.execute(f"update tasks SET progress ='Not Started' where website ='http://akm.kgd.gov.kz'")





#create_table()
#create_companies_db()



#delete_all_info_companies()