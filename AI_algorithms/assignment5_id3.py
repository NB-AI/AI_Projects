"""
Assignment 05 - id3
"""

import numpy as np

class ID3():
    def __init__(self):
        self.root = None

    def fit(self, X, y):
        self.root = DecisionTreeNode().split(X, y)
       # print(self.root, 'root in id3')
        return self

    def __str__(self):
        return str(self.root)


def entropy(labels):
    """returns the same as scipy.stats.entropy([positive, negative], base=2)"""
    n = len(labels)
    if n == 0:
        return 0.0
    positive = sum(labels) / n # sum(labels) works when we work with 1-s and 0-s as labels
    negative = 1 - positive # the 0 labels considered
    if positive == 0 or negative == 0:
        return 0.0
    return -positive * np.log2(positive) - negative * np.log2(negative) # only total number of two different features considered


class DecisionTreeNode():
    def __init__(self):
        self.label = None
        self.split_point = None
        self.split_feature = None
        self.left_child = None
        self.right_child = None


    def get_all_possible_split_points(self, features, labels):
        nr_samples, nr_features = features.shape
        split_points = [] # this should be a list of tuples (f_idx, split_at) where split_at is the value to split feature f_idx
        # add tuples using: split_points.append((f_idx, split_at))
        for f_idx in range(nr_features):
            # sort by feature feat
            idx_sort = features[:, f_idx].argsort()
            features = features[idx_sort, :] # We now get the samples sorted by the current feature index f_idx.
            # We get full array but the order of rows/samples is changed.

            labels = labels[idx_sort] # this kind of sorting only works for arrays not lists

            # TODO: check for consecutive samples whether the labels and features are different
            # be careful to not compare the 0th sample with the last sample when indexing
            # if labels and feature values are different, compute splitting values and add to list as shown above

            for index, single_sample in enumerate(features): # loop over each sample/row
                if index > 0:  # we aren't by the 0-th sample any longer
                    if memorized_label != labels[index] and single_sample[f_idx] != memorized_feat: # memorized_feat and memorized_label were defined when the index was 0
                        # single_sample[f_idx]  is the current feature of an indiviudal sample
                        # by different labels we want to set a split when the features have different values
                        split_at = (single_sample[f_idx] + memorized_feat) / 2
                        split_points.append((f_idx, split_at))  # f_idx is the feature_index
                if index == len(features)-1: # we are at the last sample of the dataset
                    break # break only stops the inner loop

                memorized_feat = single_sample[f_idx]
                memorized_label = labels[index]


        return split_points

    def get_optimal_split_point(self, features, labels):
        split_feature, split_point = None, None
        possible_split_points = self.get_all_possible_split_points(features, labels)

        current_best_ig = -np.Inf # or float('-Inf')


        # loop over all possible splitting points that you computed and return the best one

        for (f_idx, split_at) in possible_split_points:
            # TODO: compute information gain for splitting points and store the best one
            one_feat_several_samples = features[:,f_idx] # get an array of all sample values of the related feature
            info_gain = self.get_information_gain(one_feat_several_samples,labels,split_at)


            if info_gain > current_best_ig:
                split_feature = f_idx
                split_point = split_at

                current_best_ig = info_gain

        return split_feature, split_point

    def get_information_gain(self, x, y, split_point):
        ig = 0.0

        # TODO: implement the information gain as described in the slides
        # use the provided entropy() function
        # use <= and > for comparison (to get a comparable result)
        general_entropy = entropy(y)
        labels_smaller = []
        labels_bigger = []

        for ind, single_row in enumerate(x):
            single_sample = single_row # single_row[split_point]
            if single_sample <= split_point:
                labels_smaller.append(y[ind])
            else:
                labels_bigger.append(y[ind])

        # Compute the entropies:
        entropy_smaller = entropy(labels_smaller)
        entropy_bigger = entropy(labels_bigger)

        weight_smaller = len(labels_smaller) / len(y)
        weight_bigger = len(labels_bigger) / len(y)

        ig = general_entropy - (weight_smaller * entropy_smaller + weight_bigger * entropy_bigger)
        # from the function entropy() I can see that we only work with two labels. Therefore, I continue with that style.

        return ig


    def split(self, X, y):
        # TODO: implement the ID3 algorithm
        # if you reach a node that only contains samples with the same label store the label
        # otherwise compute the optimal split point using get_optimal_split_point
        # and create the child nodes (store them in self.left_child and self.right_child)
        # call split(X_left, y_left) and split(X_right, y_right) to recursively create the tree
        # again: use <= and > for comparison

        # Check if the labels:
        check = np.where(y==1)
        if len(check[0]) == 0 or len(check[0])==len(y): # we only heave one kind of label in there
            self.label = y[0]

        else: # We have to do the whole procedure of splitting again.

            # Get the optimal split:
            split_feat_ind, split_point = self.get_optimal_split_point(X, y)

            # Use a mask to distinguish between elements of left and right children:
            self.split_point = split_point
            self.split_feature = split_feat_ind

            mask_going_left = (X[:, self.split_feature] <= self.split_point)
            X_going_left = X[mask_going_left]
            y_going_left = y[mask_going_left]

            mask_going_right = (X[:, self.split_feature] > self.split_point)
            X_going_right = X[mask_going_right]
            y_going_right = y[mask_going_right]

            # Alternative: You could also sort the array and then split at the last value which is smaller or same as the splitting point.

            self.left_child = DecisionTreeNode().split(X_going_left,y_going_left)  # create a new node which is the left child of the current node noated as 'self'
            self.right_child = DecisionTreeNode().split(X_going_right,y_going_right)


        return self # self represents the current node.

    def __str__(self):
        if self.label is not None: return "(" + str(self.label) + ")"

        str_value = str(self.split_feature) + ":" + str(self.split_point) + "|"
        str_value = str_value + str(self.left_child) + str(self.right_child)
        return str_value
