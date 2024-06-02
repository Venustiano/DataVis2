# https://realpython.com/python-sqlite-sqlalchemy/
# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
# 

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, ForeignKeyConstraint
# from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# DB_URL="mysql+mysqldb://<user>:<password>@<host>:<port>/<db_name>"
# scoped_engine = create_engine(DB_URL)
# Base = declarative_base()
# Base.metadata.create_all(scoped_engine)

Base = declarative_base()

class Technique(Base):
    __tablename__ = "technique"
    tlibrary = Column(String(50), primary_key=True) 
    tname = Column(String(50), primary_key=True)
    url_repo = Column(String(512))

    def __repr__(self):
        return "<Technique(library='%s', name ='%s')>" % (self.tlibrary, self.tname)

class Experiment(Base):
    __tablename__ = "experiment"
    experiment_id = Column(Integer, primary_key=True) 
    tlibrary = Column(String(50))
    tname = Column(String(50))

    __table_args__ = (ForeignKeyConstraint([tlibrary, tname],
                                           [Technique.tlibrary, Technique.tname]),
                      {})
    
    results = Column(String)
    comment = Column(String)
    time_begin = Column(DateTime(timezone=True))
    time_end = Column(DateTime(timezone=True))
    params = Column(String,nullable= False)

# class Experiment_Technique(Base):
#     __tablename__ = 'experiment_technique'
#     experiment_id = Column(Integer, ForeignKey('experiment.experiment_id'), primary_key = True)
#     tech_lib_id = Column(String, ForeignKey('technique.tlibrary'), primary_key = True)
#     tech_method_id = Column(String, ForeignKey('technique.tname'), primary_key = True)