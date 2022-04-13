import sqlite3

from const import websites
from excel import load_xlsx_to_db
from main import download_form
import os, shutil


def start_job():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    cur.execute("Select * from tasks where progress='Not Started'")
    result = cur.fetchall()
    if result:
        for job in result:
            task_dispatcher(job[1], job[2], job[3], job[4], job[5], job[6])
        update_main_progress()
    else:
        print("No jobs to execute")
    # изменяем прогресс


    print("Удаляем скачанные файлы")
    delete_downloads()


def start_new_job():
    # reset_statuses() #Для сброса статусов с задании.
    add_jobs_table(websites)
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    cur.execute("Select * from tasks")
    result = cur.fetchall()
    if result:
        for job in result:
            task_dispatcher(job[1], "Not Started", "Not Started", "Not Started", "Not Started", "Not Started")
        update_main_progress()
    else:
        print("No jobs to execute")
    # изменяем прогресс


    print("Удаляем скачанные файлы")

    delete_downloads()


def task_dispatcher(website, progress, progress2018, progress2019, progress2020, progress2021):
    if progress == "Not Started":
        if progress2018 == "Not Started":
            start_a_job(website, 2018)
        if progress2019 == "Not Started":
            start_a_job(website, 2019)
        if progress2020 == "Not Started":
            start_a_job(website, 2020)
        if progress2021 == "Not Started":
            start_a_job(website, 2021)


def start_a_job(website, year):
    result, file_path = download_form(website, year)
    print("Удалось скачать форму? " + str(result))
    if result:
        #
        bool_loaded = load_xlsx_to_db(file_path)
        if bool_loaded:
            update_status(website, "progress" + str(year), "Success")
        else:
            update_status(website, "progress" + str(year), "Failed")
    else:
        update_status(website, "progress" + str(year), "Not Found")


def update_status(website, progress_type, success):
    print("Updating status of " + str(website) + " " + progress_type + " to " + success)
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    try:
        cur.execute(f"update tasks SET {progress_type} ='{success}'where website='{website}' ")
        conn.commit()
    except Exception as ex:
        print(ex)




def delete_downloads():
    folder = 'downloads'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))





def add_jobs_table(sites):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    for i in range(len(sites)):
        cur.execute(
            f"INSERT OR REPLACE INTO tasks(wid, website, progress, progress2018, progress2019,progress2020,progress2021, comment) VALUES(?, ?, 'Not Started','Not Started','Not Started','Not Started','Not Started', 'S');",
            (i, str(sites[i])))
        conn.commit()

    print("The table is now filled")


def update_main_progress():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute("Select * from tasks")
    results = cur.fetchall()

    for row in results:
        if row[3] == "Failed" or row[3] == "Failed" or row[3] == "Failed" or row[3] == "Failed":
            result = "Failed"
        else:
            result = "Success"
        cur.execute(f"update tasks SET progress ='{result}'")
        conn.commit()

##

# def reset_statuses():
#     conn = sqlite3.connect('tasks.db')
#     cur = conn.cursor()
#     cur.execute(
#         "Update tasks set progress='Not Started',progress2018='Not Started',progress2019='Not Started',progress2020='Not Started',progress2021='Not Started'")
#     conn.commit()




