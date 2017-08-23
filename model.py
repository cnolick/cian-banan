from sqlalchemy import Integer, Column, String, MetaData
import config
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = config.engine
metadata = MetaData()

class Request(Base):
    __tablename__ = 'Request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    count_objects = Column(String)

    def __init__(self, url, count_objects):
        self.url = url
        self.count_objects = count_objects
    def __repr__(self):
        return "<request(id={}," \
               "         url={}," \
               "         count_objects={}".format(self.id,
                                              self.url,
                                              self.count_objects)

class Object(Base):
    __tablename__ = 'Object'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_url = Column(Integer)
    link_object = Column(String)
    cost = Column(String)
    meter = Column(String)
    floor = Column(String)
    photo_object = Column(String)

    def __init__(self, id_url, link_object, cost, meter, floor, photo_object):
        self.id_url = id_url
        self.link_object = link_object
        self.cost = cost
        self.meter = meter
        self.floor = floor
        self.photo_object = photo_object
    def __repr__(self):
        return "<object(id={}" \
               "        id_url={}" \
               "        link_object={}" \
               "        cost={}" \
               "        meter={}" \
               "        floor={}" \
               "        photo_object={})>".format(self.id,
                                                  self.id_url,
                                                  self.link_object,
                                                  self.cost,
                                                  self.meter,
                                                  self.floor,
                                                  self.photo_object)

Base.metadata.create_all(engine)