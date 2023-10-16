import pandas as pd

df = pd.read_csv("shipdata.csv",delimiter=";")
df = df.groupby(['imo'])[["mainEngineConsumption","DistanceOverGround","Speed"]].sum()
print(df)