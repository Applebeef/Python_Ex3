import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## 1.1.
## Load train.csv
import sklearn.metrics


def load_train_data():
    # ! your code here
    # df_train = pd.read_...
    df_train = pd.read_csv('train.csv')

    return df_train


## 1.2.
## Display some data - display the top 10 rows
def disp_some_data(df_train):
    # ! your code here
    # df_train...
    print(df_train.head(10))

    return


## 1.3.
## In order to know what to do with which columns, we must know what types are there, and how many different values are there for each.
def display_column_data(df_train: pd.DataFrame, max_vals=10):
    '''
    First, let's investigate the columns in the dataset columns, using the .info() command. For now, we'll deal just with int, float and strings.
    Note that "object" is for string
    '''

    df_train.info()

    '''
    Let's count the number of unique values per column:
    '''
    num_uq_vals_sr = df_train.nunique()
    print(num_uq_vals_sr)

    '''
    num_uq_vals_sr is pandas Series. It's index are the column names - "Survived", "Pclass", "Name", "Sex", ...
    Its values are the number of unique values for each column. For "Sex", for example, it is 2. For "Pclass", it is 3 - 3 classes of passengers.
    It discards NaN's by default. You can count NaN's as well with: df_train.nunique(dropna=False). Try it!
    '''

    '''
    For columns that have less than max_vals values, print the number of occurrences of each value
    '''
    # ! your code here
    # TODO maybe try to fit formatting (num_uq_vals_sr[<Code here>].index)
    columns_to_print = num_uq_vals_sr.index
    columns_to_print = [x for x in columns_to_print if num_uq_vals_sr[x] < max_vals]

    for col in columns_to_print:
        print('{:s}: '.format(col), dict(df_train[col].value_counts()))

    return


## 1.4
## Now that we know which columns are there, we can drop some of them - the ones that do not carry predictive power.
## In addition we will drop columns that we do not know how to handle such as free text.
## Drop the columns: PassengerId, Name, Ticket, Cabin
def drop_non_inform_columns(df_train):
    # ! your code here, store your results in df_lean
    to_drop = ["PassengerId", "Name", "Ticket", "Cabin"]
    df_lean = df_train.drop(to_drop, axis=1)

    return df_lean


def where_are_the_nans(df_lean: pd.DataFrame):
    # ! your code here: print and return the names of the columns that have at least one missing value, and the number of missing values
    # ! store your results in a dict or a series, where the index/key is the column name, and the value is the number of nans. For example:
    # !
    # ! cols_with_nans = {'col_1': 20, 'col_5': 1, 'col_4': 13}
    # ! DO NOT include columns with 0 NaN's - columns without missing values.
    res = df_lean.isna().sum()
    cols_with_nans = {x: res[x] for x in res.index if res[x] > 0}
    print(cols_with_nans)

    return cols_with_nans


## 2.2
## We see that the columns 'Age' and 'Embarked' have missing values. We need to fill them.
## Let's fill 'Age' with the average and 'Embarked' with the most common
def fill_titanic_nas(df_lean: pd.DataFrame):
    '''
    For "Embarked", consider using value_counts() to get (again) the value counts,
    and idxmax() on that result - to get the index in of the maximal value value_counts() - that is most common value in "Embarked"
    '''

    # ! your code here
    embarked = "Embarked"
    age = "Age"
    df_filled = df_lean.copy()
    df_filled[embarked] = df_filled[embarked].fillna(df_lean[embarked].value_counts().idxmax())
    df_filled[age] = df_filled[age].fillna(df_filled[age].mean())
    return df_filled


