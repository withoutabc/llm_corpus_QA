param_error = "param error"
interval_error = "interval error"

error_dict = {param_error: 20001,
              interval_error: 50000,
              }


def BaseResp(info: str):
    base_resp = {}
    base_resp["status"] = error_dict[param_error]
    base_resp["info"] = param_error
    return {"code"}
