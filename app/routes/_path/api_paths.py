# api_paths.py

ROOT = "/proxy/"
SEPARATE = "/"
V1 = ROOT + "v1"

# Auth paths
AUTH = V1 + SEPARATE + "auth"
LOGIN_WITH_MS = AUTH + SEPARATE + "login"
AUTH_CALLBACK = AUTH + SEPARATE + "oauth" + SEPARATE + "callback"
LOGOUT = AUTH + SEPARATE + "logout"
CHECK_SESSION = AUTH + SEPARATE + "validate"
USER_INFO = AUTH + SEPARATE + "userinfo"
# USER_PROFILE =

# User paths
USER = V1 + SEPARATE + "user"
READ_USER = USER + SEPARATE + "readuser"
CREATE_USER = USER + SEPARATE + "createuser"
UPDATE_USER = USER + SEPARATE + "updateuser"
DELETE_USER = USER + SEPARATE + "deleteuser"

# Request paths
REQUEST = V1 + SEPARATE + "request"
READ_REQUEST = REQUEST + SEPARATE + "readrequest"
READ_REQUEST_TEMPORARY = REQUEST + SEPARATE + "temprary"
READ_REQUEST_DETAIL = REQUEST + SEPARATE + "readrequest" + SEPARATE + "detail"
CREATE_REQUEST = REQUEST + SEPARATE + "createrequest"
CREATE_REQUEST_TEMPORARY = REQUEST + SEPARATE + "createrequest" + SEPARATE + "temporary"
UPDATE_REQUEST = REQUEST + SEPARATE + "updaterequest"
UPDATE_REQUEST_TEMPORARY = REQUEST + SEPARATE + "updaterequest" + SEPARATE + "temporary"
DELETE_REQUEST = REQUEST + SEPARATE + "deleterequest"
DELETE_REQUEST_TEMPORARY = REQUEST + SEPARATE + "deleterequest" + SEPARATE + "temporary"

# Contract paths
CONTRACT = V1 + SEPARATE + "contract"
READ_CONTRACT = CONTRACT + SEPARATE + "readcontract"
CREATE_CONTRACT = CONTRACT + SEPARATE + "createcontract"
UPDATE_CONTRACT = CONTRACT + SEPARATE + "updatecontract"
DELETE_CONTRACT = CONTRACT + SEPARATE + "deletecontract"

# Tax paths
TAX = V1 + SEPARATE + "tax"
READ_TAX = TAX + SEPARATE + "readtax"
CREATE_TAX = TAX + SEPARATE + "createtax"
UPDATE_TAX = TAX + SEPARATE + "updatetax"
DELETE_TAX = TAX + SEPARATE + "deletetax"
