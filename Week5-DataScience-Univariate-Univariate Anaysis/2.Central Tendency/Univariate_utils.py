import pandas as pd
import numpy as np

class Univariate:

    # Split quantitative and qualitative columns
    @staticmethod
    def quanQual(dataset):
        quan = []
        qual = []
        for columnName in dataset.columns:
            if dataset[columnName].dtype == 'O':
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan, qual

    # Frequency table
    @staticmethod
    def freqTable(columnName, dataset):
        freqTable = pd.DataFrame()
        freqTable["Unique_Values"] = dataset[columnName].value_counts().index
        freqTable["Frequency"] = dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"] = freqTable["Frequency"] / len(dataset)
        freqTable["Cumsum"] = freqTable["Relative_Frequency"].cumsum()
        return freqTable

    # Descriptive stats
    @staticmethod
    def descriptive_stats(dataset, quan):
            descriptive = pd.DataFrame(
                index=[
                    "Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%",
                    "IQR","1.5Rule","Lesser","Greater","Min","Max"
                ],
                columns=quan
            )
            for columnName in quan:
                descriptive[columnName]["Mean"]    = dataset[columnName].mean()
                descriptive[columnName]["Median"]  = dataset[columnName].median()
                descriptive[columnName]["Mode"]    = dataset[columnName].mode()[0]
                descriptive[columnName]["Q1:25%"]  = dataset.describe()[columnName]["25%"]
                descriptive[columnName]["Q2:50%"]  = dataset.describe()[columnName]["50%"]
                descriptive[columnName]["Q3:75%"]  = dataset.describe()[columnName]["75%"]
                descriptive[columnName]["99%"]     = np.nanpercentile(dataset[columnName],99)
                descriptive[columnName]["Q4:100%"] = dataset.describe()[columnName]["max"]
                descriptive[columnName]["IQR"]     = descriptive[columnName]["Q3:75%"] - descriptive[columnName]["Q1:25%"]
                descriptive[columnName]["1.5Rule"] = 1.5 * descriptive[columnName]["IQR"]
                descriptive[columnName]["Lesser"]  = descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5Rule"]
                descriptive[columnName]["Greater"] = descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5Rule"]
                descriptive[columnName]["Min"]     = dataset[columnName].min()
                descriptive[columnName]["Max"]     = dataset[columnName].max()
            return descriptive

    # Detect outliers
    @staticmethod
    def outliercolnames(descriptive, quan):
        lesser = []
        greater = []
        for columnName in quan:
            if descriptive[columnName]["Min"] < descriptive[columnName]["Lesser"]:
                lesser.append(columnName)
            if descriptive[columnName]["Max"] > descriptive[columnName]["Greater"]:
                greater.append(columnName)
        return lesser, greater

    # Cap outliers
    @staticmethod
    def cap_outliers(dataset, descriptive, lesser, greater):
        for columnName in lesser:
            dataset.loc[dataset[columnName] < descriptive[columnName]["Lesser"], columnName] = descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset.loc[dataset[columnName] > descriptive[columnName]["Greater"], columnName] = descriptive[columnName]["Greater"]
        return dataset