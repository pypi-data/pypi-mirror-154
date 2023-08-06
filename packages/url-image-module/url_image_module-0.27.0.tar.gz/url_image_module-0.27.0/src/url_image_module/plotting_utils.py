from typing import Dict, List, Optional, Tuple
from PIL.Image import Image

import torch
from torch.utils.data import DataLoader
from torch import device
import torch.nn as nn

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from matplotlib import figure
import seaborn as sns
plt.style.use('ggplot')
plt.ion()

from typing import Set, Dict, Optional, List, Union

from .constants import (
    IMAGE_NORMALIZE_MEAN,
    IMAGE_NORMALIZE_STD,
)
from .misc_utils import (
    prettify_underscore_string
)

from .metric_utils import (
    calc_confusion_matrix,
    calc_metric_scores_dict,
)

from .data_labeling_utils import (
    compute_label_counts
)

# Function taken from https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html 
def imshow(inp: Image, title: Optional[str] = None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array(IMAGE_NORMALIZE_MEAN)
    std = np.array(IMAGE_NORMALIZE_STD)
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

# Function taken from https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
def visualize_model(model: nn.Module, device: device, pred_loader: DataLoader, class_label_dict: Dict[int, str], num_images: int = 6) -> None:
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, inputs in enumerate(pred_loader):
            inputs = inputs.to(device)
            outputs = model(inputs)
            preds = outputs.max(1, keepdim=True)[1] # get index of max log-probability
            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images//2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_label_dict[preds[j].item()]))
                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    return

# Graph Visualizations for training & dev performance and other values over time
def plot_values_over_epochs(train_value_list: List[float], dev_value_list: List[float], value_name: str, min_or_max: str = 'max') -> None:
    """Plots line plots of values across epochs for both the training and dev sets.

        A line is plotted for both train and dev set values over the epochs. A vertical line is drawn at the epoch index corresponding to the
        best value on the dev set.

    Args:
        train_value_list: Values for the model on the training set over len(train_value_list) epochs.
        dev_metric_list: Values for the model on the dev set over len(dev_value_list) epochs.
        value_name: Name of the value being plotted. E.g. 'Average Loss'
        min_or_max: Determines how to find the best value on the dev set values, i.e. finding the min or max value. Defaults to 'max'.
    """
    assert len(train_value_list) == len(dev_value_list), 'train_value_list and dev_value_list must be the same length.'
    assert min_or_max == 'min' or min_or_max == 'max', "min_or_max must be 'min' or 'max'"
    epochs = len(train_value_list)
    epochs_list = range(1, epochs + 1)
    best_dev_value, best_dev_value_idx = find_best_value_and_index(dev_value_list, min_or_max)
    best_dev_value_epoch = best_dev_value_idx + 1
    plt.xlabel('Epoch')
    plt.ylabel(value_name)
    plt.axvline(x=best_dev_value_epoch, color='red', label=f'{min_or_max.capitalize()} Dev {value_name} Epoch')
    plt.title(f'{value_name} per Epoch')
    plt.plot(epochs_list, train_value_list, marker='o', color='blue', label=f'Training {value_name}')
    plt.plot(epochs_list, dev_value_list, marker='s', color='orange', label=f'Dev {value_name}')
    plt.legend()
    plt.show()

def find_best_value_and_index(values_list: List[float], min_or_max: str) -> Tuple[float, int]:
    """Finds the best value in a list and returns the value and the index that value occurs.

    Args:
        values_list: Values to find best value in.
        min_or_max: Determines method to find best value, i.e. min or max value in values_list. Must be either 'min' or 'max'.

    Returns:
        best_value: best value in the values list, i.e. max value if min_or_max == 'max' or 
            min value if min_or_max == 'min'
        best_index: index where best value occurs in values_list
    """
    assert min_or_max == 'min' or min_or_max == 'max', "min_or_max must be 'min' or 'max'"
    best_value = max(values_list) if min_or_max == 'max' else min(values_list)
    best_index = values_list.index(best_value)
    return best_value, best_index

# Plotting for visualizing data distribution

# Plotting utility for visualizing model predictions

# Function inspired by https://github.com/DTrimarchi10/confusion_matrix/blob/master/cf_matrix.py
def plot_confusion_matrix_heatmap(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metrics_set: Optional[Set[str]] = None,
    group_names: Optional[List[str]] = None,
    ordered_labels_list: Optional[List[str]] = None,
    labels: Union[List[str], str] = 'auto',
    count: bool = True,
    normalize: bool = True,
    cbar: bool = True,
    xyticks: bool = True,
    xyplotlabels: bool = True,
    figsize: Optional[Tuple[float, float]] = None,
    cmap: str = 'Blues',
    title: Optional[str] = None
) -> None:
    """This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.

    Args:
        y_true:        1-D numPy row vector of ground truth labels
        y_pred:        1-D numPy row vector of labels predicted by model 
        metrics_set:   Set of metrics to be computed from y_true and y_pred. If set is provided, computed metrics are displayed on bottom of figure.
                    Default is None.
        group_names:   List of strings that represent the labels row by row to be shown in each square. Default is None.
        ordered_labels_list: List of labels (as they appear in y_true & y_pred), in the order they should appear in the confusion matrix. 
                                Default is None.
        labels:        List of strings containing the labels to be displayed on the x,y axis. Default is 'auto'
        count:         If True, show the raw number in the confusion matrix. Default is True.
        normalize:     If True, show the proportions for each category. Default is True.
        cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                    Default is True.
        xyticks:       If True, show x and y ticks. Default is True.
        xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
        figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
        cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                    See http://matplotlib.org/examples/color/colormaps_reference.html.
        title:         Title for the confusion matrix heatmap. Default is None.
    """

    cf = calc_confusion_matrix(y_true, y_pred, ordered_labels_list = ordered_labels_list)
    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names) == cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if normalize:
        group_percentages = ["{0:.2%}".format(value) for value in cf.flatten()/np.sum(cf)]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels,group_counts,group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0],cf.shape[1])


    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if metrics_set:
        metrics_dict = calc_metric_scores_dict(y_true, y_pred, metrics_set)
        stats_text = '\n'
        for metric, score in metrics_dict.items():
          stats_text += '\n{} = {:0.3f}'.format(prettify_underscore_string(metric), score)
    else:
        stats_text = ""


    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if figsize == None:
        #Get default figure size if not set
        figsize = plt.rcParams.get('figure.figsize')

    if xyticks == False:
        #Do not show labels if xyticks is False
        labels = False


    # MAKE THE HEATMAP VISUALIZATION
    plt.figure(figsize=figsize)
    sns.heatmap(
        cf,
        annot=box_labels,
        fmt="",
        cmap=cmap,
        cbar=cbar,
        xticklabels=labels,
        yticklabels=labels
    )

    if xyplotlabels:
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label' + stats_text)
    else:
        plt.xlabel(stats_text)
    
    if title:
        plt.title(title)

