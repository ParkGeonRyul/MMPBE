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

# Category paths
CATEGORY = V1 + SEPARATE + "category"


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
UPDATE_REQUEST_STATUS = REQUEST + SEPARATE + "updatestatus"

# Plan paths
PLAN = V1 + SEPARATE + "plan"
SELECT_PLAN = PLAN + SEPARATE + "selectListPlan"
SELECT_PLAN_TEMPORARY = PLAN + SEPARATE + "temprary"
SELECT_PLAN_DETAIL = PLAN + SEPARATE + "selectPlan" + SEPARATE + "detail"
SELECT_APPROVE_WR_LIST = PLAN + SEPARATE + "selectApproveWrList"
CREATE_PLAN = PLAN + SEPARATE + "createPlan"
CREATE_PLAN_TEMPORARY = PLAN + SEPARATE + "createPlan" + SEPARATE + "temporary"
UPDATE_PLAN = PLAN + SEPARATE + "updatePlan"
UPDATE_PLAN_STATUS = PLAN + SEPARATE + "updatePlanStatus"
UPDATE_PLAN_STATUS_ACCEPT = PLAN + SEPARATE + "updatePlanStatusAccept"
UPDATE_PLAN_TEMPORARY = PLAN + SEPARATE + "updatePlan" + SEPARATE + "temporary"
DELETE_PLAN = PLAN + SEPARATE + "deletePlan"
DELETE_PLAN_TEMPORARY = PLAN + SEPARATE + "deletePlan" + SEPARATE + "temporary"

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