def encode_one_hot(df_filled: pd.DataFrame):
    '''
    There are 3 distinct values for "Embarked": "S", "C", "Q". Also, there are 3 classes of tickets. While the column "Pclass" is numeric,
    it is more categorical than numeric - the number of the class does not bear special meaning, and could've easily been A, B, C, and not 1, 2, 3.
    We shall encode these two variables by the "one-hot" scheme, which produces numerical values for categorical variables (columns).

    For a categorical variable X, with 3 values x1, x2, x3, "one-hot" introduces 3 new binary variables - X_1, X_2, X_3, where each represents whether X is valued
    x1, x2 or x3. It is called "one-hot", because at each row, only a single variable of X_1, X_2, X_3 will be 1, and the rest will be 0.

    In short: for a categorical variable with, say 7 distinct values, "one-hot" introduces 7 new binary variables,
    where at each row exactly one of the new variables is 1, with the rest being zero


    For example, suppose we have the following "Embarked" column:

     Index | "Embarked" | ...
    ------ +------------+------
        0  |   "S"      | ...
        1  |   "C"      | ...
        2  |   "C"      | ...
        3  |   "Q"      | ...
        4  |   "S"      | ...
        5  |   "Q"      | ...


    Then, applying "one-hot" to it, and naming the new columns "Emb_C", "Emb_Q", "Emb_S", will yield the following table:


     Index | "Embarked" | "Emb_C" | "Emb_Q" | "Emb_S" | ...
    -------+------------+---------+---------+---------+------
        0  |   "S"      | 0       | 0       | 1       | ...
        1  |   "C"      | 1       | 0       | 0       | ...
        2  |   "C"      | 1       | 0       | 0       | ...
        3  |   "Q"      | 0       | 1       | 0       | ...
        4  |   "S"      | 0       | 0       | 1       | ...
        5  |   "Q"      | 0       | 1       | 0       | ...



    Applying "one-hot" to "Embarked" introduces 3 new columns, where for each of the new columns we'll place 1 if the passenger embarked from that port, and 0 otherwise.

    '''

    # Apply one-hot to "Embarked" and "Pclass" columns.
    # For "Embarked", the new coumns should be named "Emb_C", "Emb_Q", "Emb_S"
    # For "Pclass", the new coumns should be named "Cls_1", "Cls_2", "Cls_3"

    # ****************************
    # ***** !!!!! ALSO !!!!! *****
    # ****************************
    #
    # For lack of better place, introduce a new column, "Bin_Sex" - a binary (1 or 0) version of the "Sex" column
    #
    # ****************************
    # ***** !!!!! ALSO !!!!! *****
    # ****************************

    # ! your code here. Hint: you are strongly encouraged to use pd.get_dummies(...) function and then rename the columns.
    one_hot_embarked = pd.get_dummies(df_filled["Embarked"], 'Emb', "_")
    df_one_hot = pd.concat([df_filled, one_hot_embarked], axis=1)
    one_hot_pclass = pd.get_dummies(df_filled["Pclass"], "Cls", "_")
    df_one_hot = pd.concat([df_one_hot, one_hot_pclass], axis=1)
    bin_sex = pd.DataFrame(data=np.where(df_one_hot["Sex"] == "male", 1, 0), columns=["Bin_Sex"])
    df_one_hot = pd.concat([df_one_hot, bin_sex], axis=1)
    df_one_hot.drop(["Embarked", "Pclass", "Sex"], axis=1, inplace=True)

    # *** NOTE ***: after encoding by one-hot, we may delete the original columns, although it is not necessery.

    return df_one_hot


def make_family(df_one_hot):
    '''
    Introduce a new column with the name "Family", that will be the sum of "SibSp" and "Parch" columns
    '''

    # ! your code here
    df_one_hot['Family'] = df_one_hot['SibSp'] + df_one_hot['Parch']

    return df_one_hot


def add_log1p(df_one_hot):
    # For each of the numeric columns: 'Age', 'SibSp', 'Parch', 'Fare', 'Family'
    # we introduce a new column that starts with the 'log1p_' string: 'log1p_Age', 'log1p_SibSp', 'log1p_Parch', 'log1p_Fare', 'log1p_Family'

    for col in ['Age', 'SibSp', 'Parch', 'Fare', 'Family']:
        df_one_hot['log1p_' + col] = np.log1p(df_one_hot[col])

    return df_one_hot


def survival_vs_gender(df):
    '''
    What is the survival rate for women and men?
    '''

    # ! Compute the survival rate of women and men. That is, compute the percentage of survived women and survived men.
    # ! Gender is specified in the "Sex" column.
    # ! You should - but do not have to - do it by defining a view of the DataFrame that includes, for example, only men, and then computing the average of "Survived"
    # ! For example:
    # ! df_male = df[df['Sex']=='male']
    # ! Now, compute the average of "Survived":
    # ! df_male["Survived"].mean()

    # ! your code here
    # ! Return the result in a dict or a series. Your keys for dict / index for Series should be the strings "male", "female"
    df_male = df[df['Sex'] == 'male']
    df_female = df[df['Sex'] == 'female']
    survived_by_gender = {"male": df_male["Survived"].mean(), "female": df_female["Survived"].mean()}

    print(survived_by_gender)

    return survived_by_gender


