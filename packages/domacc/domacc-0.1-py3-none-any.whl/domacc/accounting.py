import json
import re

import pandas as pd

from domacc.accountingData import AccountingData


class Accounting:
    def __init__(self, accountingData, categories):
        self.accountingData = accountingData
        self.categories = categories

    def getAccounting(self, initialDate=None, finalDate=None):
        movements = self.getMovements(initialDate, finalDate)
        movements = self.addBalance(movements)
        return self.addCategories(movements)

    @classmethod
    def LoadFromJsonFile(cls, configFile):
        with open(configFile) as jsonFile:
            jsonData = json.load(jsonFile)
            accountingData = cls._getAccountingData(jsonData)
            categories = jsonData.get("categories", {})
        return cls(accountingData, categories)

    @classmethod
    def _getAccountingData(cls, jsonData):
        accountingData = []
        customReaders = jsonData.get("customReaders")
        for accDataDict in jsonData["data"]:
            accountingData.append(
                AccountingData.LoadFromJsonObject(accDataDict, customReaders)
            )
        return accountingData

    def getMovements(self, initialDate, finalDate):
        dfs = []
        for accData in self.accountingData:
            dfs.append(accData.getMovements())

        df = pd.concat(dfs, ignore_index=True)
        df = df.sort_values(by="Date")
        if initialDate:
            mask = df["Date"] >= initialDate
            df = df.loc[mask]
        if finalDate:
            mask = df["Date"] <= finalDate
            df = df.loc[mask]
        df.index = range(len(df))
        return df

    def addBalance(self, movements):
        movements["Balance"] = 0
        for index, _ in movements.iterrows():
            previousBalance = movements.loc[index - 1, "Balance"] if index else 0
            income = movements.loc[index, "Income"]
            outcome = movements.loc[index, "Outcome"]
            movements.loc[index, "Balance"] = previousBalance + income - outcome
        return movements

    def addCategories(self, movements):
        movements["Tags"] = ""
        for index, row in movements.iterrows():
            newTags = []
            for category in self.categories:
                if re.search(category["regex"], row["Concept"]):
                    newTags.extend(category["tags"])
            movements.at[index, "Tags"] = ",".join(set(newTags))
        return movements
