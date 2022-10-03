# def checkyear(listyear, data):
#     for i in listyear:
#         if data.get(i) is None:
#             if i == "start_year":
#                 return False, ("You need to fill start year ")
#             elif i == "end_year":
#                 return False, ("You need to fill end year ")
#         elif len(str(data.get(i))) != 4:
#             return False, ("You need to fill 4 int ")
#     return True, "success"


# def nonecheck(listpro, data):
#     for i in listpro:
#         if data.get(i) is None:
#             if i == "name_th":
#                 return False, ("You need to fill program thai name ")
#             elif i == "name_en":
#                 return False, ("You need to fill program english name ")
#     return True, "success"
