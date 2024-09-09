from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from pydantic.alias_generators import to_camel
from dotenv import load_dotenv

import json
import os

from utils.pymongo_object_id import PyObjectId
from utils.snake_by_camel import convert_keys_to_camel_case


def lookup_data(collection: str, key: str, value: str, field_nm: str):
    return {"collection": collection, "key": key, "value": value, "field_nm": field_nm}

def test(lookup_list: List[str]):
    test1 = []
    for item in lookup_list:      
        test123 = lookup_data(*item)
        test2 = {
                    "$lookup": {
                        "from": test123['collection'],
                        "let": { f"{test123['key']}Id": f"${test123['value']}_id" },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": [ {"$toString": "$_id"}, f"$${test123['key']}Id"]
                                    }
                                }
                            }
                        ],
                        "as": f"{test123['field_nm']}_field"
                    }
                }
        test1.append(test2)
    return test1

def get_lookup(collection: str, key: str, value: str, field_nm: str):
    return [
                {
                    "$lookup": {
                        "from": collection,
                        "let": { f"{key}Id": f"${value}_id" },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": [ {"$toString": "$_id"}, f"$${key}Id"]
                                    }
                                }
                            }
                        ],
                        "as": f"{field_nm}_field"
                    }
                },
                {
                    "$unwind": f"${field_nm}_field"
                }
            ]

def set_pipeline(match: dict, projection: dict, join_list: List[str], set_data: dict):
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


    return pipeline