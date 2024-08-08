import pandas as pd
from pathlib import Path
BASE_PATH = Path("<INSERT YOUR PATH HERE>")
samusik_all = pd.read_csv(BASE_PATH / "samusik_all.csv")

# source of the marker columns is https://rdrr.io/github/lmweber/HDCytoData/src/inst/scripts/make-data-Samusik.R
samusik_markers = samusik_all.iloc[:, range(8, 47)]
samusik_eosinophils_markers = samusik_markers.loc[samusik_all["label"] == 8, :]


batch_size = 5_000
for nr, i in enumerate(range(0, samusik_eosinophils_markers.shape[0], batch_size)):
    samusik_eosinophils_markers.iloc[i:i + batch_size, :].to_csv(BASE_PATH / f"/eosinophils_{nr+1}/data.csv", index=False)