def plot_per_class_metric_bar_chart(
    task_name: str,
    y_true: np.ndarray, 
    y_pred: np.ndarray,
    class_label_dict: Dict[str, int],
    ordered_label_names: List[str], 
    width: float = 0.35,
    fig_size: Tuple[float, float] = (10, 5),
    title: Optional[str] = None,
    colors: Optional[List[str]] = None, 
    cmap: Optional[str] = None,
    label_size: float = 10,
    title_padding: float = 0,
    legend_outside_plot: bool = False
) -> figure:
    """Plots the Precision, Recall, and F1 Score for each class as a bar plot based on labels predicted by a model compared to the ground truth labels

    Args:
        task_name:     snake_case name of the task with the classes being plotted
        y_true:        1-D numPy row vector of ground truth labels
        y_pred:        1-D numPy row vector of labels predicted by model 
        class_label_dict:   Mapping from class string to integer label
        ordered_label_names: List of the keys in class_label_dict, i.e. the labels for the task ordered
                        for the plot, i.e. the metrics will for ordered_label_names[0] will be shown first on the left, then 
                        ordered_label_names[1], etc. Strings in this list must match exactly, the keys in class_label_dict
        width:         Float representing bar's width. Default is 0.35
        fig_size:      Tuple of the figure's (width, height) in inches. Default is (10, 5).
        title:         Title for the per class metric bar plot. Default is None.
        colors:        Ordered list of Matplotlib colors strings corresponding to color associated with each label. 
                    That is colors[0] is the bar color for the ordered_class_labels[0] label. Default is None.
        cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is None
                    See http://matplotlib.org/examples/color/colormaps_reference.html. Only used if colors is None.
        label_size:    Size of x-axis, y-axis, and metric labels
        title_padding: Adds padding to the title. Default is 0.
        legend_outside_plot: Places legend outside of plot in the top right corner of the figure window. 
                            Default is False.
    
    Returns:
        fig:        Matplotlib Figure object with per class metric bar plot
    """
    assert len(class_label_dict) == len(ordered_label_names)
    N = len(ordered_label_names)
    DECIMAL_PLACES = 3
    PADDING = 3
    
    METRIC_KEYS = ['precision', 'recall', 'f1-score']
    PRETTIFIED_METRICS = ['Precision', 'Recall', 'F1']
    SUPPORT_KEY = 'support'
    prettified_labels = [prettify_underscore_string(label) for label in ordered_label_names]

    target_names = [None]*len(class_label_dict)
    for class_label, i in class_label_dict.items():
        target_names[i] = class_label

    metric_dict = classification_report(y_true, y_pred, target_names=target_names, output_dict=True)

    if colors is None:
        data_color = [100*i for i in range(N)]
        data_color_normalized = [x / max(data_color) for x in data_color]
        cmap = plt.cm.get_cmap(cmap if cmap else 'Set1')
        colors = cmap(data_color_normalized)

    x = np.arange(len(METRIC_KEYS))  # the label locations

    fig, ax = plt.subplots(figsize = fig_size)
    ax.xaxis.label.set_size(label_size)
    ax.yaxis.label.set_size(label_size)

    for i in range(N):
        class_i_metrics = metric_dict[ordered_label_names[i]] 
        class_i_metric_vals = [round(class_i_metrics[m], DECIMAL_PLACES) for m in METRIC_KEYS]
        bar_labels = [f"{val}" for val in class_i_metric_vals]
        label = "{} ({})".format(prettified_labels[i], class_i_metrics[SUPPORT_KEY])
        rects_i = ax.bar(x + width*i, class_i_metric_vals, width, label=label, color=colors[i], edgecolor='black')
        for rect, label in zip(rects_i, bar_labels):
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2, height + 0.0125, label, ha="center", va="bottom",
            )
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Score')
    ax.set_xlabel('Metric')
    ax.set_title(title if title else f"Per Class Metric Scores for {prettify_underscore_string(task_name)}", pad=title_padding)
    ax.set_ylim(top=1.0)
    ax.set_xticks(x + (N/2 - 0.5)*width)
    ax.set_xticklabels(PRETTIFIED_METRICS)
    if legend_outside_plot:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    else:
        ax.legend()

    for metric in ax.get_xticklabels():
        metric.set_fontsize(label_size)
 
    fig.tight_layout()
    return fig 

