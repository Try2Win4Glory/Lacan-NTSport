import pandas, math
import numpy as np
from nitrotype import Racer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, ExtraTreesRegressor, VotingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_squared_log_error, median_absolute_error, mean_absolute_percentage_error,explained_variance_score, accuracy_score
async def check(username):
    df = pandas.read_csv("data.csv")
    df = df.drop_duplicates()
    df = df.sample(frac=1)
    features = ['avgSpeed', 'highSpeed', 'racesTotal', 'highestSession']
    X = df[features]
    y = df['Go']
    x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
    r1 = RandomForestRegressor()
    r2 = ExtraTreesRegressor()
    dtree_regressor = VotingRegressor([('rf', r1),('et', r2)])
    dtree_classifier = RandomForestClassifier()
    dtree_regressor = dtree_regressor.fit(x_train, y_train)
    dtree_classifier = dtree_classifier.fit(x_train, y_train)
    try:
        racer = await Racer(username)
        pred_regressor = (dtree_regressor.predict([[racer.wpm_average,racer.wpm_high,int(racer.races.replace(',', '')),int(racer.newdata['longestSession'])]]))
        pred_classifier = (dtree_classifier.predict([[racer.wpm_average,racer.wpm_high,int(racer.races.replace(',', '')),int(racer.newdata['longestSession'])]]))
        '''
        fn=features
        cn=['Go']
        fig, axes = plt.subplots(figsize=(20,20))
        tree.plot_tree(dtree.estimators_[0],filled=True, feature_names=fn, class_names=cn)
        #fig.savefig('rf_individualtree.png')
        '''
        prediction = dtree_regressor.predict(x_test)
        return {"botornot": [float(pred_classifier[0]), float(pred_regressor[0])], "accuracies": [{"r2_score": r2_score(y_test, prediction)}, {"mean_squared_error": mean_squared_error(y_test, prediction)},{"mean_absolute_error": mean_absolute_error(y_test, prediction)},{"mean_squared_log_error": mean_squared_log_error(y_test, prediction)}, {"median_absolute_error": median_absolute_error(y_test, prediction)},{"mean_absolute_percentage_error": mean_absolute_percentage_error(y_test, prediction)},{"explained_variance_score": explained_variance_score(y_test, prediction)}], "accuracy": [accuracy_score(y_test, dtree_classifier.predict(x_test)),1-mean_squared_error(y_test, prediction)]}
    except Exception as e:
        raise e
        return {"botornot": "error"}
