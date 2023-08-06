from IPython import display
import pandas as pd
from matplotlib import pyplot as plt

def null(df,df_name):
    if df.isnull().values.any() ==False:
        print(f'STATUS: There is NO ANY null value in {df_name}')
    else:
        print('STATUS: There is null value in dataframe')
        columns = df.columns[df.isna().any()].tolist()
        temp = {}
        for column in columns:
            count = (len(df)) - (df[column].count())
            temp[column] = f"{count} ({round((count/len(df)), 4)*100}%)"
        print(f'STATUS: Nulls of {df_name} = {temp} of total {len(df)}')

def duplicate(df, column):
    if len(df[df[column].duplicated()]) ==0:
        print(f'STATUS: There is NO ANY duplicate value in the column of "{column}"')
    else:
        print(f'STATUS: There are {len(df[df[column].duplicated()])} duplicate values in the column of "{column}"')

def shape(df,df_name):
    print(f'STATUS: Dimension of "{df_name}" = {df.shape}')

def vc(df, column, r=False):
    vc_df = df.reset_index().groupby([column]).size().to_frame('count')
    vc_df['percentage (%)'] = vc_df['count'].div(sum(vc_df['count'])).mul(100)
    vc_df = vc_df.sort_values(by=['percentage (%)'], ascending=False)
    print(f'STATUS: Value counts of "{column}"...')
    display(vc_df)
    if r:
        return vc_df

def pie(df, column):
    (df[column].value_counts().plot(kind='pie' , autopct='%1.1f%%', title=f'Pie chart of "{column}"'))
    return plt.show()

def drop(df, column):
    df2 = df.drop(column, axis=1)
    print(f"STATUS: Columns of {column} were dropped")
    return df2

def dtype(df, column):
    print(f"STATUS: Data type of {column} = {df[column].dtypes}")

def unique(df, column, r =False):
    num = len(df[column].unique())
    print(f"STATUS: Unique value for {column} = {num}")
    if r:
        return num

def merge(df1 ,df2, column, df1_name=None, df2_name=None):
    if (df1[column].isnull().values.any() ==False) & (df2[column].isnull().values.any() ==False):
        if (df1_name == None) & (df2_name == None):
            if (len(df1[df1[column].duplicated()]) ==0) & (len(df2[df2[column].duplicated()]) ==0):
                print(f"STATUS: One-to-One Relationship Merging on '{column}'")
                df3 = df1.merge(df2, on=column, how='left')
            elif  (len(df1[df1[column].duplicated()]) !=0) & (len(df2[df2[column].duplicated()]) ==0):
                print(f"STATUS: Many-to-One Relationship Merging on '{column}'")
                df3 = df1.merge(df2, on=column, how='left')
            elif  (len(df1[df1[column].duplicated()]) ==0) & (len(df2[df2[column].duplicated()]) !=0):
                print(f"STATUS: One-to-Many Relationship Merging on '{column}'")
                df3 = df1.merge(df2, on=column, how='left')
            elif  (len(df1[df1[column].duplicated()]) !=0) & (len(df2[df2[column].duplicated()]) !=0):
                raise Exception(f"STATUS: Many-to-Many Relationship Merging, please check duplicates on '{column}'")
        else:
            if (len(df1[df1[column].duplicated()]) ==0) & (len(df2[df2[column].duplicated()]) ==0):
                print(f"STATUS: One-to-One Relationship '{df1_name}' left join '{df2_name}' on '{column}'")
                df3 = df1.merge(df2, on=column, how='left')
            elif  (len(df1[df1[column].duplicated()]) !=0) & (len(df2[df2[column].duplicated()]) ==0):
                print(f"STATUS: Many-to-One Relationship '{df1_name}' left join '{df2_name}' on '{column}'")
                df3 = df1.merge(df2, on=column, how='left')
            elif  (len(df1[df1[column].duplicated()]) ==0) & (len(df2[df2[column].duplicated()]) !=0):
                print(f"STATUS: One-to-Many Relationship '{df1_name}' left join '{df2_name}' on '{column}'")
                df3 = df1.merge(df2, on=column, how='left')
            elif  (len(df1[df1[column].duplicated()]) !=0) & (len(df2[df2[column].duplicated()]) !=0):
                raise Exception(f"STATUS: Many-to-Many Relationship Merging, please check duplicates on '{column}'")
        return df3
    else:
        raise Exception("STATUS: There is null values in the merging df")

def mergex(df1 ,df2, column1, column2, df1_name=None, df2_name=None):
    if (df1[column1].isnull().values.any() ==False) & (df2[column2].isnull().values.any() ==False):
        if (df1_name == None) & (df2_name == None):
            if (len(df1[df1[column1].duplicated()]) ==0) & (len(df2[df2[column2].duplicated()]) ==0):
                print(f"STATUS: One-to-One Relationship Merging on '{column1}' = '{column2}'")
                df3 = df1.merge(df2, left_on=column1, right_on=column2, how='left')
            elif  (len(df1[df1[column1].duplicated()]) !=0) & (len(df2[df2[column2].duplicated()]) ==0):
                print(f"STATUS: Many-to-One Relationship Merging on '{column1}' = '{column2}'")
                df3 = df1.merge(df2, left_on=column1, right_on=column2, how='left')
            elif  (len(df1[df1[column1].duplicated()]) ==0) & (len(df2[df2[column2].duplicated()]) !=0):
                print(f"STATUS: One-to-Many Relationship Merging on '{column1}' = '{column2}'")
                df3 = df1.merge(df2, left_on=column1, right_on=column2, how='left')
            elif  (len(df1[df1[column1].duplicated()]) !=0) & (len(df2[df2[column2].duplicated()]) !=0):
                raise Exception(f"STATUS: Many-to-Many Relationship Merging, please check duplicates on '{column1}' = '{column2}'")
        else:
            if (len(df1[df1[column1].duplicated()]) ==0) & (len(df2[df2[column2].duplicated()]) ==0):
                print(f"STATUS: One-to-One Relationship '{df1_name}' left join '{df2_name}' on '{column1}' = '{column2}")
                df3 = df1.merge(df2, left_on=column1, right_on=column2, how='left')
            elif  (len(df1[df1[column1].duplicated()]) !=0) & (len(df2[df2[column2].duplicated()]) ==0):
                print(f"STATUS: Many-to-One Relationship '{df1_name}' left join '{df2_name}' on '{column1}' = '{column2}")
                df3 = df1.merge(df2, left_on=column1, right_on=column2, how='left')
            elif  (len(df1[df1[column1].duplicated()]) ==0) & (len(df2[df2[column2].duplicated()]) !=0):
                print(f"STATUS: One-to-Many Relationship '{df1_name}' left join '{df2_name}' on '{column1}' = '{column2}")
                df3 = df1.merge(df2, left_on=column1, right_on=column2, how='left')
            elif  (len(df1[df1[column1].duplicated()]) !=0) & (len(df2[df2[column2].duplicated()]) !=0):
                raise Exception(f"STATUS: Many-to-Many Relationship Merging, please check duplicates on '{column1}' = '{column2}'")
        return df3
    else:
        raise Exception("STATUS: There is null values in the merging df")
        
def one_hot_encode(df, column):
    # Get one hot encoding of columns B
    one_hot = pd.get_dummies(df[column])
    # Drop column as it is now encoded
    df = df.drop(column,axis = 1)
    print(f"one hot encoded {column}")
    # Join the encoded df
    df = df.join(one_hot)
    return df