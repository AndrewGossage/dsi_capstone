import sys
sys.path.append('../cpp_code')
import cgoss
import xgboost as xgb
import pandas as pd
import pickle
import dill

def predict_bst():
    model = xgb.Booster()
    model.load_model('../models/xgb.json')
    df2 = pd.read_csv('../data/survey-results.csv')
    df2.dropna(inplace=True)
    df2.drop(columns='EmployeeNumber', inplace=True)
    df2 = pd.get_dummies(df2, columns = ['EducationField'] )
    with open('../pickles/sc.pkl', 'rb') as pickle_in:
        sc = pickle.load(pickle_in)
    X_train = sc.fit_transform(df2.drop(columns=['Attrition']))
    D = xgb.DMatrix(X_train)
    filt = 0.5
    df2['pred'] =  [ 1 if i > filt else 0 for i in  model.predict(D)]
    df2['proba'] = model.predict(D)
    # make prediction
    
    return df2

def predict():
    with open('../pickles/voter.pkl', 'rb') as pickle_in:
        v = dill.load(pickle_in)
    import cgoss
    df2 = pd.read_csv('../data/survey-results.csv')
    df2.dropna(inplace=True)
    df2.drop(columns='EmployeeNumber', inplace=True)
    df2 = pd.get_dummies(df2, columns = ['EducationField'] )
    with open('../pickles/sc.pkl', 'rb') as pickle_in:
        sc = pickle.load(pickle_in)
    X = sc.fit_transform(df2.drop(columns=['Attrition']))
    filt = 0.5
    pred = v.predict_proba_soft(X)
    df2['pred'] =  [ 1 if i > filt else 0 for i in  pred]
    df2['proba'] = pred   
    
    return df2





