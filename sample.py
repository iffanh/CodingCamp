import pandas as pd
from sklearn import datasets
from sklearn.discriminant_analysis import StandardScaler

iris=datasets.load_iris()

target_names={
    0:'sentosa',
    1:'versicolor',
    2:'virginica'
}

df=pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

df['target']=iris.target
df['target_names']=df['target'].map(target_names)

import matplotlib.pyplot as plt
import seaborn as sns

sns.countplot(
    x='target_names',   
    data=df)
plt.title('Iris Target Value Count')
#plt.show()

#load features and target separately
x=iris.data
y=iris.target
#print(x)
#print(y)

#DataPreprocessing and scale using standardscaler
x_scaled=StandardScaler().fit_transform(x)
df2=pd.DataFrame(x_scaled,columns=['1','2','3','4'])
#print(x)

#Dimention reduction using PCA

from sklearn.decomposition import PCA
pca = PCA(n_components=3)
pca_features = pca.fit_transform(x_scaled)

print('Shape before PCA:',x_scaled.shape)
print('Shape after PCA:',pca_features.shape)

pca_df=pd.DataFrame(
    data=pca_features,
    columns=['PCA1','PCA2','PCA3']
)
print(pca_df)








