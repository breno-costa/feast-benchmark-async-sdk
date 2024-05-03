import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
from pathlib import Path

def generate_data(num_rows: int, num_features: int, key_space: int) -> pd.DataFrame:
    features = [f"feature_{i}" for i in range(num_features)]
    columns = ["entity", "event_timestamp"] + features
    df = pd.DataFrame(0, index=np.arange(num_rows), columns=columns)
    df["event_timestamp"] = datetime.datetime.utcnow()
    df["entity"] = df.index
    for column in features:
        df[column] = np.random.randint(1, key_space, num_rows)
    return df

if __name__ == "__main__":
    df = generate_data(10000, 250, 10000)
    df.to_parquet(Path(__file__).parent / "generated_data.parquet")
