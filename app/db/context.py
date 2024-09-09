from pymongo import MongoClient, ASCENDING
from config import Config


class Database:
    client = MongoClient(Config.MONGO_URI)
    db = client.get_default_database()
    
    @staticmethod
    def get_collection(name):
        return Database.db[name]

company_collection = Database.db["companys"]
contract_data_collection = Database.db["contractData"]
contract_collection = Database.db["contract"]
maintenance_collection = Database.db["maintenance"]
request_tax_collection = Database.db["requestTax"]
role_collection = Database.db["role"]
service_device_collection = Database.db["serviceDevice"]
tax_collection = Database.db["tax"]
usage_collection = Database.db["usage"]
user_collection = Database.db["users"]
work_request_collection = Database.db["workRequest"]
work_plan_collection = Database.db["workPlan"]
auth_collection = Database.db["auth"]
login_log_collection = Database.db["loginLog"]
work_log_collection = Database.db["workLog"]
file_collection = Database.db["files"]

# authCollection.drop_index("expireAt_1")

# ttl_seconds = 3600
# authCollection.create_index(
#     [("expireAt", ASCENDING)],
#     expireAfterSeconds=ttl_seconds
# )ss