def survival_vs_class(df):
    # ! your code here
    # ! Return the result in a dict or a series. Your keys for dict / index for Series should be the strings "Cls_1", "Cls_2", "Cls_3"
    # For instance: survived_by_class = {"Cls_1": .25, "Cls_2": .35, "Cls_3": .45}
    df_class_1 = df[df['Cls_1'] == 1]
    df_class_2 = df[df['Cls_2'] == 1]
    df_class_3 = df[df['Cls_3'] == 1]

    survived_by_class = {"Cls_1": df_class_1["Survived"].mean(), "Cls_2": df_class_2["Survived"].mean(),
                         "Cls_3": df_class_3["Survived"].mean()}
    print(survived_by_class)

    return survived_by_class


def survival_vs_family(df):
    '''
    The different family size metrics - "SibSp", "Parch", "Family" are all numeric.
    '''

    survived_by_family = {}

    for metric in ["SibSp", "Parch", "Family"]:
        # ! your code here
        values = df[metric].unique()
        survived_by_metric = {value: df[df[metric] == value]["Survived"].mean() for value in values}

        # Example for survived_by_metric:
        # survived_by_metric = {0: 0.2, 1: 0.3, 2: 0.35, 4: 0.5...}
        # here the keys are unique values of each metric, and the values are the survival probability.
        # So in this example, we got 4 unique values for the metric - 0,1,2,4 , and the corresponding survival probabilities are 0.2, 0.3, 0.35, 0.5

        print("Family metric: ", metric)
        print("Survival stats:")
        print(survived_by_metric)

        survived_by_family[metric] = survived_by_metric

        # ! What survival metric with what value ensures the highest probability of survival?
        # ! Complete the following print statement after inspecting the reuslts

        # ! your code here
    max_metric = max(survived_by_family, key=lambda x: survived_by_family[x][2])
    max_probability = max(survived_by_family[max_metric].keys(), key=lambda x: survived_by_family[max_metric][x])
    print("To ensure the highest chance of survival, the metric ", max_metric,
          " must have the value ", max_probability)

    return survived_by_family


def survival_vs_age(df: pd.DataFrame):
    '''
    Here we would like to plot some histograms.
    Some very basic plotting: run these three commands:

    plt.plot(np.arange(10))
    plt.plot(np.arange(10)**.5)
    plt.plot(np.arange(10)**2)

    You should get 3 lines on a single figure. While that is a desirable functionality, things can quickly go out of hand if you do not close or clear your figures.

    To prevent clogging your figures with clutter, you can do one of several things:

    1. put:
    plt.close('all')
    at the beginning of this function. This will close all figures, all subsequent plots will be "new"

    2. Naming your figures and closing / clearing them before the first plot in the function.

    2.1. Closing:

    plt.close('abc') # closes figure "abc", no error raised if it does not exist.
    plt.figure('abc') # opens a brand, empy figure named "abc"
    plt.plot(...)
    df[...].hist()

    2.1. clearing:

    Here the order is reversed

    plt.figure('abc') # makes "abc" the active figure, makes a new figure named "abc" if it does not exist
    plt.clear('abc') # clears the figure "abc", leaving it empty and active to recieve plots
    plt.plot(...)
    df[...].hist()


    Now, back to age histogram (distributions)
    First, define the histogram edges

    The following is a suggestion, the choice is up to you (will not affect the grade except for a really bad case, like bins = [0,100])
    '''
    bins = list(range(0, 100, 4))
    '''
    We can plot a histogram of any column of numerical values by the "hist" method of DataFrame
    '''

    plt.close('Age, all')
    plt.figure('Age, all')
    # df['Age'].hist(bins=bins)

    '''
    Note, you can also put: bins = 'auto'
    df['Age'].hist(bins='auto')

    Try it! 

    '''

    # ! your code here
    # ! plot 2 histograms of age: one for those who survived, and one for those that did not
    # ! Bonus 1: plot 4 histograms of age: for women that survived and not, and for men tat survived and not
    # ! Bonus 2: plot 6 histograms of age: for survivors and casualties of each of the 3 classes
    survived = df[df['Survived'] == 1]
    died = df[df['Survived'] == 0]
    died['Age'].hist(bins=bins)
    survived['Age'].hist(bins=bins)
    plt.legend(['Died', 'Survived'])
    plt.show()

    return


