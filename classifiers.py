from sklearn.base import clone
from sklearn.ensemble.forest import _generate_unsampled_indices
import numpy as np
import pandas as pd

def dropcol_importances(model, X_train, y_train, X_valid=None, y_valid=None, metric=None, sample_weights=None):
    if X_valid is None: 
        X_valid = X_train
    if y_valid is None: 
        y_valid = y_train
    model_ = clone(model)
    model_.random_state = 999
    model_.fit(X_train, y_train)
    if callable(metric):
        baseline = metric(model_, X_valid, y_valid, sample_weights)
    else:
        baseline = model_.score(X_valid, y_valid, sample_weights)
    print(baseline)
    imp = []
#     for col in X_train.columns:
    for i in range(X_train.shape[1]):
        col = X_train[:,i]
        model_ = clone(model)
        model_.random_state = 999
       # model_.fit(X_train.drop(col,axis=1), y_train)
        model_.fit(np.delete(X_train,i,1), y_train)
        if callable(metric):
            s = metric(model_, np.delete(X_valid,i,1), y_valid, sample_weights)
        else:
            s = model_.score(np.delete(X_valid,i,1), y_valid, sample_weights)
        print(s)
        drop_in_score = baseline - s
        imp.append(drop_in_score)
    imp = np.array(imp)
#     I = pd.DataFrame(data={'Feature':[i for i in range(X_train.shape[1])], 'Importance':imp})
#     I = I.set_index('Feature')
#     I = I.sort_values('Importance', ascending=False)
    return imp
            
def permutation_importances(rf, X_train, y_train, metric):
    baseline = metric(rf, X_train, y_train)
    imp = []
    for col in range(X_train.shape[1]):
        save = X_train[:,col].copy()
        X_train[:,col] = np.random.permutation(X_train[:,col])
        m = metric(rf, X_train, y_train)
        X_train[:,col] = save
        imp.append(baseline - m)
    return np.array(imp)

def oob_classifier_accuracy(rf, X_train, y_train):
    """
    Compute out-of-bag (OOB) accuracy for a scikit-learn random forest
    classifier. We learned the guts of scikit's RF from the BSD licensed
    code:
    https://github.com/scikit-learn/scikit-learn/blob/a24c8b46/sklearn/ensemble/forest.py#L425
    """
    X = X_train
    y = y_train

    n_samples = len(X)
    n_classes = len(np.unique(y))
    predictions = np.zeros((n_samples, n_classes))
    for tree in rf.estimators_:
        unsampled_indices = _get_unsampled_indices(tree, n_samples)
        tree_preds = tree.predict_proba(X[unsampled_indices, :])
        predictions[unsampled_indices] += tree_preds

    predicted_class_indexes = np.argmax(predictions, axis=1)
    predicted_classes = [rf.classes_[i] for i in predicted_class_indexes]

    oob_score = np.mean(y == predicted_classes)
    print(oob_score)
    return oob_score

def _get_unsampled_indices(tree, n_samples):
    """
    An interface to get unsampled indices regardless of sklearn version.
    """
    from sklearn.ensemble.forest import _get_n_samples_bootstrap
    n_samples_bootstrap = _get_n_samples_bootstrap(n_samples, n_samples)
    return _generate_unsampled_indices(tree.random_state, n_samples, n_samples_bootstrap)