# Plot Labeled Dataset Distribution
def plot_label_dist_bar_chart(
    task_name: str, 
    freq_series: pd.Series, 
    ordered_label_names: List[str],
    use_legend: bool = False,
    alt_labels: Optional[List[str]] = None,
    width: float = 0.35,
    fig_size: Tuple[float, float] = (10, 5),
    title: Optional[str] = None,
    colors: Optional[List[str]] = None, 
    cmap: Optional[str] = None, 
    label_rotation: float = 0, 
    label_size: float = 10, 
) -> figure:
    """Plots label distribution for the task_name task

    Args:
        task_name:  snake_case name of the task with the labels whose distribution is being plotted
                        Only used if title is None.
        freq_series:  Series containing all labels for the task
        ordered_label_names:  list containing the unique string labels in freq_series ordered from left to right
                        as their distributions will be shown in the plot
        use_legend:   Puts color legend on the plot. Default value is False
        alt_labels:  List of alternative labels to use in place of ordered_label_names. That is, alt_labels[0] is the alternative
                        label to present in the plot in place of ordered_label_names[0]
        width:         Float representing bar's width. Default is 0.35
        fig_size:      Tuple of the figure's (width, height) in inches. Default is (10, 5).
        title:         Title for the label distribution bar plot. Default is None.
        colors:        Ordered list of Matplotlib colors strings corresponding to color associated with each label. 
                    That is colors[0] is the bar color for the ordered_label_names[0] label. Default is None.
        cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is None
                    See http://matplotlib.org/examples/color/colormaps_reference.html. Only used if colors is None
        label_rotation:  Degrees to rotate the label names under the bars counterclockwise
        label_size:    Size of x-axis, y-axis labels and the names of the label under the corresponding bar
    
    Returns:
        fig:        Matplotlib Figure object with label distribution bar plot
    """
    if colors is None:
        COLOR_OFFSET = 100
        data_color = [COLOR_OFFSET*i for i in range(len(ordered_label_names))]
        data_color_normalized = [x / max(data_color) for x in data_color]
        cmap = plt.cm.get_cmap(cmap if cmap else 'Set1')
        colors = cmap(data_color_normalized)

    counts = compute_label_counts(freq_series, ordered_label_names)
    total = sum(counts)

    prettified_labels = [prettify_underscore_string(label) for label in ordered_label_names]

    if alt_labels is None:
        x_labels = prettified_labels
    else:
        x_labels = alt_labels
    
    x = np.arange(len(ordered_label_names))  # the label locations

    fig, ax = plt.subplots(figsize = fig_size)
    rects = ax.bar(x, counts, width, color=colors, edgecolor='black')

    ax.xaxis.label.set_size(label_size)
    ax.yaxis.label.set_size(label_size)
    # Text on the top of each bar
    for label in ax.get_xticklabels():
        label.set_fontsize(label_size)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Counts')
    ax.set_xlabel('Label')
    ax.set_title(title if title else f"Label Counts for {task_name}")
    ax.set_xticks(x)
    bar_labels = [f"{counts[i]} ({round(counts[i]/total*100, 2)}%)" for i in range(len(counts))]
    ax.set_xticklabels(x_labels, rotation = label_rotation)

    # Label bars with frequency and relative frequency
    for rect, label in zip(rects, bar_labels):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2, height + 0.025, label, ha="center", va="bottom",
            fontsize = 'large',
            fontweight = 'bold'
        )
        
    if use_legend:
        ax.legend(rects, prettified_labels)

    fig.tight_layout()
    return fig

