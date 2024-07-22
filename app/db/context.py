from pymongo import MongoClient, ASCENDING
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

# authCollection.drop_index("expireAt_1")

ttl_seconds = 3600
authCollection.create_index(
    [("expireAt", ASCENDING)],
    expireAfterSeconds=ttl_seconds
)