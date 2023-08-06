from itertools import cycle

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def roc_from_predictions(y_score, y, title='Some extension of Receiver operating characteristic to multi-class',
                         labels=None, lw=2):
    """
    This function builds ROC curve from model predictions.
        - y_score - model class predictions (as numpy array)
        - y - one-hot encoded ground truth (as numpy array)
        - labels - class labels
        - lw - plot's line width
    """

    n_classes = y.shape[1]

    _roc(n_classes, y_score, y, title, labels, lw)


def roc_from_keras_model(compiled_model, x, y,
                         title='Some extension of Receiver operating characteristic to multi-class', labels=None, lw=2):
    """
    This function builds ROC curve from the Keras classification model.
        - compiled_model is a keras model
        - x - dataset
        - y - one-hot encoded ground truth (as numpy array)
        - labels - class labels
        - lw - plot's line width
    """

    n_classes = y.shape[1]
    y_score = compiled_model.predict(x)

    _roc(n_classes, y_score, y, title, labels, lw)


def _roc(n_classes: int, y_score, y, title: str, labels=None, lw=2):
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    # Plot all ROC curves
    plt.figure(1)

    _plot(fpr, tpr, roc_auc, n_classes, labels, title, lw)


def _plot(fpr, tpr, roc_auc, n_classes, labels, title, lw):
    plt.plot(fpr["micro"], tpr["micro"],
             label='micro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["micro"]),
             color='deeppink', linestyle=':', linewidth=4)
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                       ''.format(labels[i] if labels is not None else i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.show()
