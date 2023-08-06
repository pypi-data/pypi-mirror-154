from plexflo.datastream.stream import stream
import pandas as pd

df = pd.read_csv("C:\\Users\\Pranav\\Desktop\\plexflo_conda\\test.csv")


stream(df, "127.0.0.1", 5999, 1)