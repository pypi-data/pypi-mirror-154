
# A package to easy implement memory-based recommender
The description here will walkthrough a tutorial to implement a memory-based recommender step by step.


## To install the package

```
pip install memory-recommender==0.0.4
```

## Let's get started

Let me show you how the package works, here will show user-based top-n recommendation. To make item-based, simply switch the index_col and column_col

## **Step 1**: To get a sample dataframe from MovieLens
The first step is to get a sample dataset to show how it works. Let get a sample dataset from MovieLens.

**Input [1]**:

```python
# let's import the package
from m_recommender import memory as m

# get dataframe
df = m.get_df()
df
```

**Output [1]**:

```
+-------+----------+-----------+----------+-------------------------------------+
|       |   userId |   movieId |   rating | title                               |
+=======+==========+===========+==========+=====================================+
| 32170 |      605 |      1498 |        2 | Inventing the Abbotts               |
+-------+----------+-----------+----------+-------------------------------------+
| 83001 |       38 |    110102 |        4 | Captain America: The Winter Soldier |
+-------+----------+-----------+----------+-------------------------------------+
| 78180 |      574 |     64614 |        4 | Gran Torino                         |
+-------+----------+-----------+----------+-------------------------------------+
| 17477 |      190 |       785 |        5 | Kingpin                             |
+-------+----------+-----------+----------+-------------------------------------+
| 31043 |       57 |      1378 |        4 | Young Guns                          |
+-------+----------+-----------+----------+-------------------------------------+
1000 rows × 4 columns
```

## **Step 2**: To pivot a table and compute the pearson correlation
Next, in this function, it will help you to settle (3) pre-processing tasks. Those tasks are common tasks before putting it into memory-based recommender, which are:
(1): Stratified Split into training subset and testing subset
(2): Pivot the dataset
(3): Normalised the dataset

**Input [2]**:
```python

df2=df # selected dataframe
index_col='userId' # to make a pivot table with what kind of index column
columns_col='title' # to make a pivot table with what kind of columns
values_col='rating' # to make a pivot table with what kind of values
random_state_value =42
proposed_test_size=0.2 # the proposed stratified split with the index column, if rejected, it will auto propose a new one

X_train, X_test, matrix_train_norm, matrix_train_norm_treated_pearson, matrix_test = m.recommender_pre_processing(df2=df, \
                                                                                                                  index_col=index_col, \
                                                                                                                  columns_col=columns_col, \
                                                                                                                  values_col=values_col, \
                                                                                                                  random_state_value =random_state_value, \
                                                                                                                  proposed_test_size=proposed_test_size)
```

**Output [2]**:
```
STATUS: Unique value for userId = 386
STATUS: The proportion of the stratified splitting is 0.4246 to be able to perform stratify split
STATUS: The dataframe is splitted with test size of 0.4246
STATUS: Dimension of "X_train" = (471, 4)
STATUS: Dimension of "X_test" = (349, 4)
STATUS: Pivoted for matrix training set
STATUS: Dimension of "train matrix" = (206, 422)
STATUS: Pivoted for matrix testing set
STATUS: Dimension of "test matrix" = (206, 312)
...
STATUS: Computing Pearson Correlation ...
STATUS: Computing Pearson Correlation Done
...
```

## **Step 3**: To make a prediction (user-based top-10 recommendation)

Now, the dataset is ready to make a prediction. Let say we want to predict userId 15 to see what movies are recommended for this user. And the function to implement is show here.

