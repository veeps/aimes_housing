from sklearn import metrics
import numpy as np
import pandas as pd

def regression_metrics(X, y, y_hat):
    mae = metrics.mean_absolute_error(y, y_hat) # mean absolute error
    mse = metrics.mean_squared_error(y, y_hat) # mean squared error
    rss = np.square(y - y_hat).sum() # residual sum of squares
    rmse = np.sqrt(mse) # root mean squared error
    r2 = metrics.r2_score(y, y_hat) # coefficient of determination
    def r2_adj(X, y, y_hat):
        n = len(X) # number of observations
        k = X.shape[1] # number of predictors
        r_squared = metrics.r2_score(y, y_hat) # r squared
        return r_squared - ((k-1)/(n-k))*(1-r_squared)
    adjusted_r2 = r2_adj(X, y, y_hat) # adjusted r squared
    metrics_dict = { # create a dictionary with all these values
        "MAE": [round(mae,2)],
        "MSE": [round(mse, 2)],
        "RSS": [round(rss,2)],
        "RMSE": [round(rmse,2)],
        "R Squared": [round(r2,2)],
        "Adjusted R Squared": [round(adjusted_r2,2)]
    }
    df = pd.DataFrame.from_dict(metrics_dict).T
    df.columns = [f"Model Based on {' '.join(X.columns)}"]
    df.reset_index(inplace = True)              
    return df # return values as a data frame