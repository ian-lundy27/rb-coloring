import pandas as pd
import math
from sympy import primerange

from check import check


def convert_setlist(setlist: str):
    setlist = setlist[1:-2].replace(" ","").replace("{","").split("},")
    for i in range(len(setlist)):
        setlist[i] = set([int(j) for j in setlist[i].split(",")])
    return setlist


def read(path: str = "rb.csv", delim: str = ";"):
    df = pd.read_csv(path, delimiter=delim)
    df["coloring"] = df["coloring"].transform(convert_setlist)
    return df


def two_p(df: pd.DataFrame):
    return pd.DataFrame([{
        "i": p,
        "p": df[df["i"] == p]["rb"].item(), # -2 corrects for missing i=0,1 rows
        "2p": df[df["i"] == 2 * p]["rb"].item()
    } for p in primerange(math.floor(df.iloc[-1, 0]/2) + 1)])


def _get(df: pd.DataFrame, i: int) -> pd.DataFrame:
    return df[df["i"] == i]


def get_rb(df: pd.DataFrame, i: int) -> int:
    return _get(df, i)["rb"].item()


def get_coloring(df: pd.DataFrame, i: int) -> list[set]:
    return _get(df, i)["coloring"].item()


def p_pow(df: pd.DataFrame):
    rows, last = [], df.iloc[-1,0]
    for p in primerange(math.sqrt(last) + 1):
        row = {"i": p, "p1": df[df["i"] == p]["rb"].item()}
        for i in range(2,math.floor(math.log(last,p)) + 1):
            row[f"p{i}"] = df[df["i"] == p ** i]["rb"].item()
        rows.append(row)
    return pd.DataFrame(rows, dtype=pd.Int64Dtype())


class Colorings:
    df: pd.DataFrame
    def __init__(self, df: pd.DataFrame = None, path: str = "rb.csv"):
        self.df = df if df else read(path)
    def two_p(self):
        return two_p(self.df)
    def p_pow(self):
        return p_pow(self.df)
    def get(self, i: int):
        return _get(self.df, i)
    def rb(self, i: int):
        return get_rb(self.df, i)
    def coloring(self, i: int):
        return get_coloring(self.df, i)



if __name__=="__main__":
    c = Colorings()
    print(c.two_p().to_string(index=False))
    print(c.p_pow().to_string(index=False, na_rep=""))