import xgboost as xgb
import sys
sys.path.append('../cpp_code')
import cgoss

class Voter:
    """A customer ensemble voting classifier"""
    def __init__(self, models, pf = None):
        self.delimiter = .5
        self.models = models
        self.pf = pf
        
    def predict_proba_soft(self, x):
        probas = []
        for line in x:
            prob = self.delimiter
            base = 0.5
            for m in self.models:

                if "sklearn" in str(type(m)) and ('KNeighborsClassifier' not in str(type(m)) and 'Extra' not in str(type(m)) ):
                    if len(m.coef_[0]) > len (line):
                        l = self.pf.transform(line.reshape(1, -1))
                        pred =  m.predict_proba(l)[0][1]
                        prob = cgoss.max_distance(prob, pred, self.delimiter)
                    else:
                        pred =  m.predict_proba(line.reshape(1, -1))[0][1]
                        prob = cgoss.max_distance(prob, pred, self.delimiter)
                elif "GridSearchCV" in str(type(m)): 
                    pred =  m.predict_proba(line.reshape(1, -1))[0][1]
                    prob = cgoss.max_distance(prob, pred, self.delimiter)    
                
                elif "xgboost" in str(type(m)):
                    D = xgb.DMatrix(line.reshape(1, -1))
                    pred =  cgoss.scale_confidence(m.predict(D), .0)
                    prob = cgoss.max_distance(prob, pred, self.delimiter)
                elif "Extra" in str(type(m)):
                    pred =  cgoss.scale_confidence(m.predict(line.reshape(1,-1)), .0)
                    prob = cgoss.max_distance(prob, pred, self.delimiter)
                else:
                    pred =  m.predict(line.reshape(1,-1))
                    prob = cgoss.max_distance(prob, pred, self.delimiter)
            probas.append(prob)
        return probas 