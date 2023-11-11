#for try only

import pandas as pd
from sklearn import datasets

wine=datasets.load_wine()

import matplotlib.pyplot as plt
import seaborn as sns

df=pd.DataFrame(
    wine.data,
    columns=wine.feature_names    
)

sns.countplot(
    data=df
)
plt.title('Wine Data')
plt.show()
#just try to plot wine data from skycelearn dataset