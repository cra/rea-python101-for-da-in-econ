# coding: utf-8

import csv
import os

ALLOWED_IRIS_TYPES = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

# TODO: import functools, использовать wraps чтобы сохранить help

def protect_iris(func):
    def inner_f(*args, **kw):
        try:
            return func(*args, **kw)
        except KeyError:
            print("Знать что-то про такой Iris запрещено")
    return inner_f

class IrisReader:
    def __init__(self, fpath, ignore_type="Iris-virginica"):
        self.fpath = fpath
        self.ignore_type = ignore_type
        self.stats = {}

        self.read_stats_from_csv()

    def read_stats_from_csv(self):
        with open(self.fpath) as f:
            n = 0
            for row in csv.reader(f):
                n += 1
                if n == 1: # skip header
                    continue

                s_len, s_width, p_len, p_width, name = row
                if name == self.ignore_type:
                    continue

                name = name.strip()
                if name in self.stats:
                    self.stats[name]["sepalLength"].append(float(s_len))
                    self.stats[name]["sepalWidth"].append(float(s_width))
                    self.stats[name]["petalLength"].append(float(p_len))
                    self.stats[name]["petalWidth"].append(float(p_width))
                else:
                    self.stats[name] = {
                        "sepalLength": [],
                        "sepalWidth": [],
                        "petalLength": [],
                        "petalWidth": [],
                    }

    @property
    def iris_types(self):
        return self.stats.keys()

    @protect_iris
    def give_min(self, iris_type, feature=None):
        if feature is not None:
            return min(self.stats[iris_type][feature])

        return [min(f) for f in self.stats[iris_type].values()]

    @protect_iris
    def give_max(self, iris_type, feature=None):
        if feature is not None:
            return max(self.stats[iris_type][feature])

        return [
            self.give_max(iris_type, f) for f in self.stats[iris_type].keys()
        ]

    @protect_iris
    def give_avg(self, iris_type, feature=None):
        if feature is not None:
            values = self.stats[iris_type][feature]
            return sum(values) / len(values)
        return [
            self.give_avg(iris_type, f) for f in self.stats[iris_type].keys()
        ]

    @protect_iris
    def give_sma(self, iris_type, feature):
        """ blablabla """
        l = 3
        smooth = []
        values = self.stats[iris_type][feature]
        for j in range(l - 1, len(values)):
            i, tmp = 0, 0
            while i < l:
                tmp += values[j - i]/l
                i += 1
            smooth.append(tmp)
        return smooth


if __name__ == "__main__":
    r = IrisReader(os.path.join("..", "datasets", "iris.csv"), ignore_type='')
    print("Привет")
    print(r.give_avg("Iris-virginica"))
