async def is_temporary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}