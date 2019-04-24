from sklearn.metrics import classification_report
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
labelencoder_X = LabelEncoder()
sc_X = StandardScaler()
import pickle


def createData(bank):
	bank_client = bank.iloc[: , 0:7]
	bank_client['job']      = labelencoder_X.fit_transform(bank_client['job'])
	bank_client['marital']  = labelencoder_X.fit_transform(bank_client['marital'])
	bank_client['education']= labelencoder_X.fit_transform(bank_client['education'])
	bank_client['default']  = labelencoder_X.fit_transform(bank_client['default'])
	bank_client['housing']  = labelencoder_X.fit_transform(bank_client['housing'])
	bank_client['loan']     = labelencoder_X.fit_transform(bank_client['loan'])
	bank_client.loc[bank_client['age'] <= 32, 'age'] = 1
	bank_client.loc[(bank_client['age'] > 32) & (bank_client['age'] <= 47), 'age'] = 2
	bank_client.loc[(bank_client['age'] > 47) & (bank_client['age'] <= 70), 'age'] = 3
	bank_client.loc[(bank_client['age'] > 70) & (bank_client['age'] <= 98), 'age'] = 4
	bank_related = bank.iloc[: , 7:11]
	bank_related['contact']     = labelencoder_X.fit_transform(bank_related['contact'])
	bank_related['month']       = labelencoder_X.fit_transform(bank_related['month'])
	bank_related['day_of_week'] = labelencoder_X.fit_transform(bank_related['day_of_week'])
	bank_related.loc[bank_related['duration'] <= 102, 'duration'] = 1
	bank_related.loc[(bank_related['duration'] > 102) & (bank_related['duration'] <= 180)  , 'duration']    = 2
	bank_related.loc[(bank_related['duration'] > 180) & (bank_related['duration'] <= 319)  , 'duration']   = 3
	bank_related.loc[(bank_related['duration'] > 319) & (bank_related['duration'] <= 644.5), 'duration'] = 4
	bank_related.loc[bank_related['duration']  > 644.5, 'duration'] = 5
	bank_se = bank.loc[: , ['emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']]
	bank_o = bank.loc[: , ['campaign', 'pdays','previous', 'poutcome']]
	bank_o['poutcome'].replace(['nonexistent', 'failure', 'success'], [1,2,3], inplace  = True)
	bank_final= pd.concat([bank_client, bank_related, bank_se, bank_o], axis = 1)
	bank_final = bank_final[['age', 'job', 'marital', 'education', 'default', 'housing', 'loan',
                     'contact', 'month', 'day_of_week', 'duration', 'emp.var.rate', 'cons.price.idx',
                     'cons.conf.idx', 'euribor3m', 'nr.employed', 'campaign', 'pdays', 'previous', 'poutcome']]
	X_input = sc_X.fit_transform(bank_final)
	model = pickle.load(open('model.pkl','rb'))
	bank['y']=model.predict(X_input)
	bank['y'] = bank.y.map({1:'yes',0: 'no'})
	return bank
