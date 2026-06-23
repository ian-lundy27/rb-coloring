import pandas as pd
import math
import inspect
from typing import Callable
from sympy import primerange


def convert_setlist(setlist: str):
    setlist = setlist[1:-2].replace(" ","").replace("{","").split("},")
    for i in range(len(setlist)):
        setlist[i] = set([int(j) for j in setlist[i].split(",")])
    return setlist


def read(path: str = "rb.csv", delim: str = ";"):
    df = pd.read_csv(path, delimiter=delim)
    df["coloring"] = df["coloring"].transform(convert_setlist)
    return df

def write(df: pd.DataFrame, path: str = "rb.csv", delim: str = ";"):
    df.to_csv(path, sep=delim, index=False)


def sort_colorings(df: pd.DataFrame, minimum: bool = False, size: bool = False, other: Callable = None):
    def _sort(l: list):
        if minimum: l.sort(key=min)
        if size: l.sort(key=len)
        if other: l.sort(key=other)
        return l
    df["coloring"] = df["coloring"].transform(_sort)
    return df


def _get(df: pd.DataFrame, i: int) -> pd.DataFrame:
    return df[df["i"] == i]


def get_rb(df: pd.DataFrame, i: int) -> int:
    return _get(df, i)["rb"].item()


def get_coloring(df: pd.DataFrame, i: int) -> list[set]:
    return _get(df, i)["coloring"].item()


def ppow(df: pd.DataFrame):
    rows, last = [], df.iloc[-1,0]
    for p in primerange(math.sqrt(last) + 1):
        row = {"i": p, "p1": df[df["i"] == p]["rb"].item()}
        for i in range(2,math.floor(math.log(last,p)) + 1):
            row[f"p{i}"] = df[df["i"] == p ** i]["rb"].item()
        rows.append(row)
    return pd.DataFrame(rows, dtype="Int64")


def twop(df: pd.DataFrame):
    return np(df, 2)


def np(df: pd.DataFrame, *n: int):
    rows, nums, last, rb = [], list(n), df.iloc[-1,0], lambda i: get_rb(df, i)
    nums.sort()
    for p in primerange(math.floor(df.iloc[-1, 0]/min(n)) + 1):
        row = {"i": p, "p": rb(p)} 
        for i in n:
            if i * p > last: break
            row[f"{i}p"] = rb(i * p)
        rows.append(row)
    return pd.DataFrame(rows, dtype="Int64")


def _recent(cls: type["Colorings"] | type["ColoringsK"]):
    def make_wrapper(func):
        def wrapper(self: "Colorings | ColoringsK", *args, **kwargs):
            result = func(self, *args, **kwargs)
            if type(result) is pd.DataFrame:
                self.recent = result
            return result
        return wrapper
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        setattr(cls, name, make_wrapper(func))
    return cls


@_recent
class Colorings:
    df: pd.DataFrame
    recent: pd.DataFrame | None = None

    def __init__(self, df: pd.DataFrame = None, path: str = "rb.csv"):
        self.df = df if df else read(path)
    def sort_colorings(self, minimum: bool = True, size: bool = True, other: Callable = None):
        self.df = sort_colorings(self.df, minimum=minimum, size=size, other=other)
        return self.df
    def write(self, path: str = "rb.csv", delimiter=";"):
        self.df.to_csv(path, sep=delimiter, index=False)
    def twop(self):
        return twop(self.df)
    def np(self, *n: int):
        return np(self.df, *n)
    def ppow(self):
        return ppow(self.df)
    def get(self, i: int):
        return _get(self.df, i)
    def rb(self, i: int):
        return get_rb(self.df, i)
    def coloring(self, i: int):
        return get_coloring(self.df, i)
    def print(self, **kwargs):
        i = kwargs.pop("index",False)
        print(None if self.recent is None else self.recent.to_string(index=i, **kwargs))

@_recent
class ColoringsK:
    df: pd.DataFrame
    recent: pd.DataFrame | None = None

    def __init__(self, df: pd.DataFrame = None, path: str = "rbk.csv"):
        self.df = df if df else read(path)
    def print(self, **kwargs):
        kwargs["float_format"] = lambda x: f"{int(x)}"
        kwargs["na_rep"] = ""
        Colorings.print(self, **kwargs)
    def get(self, p: int, k: int = 0):
        if not k: k == math.floor((p - 1) / 2)
        return self.df[(self.df["p"] == p) & (self.df["k"] == k)]
    def rb(self, p: int, k: int = 0):
        return self.get(p, k)["rb"].item()
    def coloring(self, p: int, k: int = 0):
        return self.get(p, k)["coloring"].item()
    def allpow(self, p: int):
        return self.df[self.df["p"] == p][["k", "rb"]]
    def bigpow(self, p: int):
        return self.df[(self.df["p"] == p) & 
                       ((self.df["k"] == 2) | 
                        (self.df["k"] == math.floor((p - 1) / 2)) |
                        (self.df["k"] == p - 1))][["k","rb"]]
    def allk(self, k: int):
        return self.df[(self.df["k"] == k)][["p","rb"]]
    def bigk(self):
        df = self.df[(self.df["k"] == 2) |
                       (self.df["k"] * 2 == self.df["p"] - 1) |
                       (self.df["k"] == self.df["p"] - 1)][["p", "k", "rb"]]
        df["i"] = df.groupby("p").cumcount()
        df = df.pivot(index="p", columns="i", values="rb").reset_index()
        df.columns = ["p", "2", "p-1/2", "p-1"]
        df.loc[df["p"] == 5, "p-1"] = 3 # Hardcode fix to issue w/ 5, since 2=p-1/2
        return df
        


if __name__=="__main__":
    # c = Colorings()
    # c.np(2,3,5,7,11,13,17,19,23)
    # c.ppow()
    # c.print()
    d = ColoringsK()
    d.bigk()
    d.print()