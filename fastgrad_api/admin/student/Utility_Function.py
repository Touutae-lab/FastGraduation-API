import re

# blueprint: Blueprint = Blueprint("Utility_Function", __name__)


def checklanguage(listlang, data):
    # msg=""
    if listlang[0] == "fname_en" or listlang[1] == "mname_en":
        regex = re.compile("^[a-zA-Z]+$", re.IGNORECASE)  # create regex object

        for i in listlang:

            if data.get(i) is not None:

                match_result = regex.findall(data.get(i))  # ค้นหาผลลัพท์
                if str(match_result[0] == data.get(i)):
                    continue

                else:
                    return False, (
                        "Vaild language : " + i + " = " + str(data.get(i))
                    )
            elif data.get(i) is None and i == "fname_en":
                return False, ("You need to fill firstname ")
            elif data.get(i) is None and i == "lname_en":
                return False, ("You need to fill lastname ")

        return True, "success"

    elif listlang[0] == "fname_th":
        regex = re.compile("^[ก-ฮ]+$", re.IGNORECASE)
        for i in listlang:

            if data.get(i) is not None:
                if str(match_result[0] == data.get(i)):
                    continue

                else:
                    return False, (
                        "Vaild language : " + i + " = " + str(data.get(i))
                    )
            elif data.get(i) is None and i == "fname_th":
                return False, ("คุณต้องใส่ชื่อจริง ")
            elif data.get(i) is None and i == "lname_th":
                return False, ("คุณต้องใส่นามกสุล ")
        return True, "success"
