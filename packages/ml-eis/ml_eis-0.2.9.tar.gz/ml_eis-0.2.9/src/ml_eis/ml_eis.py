#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 21:51:22 2022

@author: yuefanji
"""
import os
import math
import numpy as np
from numpy import loadtxt
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from .electrochem import *

import sklearn         
from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_percentage_error
# Note - you will need version 0.24.1 of scikit-learn to load this library (SequentialFeatureSelector)
from sklearn.feature_selection import f_regression, SequentialFeatureSelector
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPRegressor

# Import Scikit-Learn library for decision tree models
import sklearn         
from sklearn import linear_model, datasets
from sklearn.utils import resample
from sklearn import tree

from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import BaggingRegressor,RandomForestRegressor,GradientBoostingRegressor

from sklearn.model_selection import train_test_split

import joblib
from scipy import interpolate,optimize

data_path = os.path.join(os.path.dirname(__file__),'data')



def ml_features(eis_data,cycling_data):
    EIS=impedance_data_processing(eis_data)
    BT=pd.read_csv(cycling_data)
    Max_cycle=10
    ret=[]
    ret=cap_ret(BT,Max_cycle)
    V_fit=np.linspace(2.5,4.2, num=1000)
    Max_cycle=10
    Q_fit=np.zeros((1000,10))
    dQ=np.zeros((1000,9))
    
    for j in range(1,Max_cycle+1):
        C=pd.DataFrame()
        C=cycling_data_processing(BT,j,'discharge')
        C1=C.copy()
        V=C1['Voltage(V)'].to_numpy()
        dC=C1['Capacity(Ah)'].to_numpy()
        f = interpolate.interp1d(V, dC,kind='linear', fill_value=0,bounds_error=False)
        Q_fit[:,j-1]=f(V_fit)
        if j==1:
            continue
        dQ[:,j-2]=f(V_fit)-Q_fit[:,0]
        var=np.zeros(Max_cycle-1)
        for j in range(1,Max_cycle):
            var[j-1]=dQ[:,j-1].var(ddof=1)
        
        
    feq=EIS['frequency'].dropna()
    Z1=EIS['Z1'].dropna()
    Z2=EIS['Z2'].dropna()
    low_f=min(feq)
    high_f=max(feq)
    Zt=Z1+1j*Z2

    f = interpolate.interp1d(feq, Zt,kind='linear')
    f1 = interpolate.interp1d(Zt, feq,kind='linear')
    Z1_min=Z1.min()
    Z1_max=Z1.max()
    f_max = interpolate.interp1d(Z1, Z2,kind='linear')


    xmax_local = optimize.fminbound(f_max, Z1_min, Z1_max)
    f_min = interpolate.interp1d(Z1, -Z2,kind='linear')
    xmin_local = optimize.fminbound(f_min, Z1_min, Z1_max)
    Z1max=xmax_local
    Z2max=f_max(xmax_local)
    Z1min=xmin_local
    Z2min=-f_min(xmin_local)
    freq_fit_min=f1(Z1min+1j*Z2min).real
    freq_fit_max=f1(Z1max+1j*Z2max).real
    Z1_high_f=Z1[0]
    Z2_high_f=Z2[0]
    data=np.hstack((var[:],freq_fit_max,Z1max,Z2max,Z1_high_f,Z2_high_f))
    data=np.transpose(data)
    return(data.reshape(1,-1))

def average_error(y_test, y_pred):
    y_diff = np.subtract(y_test, y_pred)
    y_diff_abs = np.abs(y_diff)
    average_error = np.sum(y_diff_abs)/y_diff_abs.size
    return (round(average_error,2))
def average_err_per_cyc(y_test,y_pred):
    n=len(y_pred[0])
    error=np.zeros(n)
    for i in range(0,n):
        error[i]=average_error(y_test[:,i],y_pred[:,i])
    return(error)

        



def rdf_online(eis_data,cycling_data,n_estimators, max_features, max_depth,test_size,cyc_num):
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')
    X_features=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X=np.transpose(X_features)
    y=np.transpose(ret)
    y=y[1:45]
    model = RandomForestRegressor(n_estimators= n_estimators, max_features = max_features, max_depth=max_depth,random_state=42,n_jobs=-1)
      
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size= test_size, random_state=42)
    model.fit(X_dev, y_dev)
    
    r2=r2_score(np.transpose(y_test), np.transpose(model.predict(X_test)))
    features= ml_features(eis_data,cycling_data)
    cap_ret=model.predict(features)
    err=average_err_per_cyc(y_test,model.predict(X_test))



    return (round(cap_ret[0][cyc_num-1],2),round(err[cyc_num-1],2))


def battery_clf(eis_data,cycling_data):
    Grade = {'98': 'AA', '97': 'A', '96': 'B+','95': 'B','94': 'C+','93': 'C'}
    X_features= ml_features(eis_data,cycling_data)
    rdf = joblib.load(os.path.join(data_path,'rdf.sav'))
    nn  = joblib.load(os.path.join(data_path,'MLP_NN_Optimized.sav'))
    gdb = joblib.load(os.path.join(data_path,'gradient_boosting.sav'))
    rdf_pred=rdf.predict(X_features)
    nn_pred=nn.predict(X_features)
    gdb_pred=gdb.predict(X_features)
    gb_err=0.47
    rdf_err=0.44
    nn_err=0.77
    average_error= np.mean([gb_err,rdf_err,nn_err])
    average_error=round(average_error,2)
    result = np.mean([rdf_pred[0][299],nn_pred[0][299],gdb_pred[0]])
    if (result-average_error)<90:
        return('Bad Cell',round(result,2),average_error)
    if (result-average_error)>=96:
        return('Top Graded Cell',round(result,2),average_error)
    if 94<=(result-average_error)<96:
        return('A',round(result,2),average_error)
    if 92<=(result-average_error)<94:
        return('B',round(result,2),average_error)
    if 90<=(result-average_error)<92:
        return('C',round(result,2),average_error)




def gbr_online(eis_data,cycling_data,n_estimators, max_depth, learning_rate,test_size,cyc_num):
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')

    X_features=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X=np.transpose(X_features)
    y=np.transpose(ret)
    y=y[1:45,cyc_num-1]
    
    model = GradientBoostingRegressor(n_estimators= n_estimators, 
                                      max_depth = max_depth, 
                                      learning_rate = learning_rate, random_state=42)
    
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size= test_size, random_state=42)
    model.fit(X_dev, y_dev)
    
    features= ml_features(eis_data,cycling_data)
    cap_ret=model.predict(features)
    r2=r2_score(np.transpose(y_test), np.transpose(model.predict(X_test)))
    
    err=average_error(y_test,model.predict(X_test))


    return (round(cap_ret[0],2),round(r2,2),round(err,2))

    
def RMSE_per_cycle(y_pred, y_act):
    '''Returns the MSE for each different output (cycle) between predicted sets and actual sets
    
    Parameters
    ----------
    y_pred : 2d array of samples and predicted y
    
    y_act: 2d array of samples and actual y
    

    Returns
    -------
    1d list of MSEs for each cycle number
    
    Values are in percentage
    '''
    
    RMSE_per_cycle = []
    
    for i in range(0,len(y_act.transpose())):
 
        RMSE_per_cycle.append(np.root(mean_squared_error(y_act.transpose()[i],y_pred.transpose()[i])))
    return RMSE_per_cycle


def rdf_online_plot(eis_data,cycling_data,n_estimators, max_features, max_depth,test_size,cyc_num):
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')
    X_features=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X=np.transpose(X_features)
    y=np.transpose(ret)
    y=y[1:45]
    model = RandomForestRegressor(n_estimators= n_estimators, max_features = max_features, max_depth=max_depth,random_state=42,n_jobs=-1)
      
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size= test_size, random_state=42)
    model.fit(X_dev, y_dev)
    
    r2=r2_score(np.transpose(y_test), np.transpose(model.predict(X_test)))
    features= ml_features(eis_data,cycling_data)
    
    
    cap_ret=model.predict(features)
    err=average_err_per_cyc(y_test,model.predict(X_test))
    fig, ax = plt.subplots(figsize=(8,6))
    fig.text(0.6,0.8,'Model $R^{2}$ = '+str(round(r2,2)))
    cyc_num = 300
    cycles = np.array(np.linspace(1,len(cap_ret[0]),len(cap_ret[0])))


    fig=plt.plot(cap_ret[0], color = 'blue',label='Prediction')
    
    plt.fill_between(cycles,
                 np.array(cap_ret[0]+err),
                 np.array(cap_ret[0]-err),
                 color='gray',
                 alpha=0.2,
                 interpolate=True,label='MAE')
    plt.xlabel('Cycle Number')
    plt.ylabel('Capacity Retention, [%]')
    plt.legend(loc='lower left')
    plt.show()
    
    return()
def cap_ret_online_NN_plot(eis_data,cycling_data, hidden_layers_sizes, learning_rate, alpha, n_iter, test_size,cyc_num,random_state=None):
    
    '''Online sklearn MLPRegressor NN for prediction of capacity at every cycle 1-300n
    
    Parameters
    ----------
    input_features : EIS and 1st 10 cycles experimental data
    
    hidden_layers_sizes: tuple of (N1, N2, N3 ... Nn) for n hidden layers with each layer having Nn nodes
    
    learning_rate : initial learning rate
    
    alpha: value for alpha
    
    n_iter: max iterations for NN learning
    
    test_size: fraction of training data set aside for test
    
    random_state: set to int for reproducible results. Default is None
    

    Returns
    -------
    cap_ret_pred: Predicted capacity retentions for experimental sample at each cycle
    
    r2_online_NN: R-squared value for predictions on test data vs. known values
    
    MSE_by_cycle_online_NN: MSE at each cycle number for test data vs. known values 
    '''
    
    #Defining model
    input_features=ml_features(eis_data,cycling_data)
    online_NN  = MLPRegressor(solver='lbfgs', activation='tanh', max_iter= n_iter,
                            learning_rate_init=learning_rate,
                            hidden_layer_sizes = hidden_layers_sizes,
                            alpha=alpha)
    
    #Getting Features and y_values
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')               
    
    X_train_i=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X_train_i=np.transpose(X_train_i)
    y_train_i=np.transpose(ret)
    y_train_i=y_train_i[1:,0:300]

    X_train, X_test, y_train, y_test = train_test_split(X_train_i, y_train_i, test_size= test_size, random_state=random_state)
    
    #Training model
    
    online_NN.fit(X_train, y_train)
    
    #Predicting test data
    
    y_pred_online = online_NN.predict(X_test)
    
    #Accuracy params for test data
    
    
    r2_online_NN = r2_score(np.transpose(y_test), np.transpose(y_pred_online))
    err=average_err_per_cyc(y_test,online_NN.predict(X_test))



    #Predict from given data
    
    cap_ret_pred = online_NN.predict(input_features)
    fig, ax = plt.subplots(figsize=(8,6))
    fig.text(0.6,0.8,'Model $R^{2}$ = '+str(round(r2_online_NN,2)))
    cyc_num = 300
    cycles = np.array(np.linspace(1,len(cap_ret_pred[0]),len(cap_ret_pred[0])))


    fig=plt.plot(cap_ret_pred[0], color = 'blue',label='Prediction')
    
    plt.fill_between(cycles,
                 np.array(cap_ret_pred[0]+err),
                 np.array(cap_ret_pred[0]-err),
                 color='gray',
                 alpha=0.2,
                 interpolate=True,label='MAE')
    plt.xlabel('Cycle Number')
    plt.ylabel('Capacity Retention, [%]')
    plt.legend(loc='lower left')
    plt.show()
    return ()



def cap_ret_online_NN(eis_data,cycling_data, hidden_layers_sizes, learning_rate, alpha, n_iter, test_size,cyc_num,random_state=None):
    
    '''Online sklearn MLPRegressor NN for prediction of capacity at every cycle 1-300n
    
    Parameters
    ----------
    input_features : EIS and 1st 10 cycles experimental data
    
    hidden_layers_sizes: tuple of (N1, N2, N3 ... Nn) for n hidden layers with each layer having Nn nodes
    
    learning_rate : initial learning rate
    
    alpha: value for alpha
    
    n_iter: max iterations for NN learning
    
    test_size: fraction of training data set aside for test
    
    random_state: set to int for reproducible results. Default is None
    

    Returns
    -------
    cap_ret_pred: Predicted capacity retentions for experimental sample at each cycle
    
    r2_online_NN: R-squared value for predictions on test data vs. known values
    
    MSE_by_cycle_online_NN: MSE at each cycle number for test data vs. known values 
    '''
    
    #Defining model
    input_features=ml_features(eis_data,cycling_data)
    online_NN  = MLPRegressor(solver='lbfgs', activation='tanh', max_iter= n_iter,
                            learning_rate_init=learning_rate,
                            hidden_layer_sizes = hidden_layers_sizes,
                            alpha=alpha)
    
    #Getting Features and y_values
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')               
    
    X_train_i=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X_train_i=np.transpose(X_train_i)
    y_train_i=np.transpose(ret)
    y_train_i=y_train_i[1:,0:300]

    X_train, X_test, y_train, y_test = train_test_split(X_train_i, y_train_i, test_size= test_size, random_state=random_state)
    
    #Training model
    
    online_NN.fit(X_train, y_train)
    
    #Predicting test data
    
    y_pred_online = online_NN.predict(X_test)
    
    #Accuracy params for test data
    
    
    r2_online_NN = r2_score(np.transpose(y_test), np.transpose(y_pred_online))
    err=average_err_per_cyc(y_test,online_NN.predict(X_test))

    #Predict from given data
    
    cap_ret_pred = online_NN.predict(input_features)
    
    return (round(cap_ret_pred[0][cyc_num-1],2),round(err[cyc_num-1],2))

def rdf_online_st(eis_data,cycling_data,n_estimators, max_features, max_depth,test_size,cyc_num):
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')
    X_features=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X=np.transpose(X_features)
    y=np.transpose(ret)
    y=y[1:45]
    model = RandomForestRegressor(n_estimators= n_estimators, max_features = max_features, max_depth=max_depth,random_state=42,n_jobs=-1)
      
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size= test_size, random_state=42)
    model.fit(X_dev, y_dev)
    
    r2=r2_score(np.transpose(y_test), np.transpose(model.predict(X_test)))
    
    features= ml_features(eis_data,cycling_data)
    
    
    cap_ret=model.predict(features)
    err=average_err_per_cyc(y_test,model.predict(X_test))


    fig, ax = plt.subplots(figsize=(8,6))
    fig.text(0.6,0.8,'Model $R^{2}$ = '+str(round(r2,2)))
    
    cycles = np.array(np.linspace(1,len(cap_ret[0]),len(cap_ret[0])))


    ax=plt.plot(cap_ret[0], color = 'blue',label='Prediction')
    
    plt.fill_between(cycles,
                 np.array(cap_ret[0]+err),
                 np.array(cap_ret[0]-err),
                 color='gray',
                 alpha=0.2,
                 interpolate=True,label='MAE')
    plt.xlabel('Cycle Number')
    plt.ylabel('Capacity Retention, [%]')
    plt.legend(loc='lower left')
    plt.show()

    
    return(fig,round(cap_ret[0][cyc_num-1],2),round(err[cyc_num-1],2))


def cap_ret_online_NN_st(eis_data,cycling_data, hidden_layers_sizes, learning_rate, alpha, n_iter, test_size,cyc_num,random_state=None):
    
    '''Online sklearn MLPRegressor NN for prediction of capacity at every cycle 1-300n
    
    Parameters
    ----------
    input_features : EIS and 1st 10 cycles experimental data
    
    hidden_layers_sizes: tuple of (N1, N2, N3 ... Nn) for n hidden layers with each layer having Nn nodes
    
    learning_rate : initial learning rate
    
    alpha: value for alpha
    
    n_iter: max iterations for NN learning
    
    test_size: fraction of training data set aside for test
    
    random_state: set to int for reproducible results. Default is None
    

    Returns
    -------
    cap_ret_pred: Predicted capacity retentions for experimental sample at each cycle
    
    r2_online_NN: R-squared value for predictions on test data vs. known values
    
    MSE_by_cycle_online_NN: MSE at each cycle number for test data vs. known values 
    '''
    
    #Defining model
    input_features=ml_features(eis_data,cycling_data)
    online_NN  = MLPRegressor(solver='lbfgs', activation='tanh', max_iter= n_iter,
                            learning_rate_init=learning_rate,
                            hidden_layer_sizes = hidden_layers_sizes,
                            alpha=alpha)
    
    #Getting Features and y_values
    ret=loadtxt(os.path.join(data_path,'44_cell_cap_ret_300_cycles.csv'),delimiter=',',skiprows=1)
    var=loadtxt(os.path.join(data_path,'44_cell_cap_diff_var_1st_10cycles.csv'),delimiter=',',skiprows=1)
    Z1max=loadtxt(os.path.join(data_path,'Z1max.csv'), delimiter=',')
    Z2max=loadtxt(os.path.join(data_path,'Z2max.csv'), delimiter=',')
    f_max=loadtxt(os.path.join(data_path,'freq_fit_max.csv'), delimiter=',')
    Z1_hf=loadtxt(os.path.join(data_path,'Z1_high_f.csv'), delimiter=',')
    Z2_hf=loadtxt(os.path.join(data_path,'Z2_high_f.csv'), delimiter=',')               
    
    X_train_i=np.vstack((var[:,1:45],f_max,Z1max,Z2max,Z1_hf,Z2_hf))
    X_train_i=np.transpose(X_train_i)
    y_train_i=np.transpose(ret)
    y_train_i=y_train_i[1:,0:300]

    X_train, X_test, y_train, y_test = train_test_split(X_train_i, y_train_i, test_size= test_size, random_state=42)
    
    #Training model
    
    online_NN.fit(X_train, y_train)
    
    #Predicting test data
    
    y_pred_online = online_NN.predict(X_test)
    
    #Accuracy params for test data
    
    
    r2_online_NN = r2_score(np.transpose(y_test), np.transpose(y_pred_online))
    err=average_err_per_cyc(y_test,online_NN.predict(X_test))



    #Predict from given data
    
    cap_ret_pred = online_NN.predict(input_features)
    

    
    #prodict plotfrom given data 
    cap_ret_pred = online_NN.predict(input_features)
    err=average_err_per_cyc(y_test,online_NN.predict(X_test))
    fig, ax = plt.subplots(figsize=(8,6))
    fig.text(0.6,0.8,'Model $R^{2}$ = '+str(round(r2_online_NN,2)))
    
    cycles = np.array(np.linspace(1,len(cap_ret_pred[0]),len(cap_ret_pred[0])))


    ax=plt.plot(cap_ret_pred[0], color = 'blue',label='Prediction')
    
    plt.fill_between(cycles,
                 np.array(cap_ret_pred[0]+err),
                 np.array(cap_ret_pred[0]-err),
                 color='gray',
                 alpha=0.2,
                 interpolate=True,label='MAE')
    plt.xlabel('Cycle Number')
    plt.ylabel('Capacity Retention, [%]')
    plt.legend(loc='lower left')
    plt.show()

    return (fig, round(cap_ret_pred[0][cyc_num-1],2),round(err[cyc_num-1],2))

    
    
    
    


    
    