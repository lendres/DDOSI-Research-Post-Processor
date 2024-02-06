import pandas as pd

# Example 1 - changing the data type.
df = pd.DataFrame(dict(column1=[1,2,3,4], column2=[1,2,3,4]))
df["column1"].attrs['name'] = 'hello'

print("\nExample 1 before:")
print(df)
print("Column1 attributes:", df["column1"].attrs)

# Changing the data type of the DataFrame drops the series attributes.
df1 = df.astype(float)
print("\nAfter type change:")
print(df1)
print("Column1 attributes:", df1["column1"].attrs)


# Example 2 - assignment to a DataFrame.
df = pd.DataFrame(dict(column1=[1,2,3,4], column2=[1,2,3,4]))
df["column1"].attrs['name'] = 'hello1'
df["column2"].attrs['name'] = 'hello2'

print("\n\n\nExample 2 before:")
print(df)
print("Column1 attributes:", df["column1"].attrs)
print("Column2 attributes:", df["column2"].attrs)

# Assigning a column to the DataFrame drops the attributes from the Series in DataFrame.
df["column1"] = df["column1"] + 5
print("\nAfter assignment to DataFrame:")
print(df)
print("Column1 attributes:", df["column1"].attrs)
print("Column2 attributes:", df["column2"].attrs)