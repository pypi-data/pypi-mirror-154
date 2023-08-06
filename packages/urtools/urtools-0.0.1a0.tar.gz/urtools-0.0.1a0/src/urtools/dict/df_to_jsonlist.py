import pandas as pd

from urtools.dict.filter_dict_nans import filter_dict_nans

def df_to_jsonlist(df: pd.DataFrame) -> list[dict]:
    return [filter_dict_nans(record) for record in df.to_dict(orient='records')]
