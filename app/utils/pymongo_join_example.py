# pipeline = [
#         {
#             '$match': {
#                 'example': 'example' # main collection 조건문
#             }
#         },
#         {
#             '$lookup': {
#                 'from': 'example', # join할 컬렉션
#                 'localField': 'example_fk', # forign key
#                 'foreignField': 'example_pk', # primary key
#                 'as': 'example_field' # data 넣을 필드
#             }
#         },
#         {
#             '$unwind': '$example_field' # data 넣을 필드를 개별 문서로 변환
#         },
#         {
#             '$set': {
#                 'example': '$example_field.example' # 원하는 조건으로 필드 변환 등
#                 }
#         },
#         {
#             '$project': { # 특정 필드만 가져오기 or 특정 필드만 없애기
#                 'example': 0,
#                 'example': 0
#             }
#         },
#         {
#             '$limit': 1 # 하나의 문서만 가져오기
#         }
#     ]

#     result = next(ex_collection.aggregate(pipeline)) # 파이프라인 실행