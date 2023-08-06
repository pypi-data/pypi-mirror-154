# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:33:24 2022

@author: User
"""

import numpy as np
import pandas as pd
import optuna

import data_science_helper.helper_classification_model as hcm
import data_science_helper.model.neg_bagging_fraction__lgb_model as nbf_lgb_model


from sklearn.metrics import  roc_auc_score, average_precision_score 
from sklearn.model_selection import StratifiedKFold   
import lightgbm as lgb 

from optuna.trial import Trial
import gc
import warnings
warnings.filterwarnings("ignore")


from sklearn.model_selection import  StratifiedShuffleSplit
from sklearn.metrics import precision_recall_fscore_support

from lightgbm import early_stopping
from lightgbm import log_evaluation
import statistics

def objective_with_prune(trial: Trial, fast_check=True, X=None,y=None,fn_params=None, list_kpi=[], n_jobs=None, metric=None, num_rounds=None,early_stop=None,log=None,random_state=42):
    folds = 5
    
    
    test_size = hcm.get_test_size(X,log)
    if test_size == 0.20:
        kf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=random_state)
        print("StratifiedKFold")
    else:
        kf = StratifiedShuffleSplit(n_splits=folds, test_size=test_size, random_state=random_state)
        print("StratifiedShuffleSplit")
    
    X_train = X
    y_train = y    
    
    X_train.reset_index(inplace=True,drop=True)
    y_train.reset_index(inplace=True,drop=True)   
 
    gc.collect()
   
    models = []
    
    list_valid_score = []
    list_valid_score2 = []
    list_train_score = []
    
    list_valid_precision = []
    list_valid_recall = []
    list_valid_f1 = []
    list_valid_average_precision = []
    list_valid_roc_auc = []
    with_bias = False
    
    for train_idx, valid_idx in kf.split(X_train, y_train):
        train_data = X_train.iloc[train_idx,:], y_train[train_idx]
        valid_data = X_train.iloc[valid_idx,:], y_train[valid_idx]

        args = {
                "trial":trial, "train":train_data, "val":valid_data, "fn_params":fn_params, "cat_features":None, 
                "metric":metric,"n_jobs":n_jobs,"num_rounds":num_rounds,"early_stop":early_stop,"log":log,"random_state":random_state
                }

        model, kpi = fit_lgbm_with_pruning(**args)

        models.append(model)
        gc.collect()
        
        list_valid_precision.append(kpi["valid/precision"])
        list_valid_recall.append(kpi["valid/recall"])
        list_valid_f1.append(kpi["valid/f1"])
        list_valid_average_precision.append(kpi["valid/average_precision"])
        list_valid_roc_auc.append(kpi["valid/roc_auc"])        
        
        
        list_valid_score.append(kpi["valid/average_precision"])
        list_valid_score2.append(kpi["valid/average_precision2"])       
        
        list_train_score.append(kpi["train/average_precision"])
        
        bias = kpi["bias"]
        
        if (bias>0.15):
            with_bias = True
            break
        
        if fast_check:
            break
            
    mean_valid_score = statistics.mean(list_valid_score)
    mean_valid_score2 = statistics.mean(list_valid_score2)

    std_valid_score = statistics.pstdev(list_valid_score)
    
    mean_train_score = statistics.mean(list_train_score)
    std_train_score = statistics.pstdev(list_train_score)
             
    mean_valid_precision = statistics.mean(list_valid_precision)           
    std_valid_precision = statistics.pstdev(list_valid_precision)
    
    mean_valid_recall = statistics.mean(list_valid_recall)           
    std_valid_recall = statistics.pstdev(list_valid_recall)
    
    mean_valid_f1 = statistics.mean(list_valid_f1)           
    std_valid_f1 = statistics.pstdev(list_valid_f1)
    
    mean_valid_average_precision = statistics.mean(list_valid_average_precision) 

    std_valid_average_precision = statistics.pstdev(list_valid_average_precision)
    
    mean_valid_roc_auc = statistics.mean(list_valid_roc_auc)           
    std_valid_roc_auc = statistics.pstdev(list_valid_roc_auc)
       
    bias = abs(mean_train_score - mean_valid_score)
    
    result_iter = {
        'trial_number':trial.number,
        'bias': bias,
        'overfitting':with_bias,
        'mean_train_score':mean_train_score,
        'std_train_score':std_valid_score,  
        
        'mean_valid_score':mean_valid_score,
        'mean_valid_score2':mean_valid_score2,
        'std_valid_score':std_train_score,       
          
    }   
    
    if(fast_check):
        split_dic = {}
        key_split = "split_{}".format(1)
        split_dic[key_split] = list_valid_score[0]
        result_iter.update(split_dic)
    else:
        for i in range(folds):
            split_train_dic = {}
            split_valid_dic = {}
            lb_fold = i+1
            
            key_split_train = "split_{}_train_score".format(lb_fold)
            split_train_dic[key_split_train] = list_train_score[i] if with_bias==False else -1
            result_iter.update(split_train_dic)
            
            key_split_valid = "split_{}_valid_score".format(lb_fold)          
            split_valid_dic[key_split_valid] = list_valid_score[i] if with_bias==False else -1
            result_iter.update(split_valid_dic)
        
        
    result_kpis = {   
        
        'mean_valid_precision':mean_valid_precision,
        'std_valid_precision':std_valid_precision,
        'mean_valid_recall':mean_valid_recall,
        'std_valid_recall':std_valid_recall, 
        'mean_valid_f1':mean_valid_f1,
        'std_valid_f1':std_valid_f1 ,
        'mean_valid_average_precision':mean_valid_average_precision,
        'std_valid_average_precision':std_valid_average_precision,       
        'mean_valid_roc_auc':mean_valid_roc_auc,
        'std_valid_roc_auc':std_valid_roc_auc       
    }
    
    result_iter.update(result_kpis)
  
    list_kpi.append(result_iter)
    return mean_valid_score

def fit_lgbm_with_pruning(trial=None, train=None, val=None, fn_params=None, cat_features=None,metric=None,n_jobs=1, num_rounds=None,early_stop=None,log=None,random_state=None ):
    """Train Light GBM model"""    
    X_train, y_train = train
    X_valid, y_valid = val
    
    train_params ,  dataset_params = fn_params(trial)
        
    nb_f = nbf_lgb_model.get_neg_bagging_fraction_params(y_train,{},log)
    
    train_params.update(nb_f)
    
    params_config = {"seed": random_state, "n_jobs":n_jobs,"objective":'binary' , "metric": metric}

    train_params.update(params_config)
    


    d_train = lgb.Dataset(X_train, label=y_train, categorical_feature=cat_features, params=dataset_params)
    d_valid = lgb.Dataset(X_valid, label=y_valid, categorical_feature=cat_features, params=dataset_params)

    watchlist = [d_valid]    

    
    pruning_callback_v = optuna.integration.LightGBMPruningCallback(trial, "average_precision",
                                                                  valid_name="data_valid")
    
    model = lgb.train(train_params,                 
                      num_boost_round = num_rounds,
                      train_set=d_train,
                      valid_names = ['data_valid'],
                      valid_sets=watchlist,
                      callbacks=[log_evaluation(log),pruning_callback_v,early_stopping(early_stop)]
                     )

    # predictions
    
    y_pred_prob_train = model.predict(X_train, num_iteration=model.best_iteration)   
    y_pred_prob_valid = model.predict(X_valid, num_iteration=model.best_iteration)   
    
    y_pred_valid = np.rint(y_pred_prob_valid)
    
    train_average_precision = average_precision_score(y_train, y_pred_prob_train)
    
    valid_average_precision2 = model.best_score['data_valid']['average_precision']
    valid_average_precision = average_precision_score(y_valid, y_pred_prob_valid)
    
    precision, recall, f1, support = precision_recall_fscore_support(y_valid, y_pred_valid ,average="binary",pos_label=1)
    roc_auc = roc_auc_score(y_valid, y_pred_prob_valid) 
    

    bias = train_average_precision - valid_average_precision    
 
    kpi = {'train/average_precision': train_average_precision,           
           'valid/average_precision': valid_average_precision,
           'valid/average_precision2': valid_average_precision2,
           'valid/precision': precision,
           'valid/recall': recall,
           'valid/f1': f1,
           'valid/roc_auc': roc_auc,
           'bias':bias
          }
    return model, kpi



  

def lgb_model_optuna(X_train=None, y_train=None,n_trials=2,fast_check=True,fn_params=None, 
                      n_jobs=None, metric=None, num_rounds=None,early_stop=None,log=None,random_state=42):
    
    if log == 0:
        optuna.logging.set_verbosity(optuna.logging.ERROR)
    
    list_kpi_ = []
    sampler = optuna.samplers.RandomSampler(seed=random_state)
    pruner=optuna.pruners.MedianPruner(n_warmup_steps=5)
    study = optuna.create_study(pruner=pruner,sampler=sampler,direction="maximize")


    func = lambda trial: objective_with_prune(trial,fast_check=fast_check, X=X_train, y=y_train,fn_params=fn_params, list_kpi=list_kpi_,
                                              n_jobs=n_jobs, metric=metric, num_rounds=num_rounds,early_stop=early_stop,log=log,
                                              random_state=random_state)
    
    study.optimize(func, n_trials=n_trials, n_jobs=n_jobs)

    best_params = study.best_params
    result = pd.DataFrame(list_kpi_)
    
    
    trials_dataframe = study.trials_dataframe()

    return result, best_params, study.best_value , trials_dataframe



def get_best_value_nob(result_,nob_group="0.0-0.15"):
    #result_ = result.copy()
    labels = ["{0} - {1}".format(i, i + 0.1) for i in np.linspace(0,1,10,endpoint=True)] #, labels=labels
    labels = ["0.0-0.15","0.15-0.2","0.2-0.3","0.3-0.4","0.4-0.5","0.5-0.6","0.6-0.7","0.7-0.8","0.8-0.9","0.9-1.0"]
    intervalos = [0. , 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ]    
    result_["bias_group"] = pd.cut(result_.bias, intervalos, right=False, labels=labels)
    #result_["bias_group"] = pd.cut(result_.bias, np.linspace(0,1,11,endpoint=True), right=False, labels=labels)
    final_result = result_[(result_.bias_group==nob_group) & (result_.overfitting==False)].sort_values(by=['mean_valid_score'], ascending=False)
    best_value_nob = final_result['mean_valid_score'].iloc[0]
    return best_value_nob

def get_params_by_trial_number(trials_dataframe_,trial_number):

    best_trial_nob = trials_dataframe_[trials_dataframe_.number==trial_number].copy()
    cls_to_delete = ["number","value","datetime_start","datetime_complete","duration","state"]
    best_trial_nob.drop(columns=cls_to_delete, inplace=True)

    best_trial_nob.columns = best_trial_nob.columns.str.replace('params_', '')
    best_params_nob = best_trial_nob.to_dict(orient='records')[0]

    return best_params_nob


def get_best_trial_number_nob(result_,nob_group="0.0-0.15"):
    #result_ = result.copy()
    labels = ["{0} - {1}".format(i, i + 0.1) for i in np.linspace(0,1,10,endpoint=True)] #, labels=labels
    labels = ["0.0-0.15","0.15-0.2","0.2-0.3","0.3-0.4","0.4-0.5","0.5-0.6","0.6-0.7","0.7-0.8","0.8-0.9","0.9-1.0"]
    intervalos = [0. , 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ]    
    result_["bias_group"] = pd.cut(result_.bias, intervalos, right=False, labels=labels)
    #result_["bias_group"] = pd.cut(result_.bias, np.linspace(0,1,11,endpoint=True), right=False, labels=labels)
    final_result = result_[(result_.bias_group==nob_group) & (result_.overfitting==False)].sort_values(by=['mean_valid_score'], ascending=False)
    trial_number = final_result['trial_number'].iloc[0]
    return trial_number


def get_kpis_by_trial_number(res,trial_number):

    result_ = res[res.trial_number==trial_number].copy()
    if len(result_)==0:
        return None
    result_dic = result_.to_dict(orient='records')[0]
    return result_dic