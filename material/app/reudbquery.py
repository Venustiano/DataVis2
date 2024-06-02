from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert
from sqlalchemy import inspect
import pandas as pd
import os
from sqlalchemy.engine.url import URL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists

from reumodel import Base, Technique, Experiment

class SQlite_connect(object):
    def __init__(self, data_dir, appname):
        
        if not os.path.isdir(data_dir):
            print("Data dir does not exist!")
            try:
                os.makedirs(data_dir)
            except OSError:
                print ("Creation of the data directory %s failed" % data_dir)
            else:
                print ("Successfully created the data directory %s " % data_dir)

        db = {'drivername':'sqlite','database':data_dir+'/'+appname+'.sqlite3'}
        self.db_uri=URL.create(**db)
        # print(db_uri)

        # Disable echo for production mode

        # if not database_exists(self.db_uri):
        dbengine = create_engine(self.db_uri, echo=False)
        Base.metadata.create_all(dbengine, checkfirst=True)
        
        # self.session = Session()

    def method_key(self, lb, rmethod):
        engine = create_engine(self.db_uri,echo=True)
        Session = sessionmaker(bind=engine)()
        tkey = Session.get(Technique,(lb, rmethod))
        if not tkey:
            #  tkey=Session.add(Technique(tlibrary=lb, tname = rmethod))
            # Session.commit()
            stmt = insert(Technique).values(tlibrary=lb, tname = rmethod)
            with engine.connect() as conn:
                tkey = conn.execute(stmt)
                conn.commit()

        print(tkey)
        #self.query_df = pd.read_sql(query,engine)
        #print ('<> Query Sucessful <>')
        engine.dispose()
        return tkey

    def save_params(self, params, library, technique, results = None, timebegin = None, timeend = None, comment = None):
        technique_key = self.method_key(library,technique)
        engine = create_engine(self.db_uri,echo=True)
        Session = sessionmaker(bind=engine)()
        new_experiment = None
        if technique_key:
            stmt = insert(Experiment).values(params=params, tlibrary = library, tname = technique)
            with engine.connect() as conn:
                new_experiment = conn.execute(stmt)
                conn.commit()
        engine.dispose()
        return new_experiment
    
    def experiments(self):
        engine = create_engine(self.db_uri)
        query = f"SELECT * FROM experiment"
        self.query_df = pd.read_sql(query,engine)
        print ('<> Query Sucessful <>')
        engine.dispose()
        return self.query_df

    def get_experiment(self, id):
        engine = create_engine(self.db_uri)
        query = f"SELECT * FROM experiment WHERE experiment_id = '{id}';"
        self.query_df = pd.read_sql(query,engine)
        # print ('<> Query Sucessful <>')
        engine.dispose()
        return self.query_df
