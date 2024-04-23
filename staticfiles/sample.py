
import pandas as pd

from datetime import datetime

# read excel file
product = pd.read_excel("product qc.xlsx")

# preprocess data
product['date'] = pd.to_datetime(product['date'])

# sort the dataframe by 'date' column
product.sort_values(by='date', inplace=True)
product.reset_index(drop=True, inplace=True)
    
# split date column to month, year column.
product['month'] = product['date'].dt.month
product['year'] = product['date'].dt.year

product['month'] = product['month'].astype(str)
product['year'] = product['year'].astype(str)

# change month values
month_dct = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', 
             '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
product['month'] = product['month'].map(month_dct)

# concatenate two columns using .str.cat() method
product['siku'] = product['month'].str.cat(product['year'], sep=' ')

# filter dates
start_str = "14-09-2022"
end_str = "14-09-2023"

# convert string to datetime datatype
start_dtf = datetime.strptime(start_str, "%d-%m-%Y")
end_dtf = datetime.strptime(end_str, "%d-%m-%Y")

filt_product = product[(product['date'] >= start_dtf) & (product['date'] <= end_dtf)]
# Dict with labels
label_dict = {"total_products": "total", "passed_products": "passed", "defect_products": "defected",
                "products_returned":"returned", "customer_compliants": "complaints"} 
selAttributes = ["total_products", "products_returned"]
selAttributes.remove("total_products")
# returned and total products
rt_list = [label_dict[selAttributes[0]] for i in range(len(filt_product['siku']))]
return_df = filt_product[["siku", selAttributes[0]]]    
return_df['Product'] = rt_list
return_df.columns = ["siku", "Number", "Product"]
# total products
rt_list = ["total" for i in range(len(filt_product['siku']))]
total_df = filt_product[["siku", "total_products"]]
total_df['Product'] = rt_list
total_df.columns = ["siku", "Number", "Product"]
# get the rate value
return_df['Rate'] = (return_df['Number'] / total_df['Number']) * 100
return_df['Rate'] = return_df['Rate'].round(2).values.astype(str)
return_df['Rate'] = [return_df['Rate'][i] + "%" for i in range(len(return_df['Number']))]
total_df['Rate'] = " "
# concatenate dataframe
viz_df = pd.concat([return_df, total_df], axis=0)
viz_df.reset_index(drop=True, inplace=True)
print(viz_df.head(5))