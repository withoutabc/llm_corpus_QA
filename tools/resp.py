from tools.error import *

def base_resp(info: str):
    base_resp = {}
    base_resp["status"] = error_dict[info]
    base_resp["info"] = info
    base_resp["data"] = {}
    return base_resp