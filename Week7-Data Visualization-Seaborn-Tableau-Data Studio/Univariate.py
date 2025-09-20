import pandas as pd
import numpy as np

class Univariate:
    
    @staticmethod
    def quanQual(dataset):
        quan, qual = [], []
        for columnName in dataset.columns:
            if dataset[columnName].dtype == 'O':
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan, qual

    @staticmethod
    def freqTable(columnName, dataset):
        total_count = dataset[columnName].count()
        freqTable = pd.DataFrame()
        freqTable["Unique_Values"] = dataset[columnName].value_counts().index
        freqTable["Frequency"] = dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"] = freqTable["Frequency"] / total_count
        freqTable["CumSum"] = freqTable["Relative_Frequency"].cumsum()
        return freqTable

    @staticmethod
    def descriptive_stats(dataset, quan):
        descriptive = pd.DataFrame(
            index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%",
                   "99%","Q4:100%","IQR","1.5Rule","Lesser","Greater","Min","Max"],
            columns=quan
        )
        for columnName in quan:
            descriptive[columnName]["Mean"]   = dataset[columnName].mean()
            descriptive[columnName]["Median"] = dataset[columnName].median()
            descriptive[columnName]["Mode"]   = dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"] = dataset[columnName].quantile(0.25)
            descriptive[columnName]["Q2:50%"] = dataset[columnName].quantile(0.50)
            descriptive[columnName]["Q3:75%"] = dataset[columnName].quantile(0.75)
            descriptive[columnName]["99%"]    = np.nanpercentile(dataset[columnName], 99)
            descriptive[columnName]["Q4:100%"]= dataset[columnName].max()
            descriptive[columnName]["IQR"]    = descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5Rule"]= 1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"] = descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5Rule"]
            descriptive[columnName]["Greater"]= descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5Rule"]
            descriptive[columnName]["Min"]    = dataset[columnName].min()
            descriptive[columnName]["Max"]    = dataset[columnName].max()
        return descriptive

    @staticmethod
    def detect_outliers(descriptive, quan):
        lesser, greater = [], []
        for columnName in quan:
            if descriptive[columnName]["Min"] < descriptive[columnName]["Lesser"]:
                lesser.append(columnName)
            if descriptive[columnName]["Max"] > descriptive[columnName]["Greater"]:
                greater.append(columnName)
        return lesser, greater

    @staticmethod
    def cap_outliers(dataset, descriptive, lesser, greater):
        for columnName in lesser:
            dataset.loc[dataset[columnName] < descriptive[columnName]["Lesser"], columnName] = descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset.loc[dataset[columnName] > descriptive[columnName]["Greater"], columnName] = descriptive[columnName]["Greater"]
        return dataset