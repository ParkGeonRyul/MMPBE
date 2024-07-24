# api_paths.py

ROOT = "/"
SEPARATE = "/"
V1 = ROOT + "v1"

# Auth paths
AUTH = V1 + SEPARATE + "AUTH"
LOGIN_WITH_MS = AUTH + SEPARATE + "login"
AUTH_CALLBACK = AUTH + "auth" + SEPARATE + "callback"
LOGOUT = AUTH + "logout"
CHECK_SESSION = AUTH + "validate"

# User paths
USER = V1 + "USER"
READ_USER = USER + SEPARATE + "readUser"
CREATE_USER = USER + SEPARATE + "createUser"
UPDATE_USER = USER + SEPARATE + "updateUser"
DELETE_USER = USER + SEPARATE + "deleteUser"

# Request paths
REQUEST = V1 + "REQUEST"
READ_REQUEST = REQUEST + SEPARATE + "readRequest"
CREATE_REQUEST = REQUEST + SEPARATE + "createRequest"
UPDATE_REQUEST = REQUEST + SEPARATE + "updateRequest"
DELETE_REQUEST = REQUEST + SEPARATE + "deleteRequest"

# Contract paths
CONTRACT = V1 + "CONTRACT"
READ_CONTRACT = CONTRACT + SEPARATE + "readContract"
CREATE_CONTRACT = CONTRACT + SEPARATE + "createContract"
UPDATE_CONTRACT = CONTRACT + SEPARATE + "updateContract"
DELETE_CONTRACT = CONTRACT + SEPARATE + "deleteContract"

# Tax paths
TAX = V1 + "TAX"
READ_TAX = TAX + SEPARATE + "readTax"
CREATE_TAX = TAX + SEPARATE + "createTax"
UPDATE_TAX = TAX + SEPARATE + "updateTax"
DELETE_TAX = TAX + SEPARATE + "deleteTax"
