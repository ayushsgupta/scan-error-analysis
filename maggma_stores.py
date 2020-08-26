from maggma.stores import MongoStore, GridFSStore

db = MongoStore(database="mp_rk_calculations",
                collection_name="tasks",
                host="mongodb03.nersc.gov",
                port=27017,
                username="mp_rk_calculations_ro",
                password="4df3t3t3554544",
                last_updated_field = "last_updated",
                key = "metadata.task_id")

elfcar_store = GridFSStore(database="mp_rk_calculations",
                           collection_name="elfcar_fs",
                           host="mongodb03.nersc.gov",
                           port=27017,
                           username="mp_rk_calculations_ro",
                           password="4df3t3t3554544",
                           last_updated_field = "last_updated",
                           key = "metadata.task_id")

chgcar_store = GridFSStore(database="mp_rk_calculations",
                           collection_name="chgcar_fs",
                           host="mongodb03.nersc.gov",
                           port=27017,
                           username="mp_rk_calculations_ro",
                           password="4df3t3t3554544",
                           last_updated_field = "last_updated",
                           key = "metadata.task_id")

aeccar0_store = GridFSStore(database="mp_rk_calculations",
                            collection_name="aeccar0_fs",
                            host="mongodb03.nersc.gov",
                            port=27017,
                            username="mp_rk_calculations_ro",
                            password="4df3t3t3554544",
                            last_updated_field = "last_updated",
                            key = "metadata.task_id")

aeccar2_store = GridFSStore(database="mp_rk_calculations",
                            collection_name="aeccar2_fs",
                            host="mongodb03.nersc.gov",
                            port=27017,
                            username="mp_rk_calculations_ro",
                            password="4df3t3t3554544",
                            last_updated_field = "last_updated",
                            key = "metadata.task_id")

# print('maggma_stores.py successfully loaded\nrun db.connect(), elfcar_store.connect(), chgcar_store.connect(), aeccar0_store.connect(), aeccar2_store.connect() to access NERSC database')

def connect_to_stores():
    try:
        db.connect()
        elfcar_store.connect()
        chgcar_store.connect()
        aeccar0_store.connect()
        aeccar2_store.connect()
        print('All connections successful')
    except:
        print('Error. Make sure you are connected to VPN')
        raise
    
print('All maggma stores (db, elfcar_store, chgcar_store, aeccar0_store, aeccar2_store) successfully loaded \nRun \'connect_to_stores()\' to connect to stores')