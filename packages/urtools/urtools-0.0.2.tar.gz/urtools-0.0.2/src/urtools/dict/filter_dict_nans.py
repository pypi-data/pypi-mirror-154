def filter_dict_nans(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and v == v and str(v).lower() != 'nan'}

