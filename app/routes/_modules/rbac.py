from fastapi import HTTPException

async def get_permission(role: int, permission: int):
    if role >= permission:
        return True
    else:
        raise HTTPException (status_code=401, detail="401 Unauthentic")