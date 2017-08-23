from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from  model import Request, Object
import config


engine = config.engine
Session = sessionmaker()
session = Session(bind=engine)
msg_id ={}


class workerWithRequest:
    def __init__(self):
        pass
    def check_uri(uri):
        ch = session.query(Request).filter_by(url=uri).first()
        if ch is None:
            return False
        else:
            return ch
    def insert(uri):
        add = Request(uri, None)
        session.add(add)
        session.commit()
    def update(id_uri, count):
        update = session.query(Request).filter_by(id=id_uri).first()
        update.count_objects = count
        session.commit()

class workerWithObject:
    def __init__(self):
        pass
    def check_object(object_uri):
        ch = session.query(Object).filter_by(link_object=object_uri).first()
        if ch is None:
            return False
        else:
            return ch
    def insert_object(id_uri ,object_uri, object_cost, object_meter, object_floor, object_pic):
        add = Object(id_uri,
                     object_uri,
                     object_cost,
                     object_meter,
                     object_floor,
                     object_pic)
        session.add(add)
        session.commit()
    def diff_object(object_uri, object_cost, object_meter, object_floor, object_pic):
        ch = session.query(Object).filter_by(
            link_object = object_uri,
            cost=object_cost,
            meter=object_meter,
            floor=object_floor,
            photo_object=object_pic
        )
        if ch is None:
            return False
        else:
            return True
    def update_object(object_uri, object_cost, object_meter, object_floor, object_pic, id_object):
        update = session.query(Request).filter_by(id=id_object).first()
        update.link_object = object_uri
        update.cost=object_cost
        update.meter = object_meter
        update.floor=object_floor
        update.photo_object=object_pic
        session.commit()




