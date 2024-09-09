from typing import List


def lookup_data(collection: str, key: str, value: str, field_nm: str):
    return {"collection": collection, "key": key, "value": value, "field_nm": field_nm}

def set_pipeline(match: dict, projection: dict, join_list: List[str], set_data: dict, skip: int | None, limit: int | None):
    pipeline = []
    for item in join_list:      
        get_data = lookup_data(*item)
        lookup = [
            {
                    "$lookup": {
                        "from": get_data['collection'],
                        "let": { f"{get_data['key']}Id": f"${get_data['value']}_id" },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": [ {"$toString": "$_id"}, f"$${get_data['key']}Id"]
                                    }
                                }
                            }
                        ],
                        "as": f"{get_data['field_nm']}_field"
                    }
            },
            {
                "$unwind": f"${get_data['field_nm']}_field"
            }
            ]
        for item in lookup:
            pipeline.append(item)

    pipeline.append({"$set": set_data})
    pipeline.append({"$match": match})
    pipeline.append({"$project": projection})
    if skip and limit:
        pipeline.append({"$skip": skip}),
        pipeline.append({"$limit": limit})


    return pipeline