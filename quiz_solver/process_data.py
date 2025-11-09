import pandas as pd
import json

def process_data(df: pd.DataFrame, raw_content: str):
    try:
        if df is not None:
            if "value" in df.columns:
                return int(df["value"].sum())
            else:
                return df.to_dict(orient="records")
        else:
            try:
                data = json.loads(raw_content)
                if isinstance(data, dict) and "value" in data:
                    return data["value"]
            except:
                pass
        return raw_content
    except Exception as e:
        print("Error in process_data:", e)
        return raw_content
