class Univariate():
     def  quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)   
            if(dataset[columnName].dtype=='O'):
                #print("Qual")
                qual.append(columnName)
            else:
                #print("Quan")
                quan.append(columnName)
        return quan,qual