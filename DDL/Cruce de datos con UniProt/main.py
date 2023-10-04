import requests
import pandas as pd
import time
import numpy as np

head = ["id",
        "annotId",
        "createDate",
        "updateDate",
        "geneName",
        "geneDesc",
        "species",
        "taxID",
        "domains",
        "flag",
        "flagNote",
        "aliases",
        "GSTpaper",
        "PDBIDs",
        "UniProtIDs"
        ]

df_rbp = pd.read_csv('datos/Proteinas.csv', header=None, names=head)

print(df_rbp.info())

df_largos = pd.DataFrame()

df_largos["UniProtID"] = df_rbp["UniProtIDs"]
df_largos.replace('\\N', np.nan, inplace=True)
df_largos = df_largos.dropna(subset=["UniProtID"])


N = len(df_largos["UniProtID"])
cont = 0

salida = open("datos/salida.csv", "w")

salida.write("UniProtID,Largo,Secuencia\n")

for _, row in df_largos.iterrows():
    pbid = row["UniProtID"].split(sep=";")[0]

    url = f"https://rest.uniprot.org/uniprotkb/{pbid}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200 and "sequence" in response.json():
            largo = response.json()["sequence"]["length"]
            sec = response.json()["sequence"]["value"]
    else:
        largo = np.nan
        sec = np.nan

    cont += 1

    print(f"{round(cont/N*100, 2)}% | UniProtID = {pbid} ; Largo = {largo}")

    salida.write(f"{pbid},{largo},{sec}\n")

    time.sleep(1)

# TODO: cruzar con informacion de estructuras
    