## 3.5 Correlation of survival to the numerical variables
# ['Age', 'SibSp', 'Parch', 'Fare', 'Family']
# ['log1p_Age', 'log1p_SibSp', 'log1p_Parch', 'log1p_Fare', 'log1p_Family']
def survival_correlations(df: pd.DataFrame):
    '''
    We can compute the correlation of the various numeric columns to survival. This is done by the corr function of DataFrame.

    '''

    corr = df.corr()

    # corr is a DataFrame that represents the correlatio matrix
    print(corr)

    # we need only the correlation to the "Survived" column. Also, we don't need the correlation of "Survived" to itself.
    # Also, remember, that for inspection purposes, it is the *absolute value* of correlation that's important

    # ! your code here
    # ! find the 5 most important numerical columns, and print (with sign) and return their correlation. Use dict or Series
    # important_feats = ...
    # important_corrs = {'a': 0.9, 'b': -0.8, ...}
    corr = corr['Survived'].drop('Survived', axis=0)
    abs_corr = abs(corr)
    important_feats = abs_corr.nlargest(5).index
    important_corrs = {feat: corr[feat] for feat in important_feats}
    print(important_corrs)

    return important_corrs


## 4.1 split data into train and test sets
def split_data(df_one_hot):
    from sklearn.model_selection import train_test_split

    Y = df_one_hot['Survived']
    X = df_one_hot.drop(['Survived'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1, stratify=Y)

    # This splits the data into a train set, which will be used to calibrate the internal parameters of predictor, and the test set, which will be used for checking

    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)

    return X_train, X_test, y_train, y_test


## 4.2 Training and testing!
def train_logistic_regression(X_train, X_test, y_train, y_test):
    from sklearn.model_selection import GridSearchCV
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

    para_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 50],  # internal regularization parameter of LogisticRegression
                 'solver': ['sag', 'saga']}

    Logit1 = GridSearchCV(LogisticRegression(penalty='l2', random_state=1), para_grid, cv=5)

    Logit1.fit(X_train, y_train)

    y_test_logistic = Logit1.predict(X_test)

    '''
    look at:
    https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

    to interpret y_test_logistic


    Now let's see how good our model is. Compute, print and return the following three performance measures, as taught in class:

    1. Confusion matrix
    2. Accuracy
    3. F1 score

    For that, in sklearn.metrics look at:
    1. sklearn.metrics.confusion_matrix
    2. sklearn.metrics.accuracy_score
    3. sklearn.metrics.f1_score


    '''

    # ! your code here
    conf_matrix = confusion_matrix(y_test, y_test_logistic)
    accuracy = accuracy_score(y_test, y_test_logistic)
    f1_score = f1_score(y_test, y_test_logistic)

    print('acc: ', accuracy, 'f1: ', f1_score)
    print('confusion matrix:\n', conf_matrix)

    return accuracy, f1_score, conf_matrix


if __name__ == "__main__":
    df_train = load_train_data()
    # disp_some_data(df_train)
    # display_column_data(df_train)
    df_lean = drop_non_inform_columns(df_train)
    # where_are_the_nans(df_lean)
    df_filled = fill_titanic_nas(df_lean)
    df_one_hot = encode_one_hot(df_filled)
    df_one_hot = make_family(df_one_hot)
    df_one_hot = add_log1p(df_one_hot)
    # survival_vs_gender(df_filled)
    # survival_vs_class(df_one_hot)
    # survival_vs_family(df_one_hot)
    # survival_vs_age(df_one_hot)
    survival_correlations(df_one_hot)
    X_train, X_test, y_train, y_test = split_data(df_one_hot)
    train_logistic_regression(X_train, X_test, y_train, y_test)
