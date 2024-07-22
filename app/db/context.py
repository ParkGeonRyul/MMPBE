from pymongo import MongoClient
from config import Config


class Database:
    client = MongoClient(Config.MONGO_URI)
    db = client.get_default_database()
    
    @staticmethod
    def get_collection(name):
        return Database.db[name]

companyCollection = Database.db["companys"]
contractDataCollection = Database.db["contractData"]
contractCollection = Database.db["contract"]
maintenanceCollection = Database.db["maintenance"]
requestTaxCollection = Database.db["requestTax"]
roleCollection = Database.db["role"]
serviceDeviceCollection = Database.db["serviceDevice"]
taxCollection = Database.db["tax"]
usageCollection = Database.db["usage"]
userCollection = Database.db["users"]
workRequestCollection = Database.db["workRequest"]
authCollection = Database.db["auth"]