def show_annotator_counts_from_dict(task_labels_unique_dict: Dict[str, Dict[str, Dict[int, List[str]]]]) -> None:
    """Plots a bar plot for each task in task_labels_unique_dict showing the number of images which have at or above a certain number of
        unique annotators. Useful heuristic for determining a cutoff, i.e. selecting only images which have 4 or more unique annotators.

    Args:
        task_labels_unique_dict: Dictionary containing dictionaries for each task which maps from an image to a dictionary containing
            user id -> list of labels mapping. Of the form {task: {img: {user: labels}}}
    """
    # task_labels_unique_dict structure: {task: {img: {user: labels}}}
    task_names = list(task_labels_unique_dict.keys())
    for task_name in task_names:
        # task dict
        task_dict = task_labels_unique_dict[task_name]
        # num_of_annotators_per_image = 
        num_of_annotators_per_image_dict = {}
        num_of_annotators_per_image = []
        # num_data_points_per_annotator_count = 
        num_data_points_per_annotator_count = {}
        for img in task_dict:
            annotator_count = len(task_dict[img].keys())
            num_of_annotators_per_image_dict[img] = annotator_count
            num_of_annotators_per_image.append(annotator_count)
            if annotator_count not in num_data_points_per_annotator_count:
                num_data_points_per_annotator_count[annotator_count] = 0
            num_data_points_per_annotator_count[annotator_count]+=1
        # unique_num_annotator_counts = 
        unique_num_annotator_counts = np.sort(list(set(num_of_annotators_per_image)))
        num_annotators_range = range(unique_num_annotator_counts[0], unique_num_annotator_counts[-1]+1)
        # at_and_above_counts
        at_and_above_counts = []
        for i in num_annotators_range:
            total_at_and_above = 0
            for j in range(i, unique_num_annotator_counts[-1]+1):
                if j in unique_num_annotator_counts:
                    total_at_and_above += num_data_points_per_annotator_count.get(j, 0)
            at_and_above_counts.append(total_at_and_above)
        plt.bar(num_annotators_range, at_and_above_counts)
        plt.xticks(num_annotators_range, [f'>={count}' for count in num_annotators_range])
        plt.xlabel('Number of Annotators')
        plt.ylabel('Number of Data Points')
        plt.title(f'Number of Labeled Data Points by Annotator Count for {task_name} Task')
        for num_annotators in num_annotators_range:
            at_and_above_count = at_and_above_counts[num_annotators-1]
            plt.text(num_annotators, at_and_above_count + 15, str(at_and_above_count), ha='center')
        plt.show()
