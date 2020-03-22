from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score


def get_scores(classifier, X_train, y_train, X_test, y_test, cv=5):
    return_scores = list()

    for score_type in ["accuracy", "precision", "recall", "f1"]:
        scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring=score_type)
        return_scores.append(scores.mean())

    rocauc = roc_auc_score(y_test, classifier.predict_proba(X_test)[:, 1])
    return_scores.append(rocauc)

    return return_scores


def get_all_scores(classifiers_to_test, X_train, y_train, X_test, y_test):

    classifier_scores = dict()

    for name, classifier in classifiers_to_test:
        accuracy, precision, recall, f1, roc_auc = get_scores(
            classifier, X_train, y_train, X_test, y_test,
        )

        classifier_scores[name] = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1": f1,
            "ROC_AUC": roc_auc,
        }

    return classifier_scores
