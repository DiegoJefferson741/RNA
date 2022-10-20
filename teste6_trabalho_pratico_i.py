# -*- coding: utf-8 -*-
"""Teste6 - Trabalho Pratico I.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19dvIXralgl9f8e4oQCiSh9vi2cDi4i--
"""

#import libraries 
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/test.csv?raw=true'
test = pd.read_csv(url)
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/train.csv?raw=true'
train = pd.read_csv(url)

display(train) # Exibe o Dataframe
#print(train.info()) # Exibe Informações do Dataframe

### Descobrir se tem valores vazios e a quantidade deles em cada coluna

#print(train.isna().any()) # Exibe como True ou False os valores do Dataframe
print(train.isna().sum()) # Exibe a soma dos valores no Dataframe

############## Tratando variaveis categoricas  ##############

#OneHotEncoding

!pip install category_encoders

import category_encoders as ce
from category_encoders.one_hot import OneHotEncoder, OrdinalEncoder

train.head()
#train.info(verbose=True)

#### Criado um Dataframe com as colunas que seram usadas   
####  Deletendo as colunas  "PassengerId","Name","Transported"  pois nao seram uteis

#dfTrain = train["HomePlanet","CryoSleep", "Cabin","Destination","Age","VIP","RoomService","FoodCourt","ShoppingMall","Spa","VRDeck","Transported"]
dfTrain = train.drop(["PassengerId","Name"], axis = 1)

dfTrain.head()
#train.info(verbose=True)

#dfTrain['Transported'] = dfTrain['Transported'].map({False:0,True:1})# target variable
#dfTrain.Transported = dfTrain.Transported({"False": 0, "True" : 1})


dfTrain.replace({False: 0, True: 1}, inplace=True)

dfTrain.head()

OderEnc = OrdinalEncoder(cols =['HomePlanet','CryoSleep','Cabin','Destination','Age','VIP','RoomService','FoodCourt','ShoppingMall','Spa','VRDeck'])  # A variavel OrderEnc recebe os dados convertidos de Destination // Converte a coluna Destination

# Faz a junção da coluna convertida com as demais do Dataframe //mas descarta a conversao anterior

OE = OderEnc.fit_transform(dfTrain)

##### Verificando os valores e colunas #####

#print(OE.isna().any()) # Exibe como True ou False os valores nan do Dataframe
#print(OE.isna().sum()) # Exibe a soma dos valores nan no Dataframe
OE.head()
#OE.info(verbose=True)
#print(OE.info())
#OE.shape
#OE.isna().sum()
#OE.isnull().sum()

X = OE.drop(["Transported",] , axis = 1)
Y = OE["Transported"]

X.shape

########## Treinando a Rede ##########

#https://keras.io/api/  (Keras Documentation)

import tensorflow as tf 
import keras 
from keras.models import Sequential      #Sequencia entre as camadas: Entrada - Oculta - Saida
from keras.layers import Dense, Dropout  #Iremos utilizar camadas densa na rede neural (full-connection)

#criar a rede neural sequencial 
ann = Sequential()

#definir as camadas de entrada, oculta 
ann.add( Dense(units = 6, activation = 'relu', kernel_initializer = 'random_uniform', input_dim=11))  #primeira camada oculta (nr_neuronios_entradas + nr_neuronios_saida / 2) = (30+1 / 2 = 16);  
                                                                                                       #input_dim = 30  (número de neuronios da camada de entrada = features de X_train)
#definir a camada de saida
ann.add(Dense(units = 1, activation = 'sigmoid'))

#configurar parâmetros da rede 
ann.compile(optimizer = 'adam',             #optimizer -> calculo dos ajustes dos pesos (descida do gradiente), calculo do delta
            loss='binary_crossentropy',     #loss -> calculo ou tratamento do erro      (binary_crossentropy -> para problemas de classificação binária)
            metrics = ['binary_accuracy']   #metrics -> avaliar a metrica do modelo ->   accuracy para problema de classificação binária 
           )

#treinar a rede neural
ann.fit(X, Y, batch_size = 10, epochs = 50)

result = ann.evaluate(X, Y)

Ypred = ann.predict(X)  #calcula o valor do veículo 
Ypred

resultado = pd.DataFrame()

YpredBin = np.where(Ypred > 0.5, 1, 0)

resultado["Y"] = Y
resultado["Ypred"] = Ypred          #valores preditos para o conjunto de treinamento 
resultado["YpredBin"] = YpredBin
resultado.reset_index(inplace = True, drop=True)
resultado

