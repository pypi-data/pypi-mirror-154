
# Title
## _Subtitle_


**Objective**: To make common analysis easier and more expressive.

To install the package

```
pip install morris-learning==0.0.2
```

Let me show you how the package works

**Input [1]**:

```python
from morris_lee_package import morris_coding as m
df =m.get_df()
df
```

**Output [1]**:

```
+----+--------+--------+----------+--------+
|    |   col1 |   col2 | col3     |   col4 |
+====+========+========+==========+========+
|  0 |      1 |      3 | dog      |      9 |
+----+--------+--------+----------+--------+
|  1 |      2 |      4 |          |      8 |
+----+--------+--------+----------+--------+
|  2 |      3 |      5 | dog      |    nan |
+----+--------+--------+----------+--------+
|  3 |      4 |      6 | elephant |      6 |
+----+--------+--------+----------+--------+
|  4 |      5 |      7 | dragon   |      5 |
+----+--------+--------+----------+--------+
```

**Input [2]**:
```python
# To identify whether there is any null values:
m.null(df,'df')

# To easy print dimension of a dataframe
m.shape(df, 'df')
```

**Output [2]**:
```
STATUS: There is null value in dataframe
STATUS: Nulls of df = {'col3': '1 (20.0%)', 'col4': '1 (20.0%)'} of total 5
STATUS: Dimension of "df" = (5, 4)
```

**Input [3]**:
```python
# To identify whether there is any duplicate values in a column:
m.duplicate(df, 'col3')
```
**Output [3]**:
```
STATUS: There are 1 duplicate values in the column of "col3"
```

**Input [4]**:
```python
# To easy print value counts of a column, including also percentage:
m.vc(df, 'col3')
```
**Output [4]**:
```
+----------+---------+------------------+
| col3     |   count |   percentage (%) |
+==========+=========+==================+
| dog      |       2 |               50 |
+----------+---------+------------------+
| dragon   |       1 |               25 |
+----------+---------+------------------+
| elephant |       1 |               25 |
+----------+---------+------------------+
```

**Input [5]**:
```python
# To easy drop a column:
m.drop(df, 'col3')
```
**Output [5]**:
```
+----+--------+--------+--------+
|    |   col1 |   col2 |   col4 |
+====+========+========+========+
|  0 |      1 |      3 |      9 |
+----+--------+--------+--------+
|  1 |      2 |      4 |      8 |
+----+--------+--------+--------+
|  2 |      3 |      5 |    nan |
+----+--------+--------+--------+
|  3 |      4 |      6 |      6 |
+----+--------+--------+--------+
|  4 |      5 |      7 |      5 |
+----+--------+--------+--------+
```
**Input [6]**:
```python
# To easy one_hot_encode a column:
m.one_hot_encode(df, 'col3')
```
**Output [6]**:
```
+----+--------+--------+--------+-------+----------+------------+
|    |   col1 |   col2 |   col4 |   dog |   dragon |   elephant |
+====+========+========+========+=======+==========+============+
|  0 |      1 |      3 |      9 |     1 |        0 |          0 |
+----+--------+--------+--------+-------+----------+------------+
|  1 |      2 |      4 |      8 |     0 |        0 |          0 |
+----+--------+--------+--------+-------+----------+------------+
|  2 |      3 |      5 |    nan |     1 |        0 |          0 |
+----+--------+--------+--------+-------+----------+------------+
|  3 |      4 |      6 |      6 |     0 |        0 |          1 |
+----+--------+--------+--------+-------+----------+------------+
|  4 |      5 |      7 |      5 |     0 |        1 |          0 |
+----+--------+--------+--------+-------+----------+------------+
```

## Merging -A simplified and smarter way to merge your dataset

```python
mergex(df1 ,df2, column1, column2, df1_name=None, df2_name=None)
```

This is contributed by [Morris Lee](http://www.morris-lee.com/).