import sqlite3
from PyQt5.QtWidgets import QFileDialog
import pandas as pd

class Database_Controller():
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cur = self.conn.cursor()
        
        
        self.cur.execute("\
        CREATE TABLE if not exists locations(\
            location_id INTEGER PRIMARY KEY, \
            location_name TEXT               \
        )")
        
        self.cur.execute("\
        CREATE TABLE if not exists workers(\
            worker_id INTEGER PRIMARY KEY, \
            worker_name TEXT,              \
            work_location INTEGER,         \
            FOREIGN KEY(work_location) REFERENCES locations(location_id) \
        )")


        self.cur.execute("\
        CREATE TABLE if not exists visits(\
            worker_id INTEGER NOT NULL,   \
            location_id INTEGER NOT NULL, \
            visit_datetime TEXT NOT NULL, \
            PRIMARY KEY (worker_id,location_id,visit_datetime), \
            FOREIGN KEY(worker_id) REFERENCES workers(worker_id),       \
            FOREIGN KEY(location_id) REFERENCES locations(location_id)  \
        )")
    def populate_from_csv(self):
        csv_file_name = QFileDialog.getOpenFileName(None, 'Open file', '',"CSV file (*.csv *.txt)")
        table_from_file = pd.read_csv(csv_file_name[0])
        test=len(table_from_file.columns)
        
        
        if (len(table_from_file.columns)==2 and all(table_from_file.columns==['location_id','location_name'])):
            command=["INSERT OR REPLACE INTO locations VALUES"]
            for index, row in table_from_file.iterrows():
                command.append(f"({row[0]},\"{row[1]}\"),")
            command[-1]=command[-1][:-1] #remove trailing comma from the end
            command="".join(command)
            self.cur.execute(command)
            self.conn.commit()
            return
        if (len(table_from_file.columns)==3 and all(table_from_file.columns==['worker_id','worker_name','work_location'])):
            command=["INSERT OR REPLACE INTO workers VALUES"]
            for index, row in table_from_file.iterrows():
                command.append(f"({row[0]},\"{row[1]}\",\"{row[2]}\"),")
            command[-1]=command[-1][:-1] 
            command="".join(command)
            self.cur.execute(command)
            self.conn.commit()
            return
        if (len(table_from_file.columns)==3 and all(table_from_file.columns==['worker_id','location_id','visit_datetime'])):
            command=["INSERT OR REPLACE INTO visits VALUES"]
            for index, row in table_from_file.iterrows():
                command.append(f"({row[0]},\"{row[1]}\", \"{row[2]}\"),")
            command[-1]=command[-1][:-1] 
            command="".join(command)
            self.cur.execute(command)
            self.conn.commit()
            return
        print("Unexpected table structure received, doing nothing as fallback.")
    def get_zone_links(self): #tuples, one per link (no 0->2 2->0 duplicates). no self connections
        command="SELECT DISTINCT w.work_location,v.location_id from workers W \
            left join visits V on W.worker_id=V.worker_id \
            WHERE w.work_location>v.location_id"
        self.cur.execute(command)
        links=self.cur.fetchall()
        print(links)
    def get_zone_populations(self):
        command="SELECT work_location, count(*) from workers group by work_location"
        self.cur.execute(command)
        populations=self.cur.fetchall()
        print(populations)
            