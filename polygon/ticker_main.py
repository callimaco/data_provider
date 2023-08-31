"""This is the main of the module collector, here the functionalities 
    of this module are used to download, filter and store data"""

from polygon.get_data.get_data import Ticker
from scriba.scriba.scriba import DbManager
from secret.secret_man.secret_man import SecretManager as sm
import time
import mysql.connector as mc

end_point = Ticker()
db = DbManager(db='finance', table='ticker')

while True:

    with mc.connect(**sm.config(db='finance')) as cnx:
        crs = cnx.cursor()
        end_point.data_getter()
        db.write(crs= crs, cnx= cnx, data= end_point.results)
        cnx.commit()

    time.sleep(end_point.waiting_time)

    if not end_point.flag: break