**Input [3]**:
```python
matrix_train_norm_treated_pearson = matrix_train_norm_treated_pearson # pearson correlation dataset as computed in previous kernel
matrix_train_norm = matrix_train_norm # normalised dataset, as computed in previous kernel
col_Id = 15 # selected target column to make a prediction for it (here is a userId)
thereshold = None # thereshold of similarity
n_rows = 100 # returned number of similar elements
topN = 10 # to return the top N ranked elements
show_text = False # want to show the computation behind the scene?

topn_result, col_Id = m.collaborative_recommender(matrix_train_norm_treated_pearson=matrix_train_norm_treated_pearson, \
                                                matrix_train_norm = matrix_train_norm, \
                                                col_Id = col_Id, \
                                                thereshold = thereshold, 
                                                n_rows = n_rows, \
                                                topN = topN, \
                                                show_text = show_text)
topn_result
```
**Output [3]**:
```
+-----+----------------------+------------------+
|     | conditional_column   |   weighted_score |
+=====+======================+==================+
| 188 | Batman Returns       |      7.55878e-18 |
+-----+----------------------+------------------+
| 114 | Taken                |      3.84573e-18 |
+-----+----------------------+------------------+
| 266 | The Sixth Sense      |      3.13265e-18 |
+-----+----------------------+------------------+
|  36 | Twelve Monkeys       |      2.85393e-18 |
+-----+----------------------+------------------+
|  27 | Romeo + Juliet       |      2.51117e-18 |
+-----+----------------------+------------------+
| 165 | Withnail & I         |      2.23939e-18 |
+-----+----------------------+------------------+
| 239 | The Boondock Saints  |      2.23008e-18 |
+-----+----------------------+------------------+
| 196 | Baraka               |      2.17991e-18 |
+-----+----------------------+------------------+
|  44 | Simon Birch          |      2.1664e-18  |
+-----+----------------------+------------------+
|  72 | Toy Story            |      1.96495e-18 |
+-----+----------------------+------------------+

```
## **Step 4**:To evaluate the user-based top-N recommender

It is also important to evaluate the recommender. This can let us know that the recommender is it perform well or not for this dataset. Because at the first place we have stratified split the data into training and testing subsets, so the testing subset are the actual moviesthat has been watched by the users. So, the recommended movies will be compared to the testing subset.

**Input [4]**:
```python

topN = 10
matrix_train_norm = matrix_train_norm
matrix_train_norm_treated_pearson = matrix_train_norm_treated_pearson
matrix_test = matrix_test
target_users_len =None
n_rows=100
SIZE=None
limit_len_actual='no' # limit test set item size
recommender_name='User-Based'


result_metric = m.get_evaluation_concat(topN =topN, matrix_train_norm = matrix_train_norm, \
                                      matrix_train_norm_treated_pearson = matrix_train_norm_treated_pearson, \
                                      matrix_test = matrix_test, \
                                      target_users_len = target_users_len, \
                                      n_rows=100, SIZE=None, limit_len_actual='no',recommender_name='User-Based')
result_metric


```
**Output [4]**:

```
STATUS: Starting TopN = 10
STATUS: Random shuffled and sample dataset done
STATUS: Complete predictions 1/103...0.97%
STATUS: Complete predictions 11/103...10.68%
STATUS: Complete predictions 21/103...20.39%
STATUS: Complete predictions 31/103...30.10%
STATUS: Complete predictions 42/103...40.78%
STATUS: Complete predictions 52/103...50.49%
STATUS: Complete predictions 62/103...60.19%
STATUS: Complete predictions 73/103...70.87%
STATUS: Complete predictions 83/103...80.58%
STATUS: Complete predictions 93/103...90.29%
STATUS: Complete predictions 103/103...100.00%
...
+----+---------------+------------------+---------------+------------------+
|    | Recommender   |   Precision@N=10 |   Recall@N=10 |   F-Measure@N=10 |
+====+===============+==================+===============+==================+
|  0 | User-Based    |           0.0039 |        0.0168 |           0.0063 |
+----+---------------+------------------+---------------+------------------+
```

Now, the user-based recommender is implemented. For item-based recommender, simply simply switch the index_col and column_col when want to pivot the table. Hope you enjoy it. If you like it please let me know.

This is contributed by [Morris Lee](http://www.morris-lee.com/).