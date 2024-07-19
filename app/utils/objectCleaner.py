def cleanObject(data: object):
    cleanData = {key: value for key, value in data.items() if value is not None}
    return cleanData