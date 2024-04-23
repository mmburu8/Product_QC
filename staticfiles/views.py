# myapp/views.py
from django.shortcuts import render, redirect
from .forms import MyModelForm
import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import io
import base64
from .models import MyModel
from datetime import datetime
from django.templatetags.static import static
import webcolors

# Define the URL of the Google Font
google_font_url = 'https://fonts.googleapis.com/css2?family=Protest+Riot'

# Import necessary libraries for font handling
import matplotlib.font_manager as fm

font_path = "Protest_Riot/ProtestRiot-Regular.ttf"
prop = fm.FontProperties(fname=font_path)
prop.set_size(30)
# dictionary with font specifics
#font_spec = {"family": prop, "size": 25}
# Read the font file from the url
#font_data = urllib.request.urlopen(google_font_url).read()

# Register the Google Font using its URL
#prop = fm.FontProperties(fname=font_data)

# Define the font properties for the title                                                                                                                                                                       
# too much

# home function
def home(request):
    return render(request, 'home.html')

def data_entry(request):
    if request.method == 'POST':
        # Extract data from the form
        date = request.POST.get("date")
        total_products = request.POST.get("total_products") 
        defect_products = request.POST.get("defect_products")
        passed_products = request.POST.get("passed_products")
        products_returned = request.POST.get("products_returned")
        customer_compliants = request.POST.get("customer_compliants")
        # create new instance of MyModel
        data_to_add = MyModel(
            date=date,
            total_products=total_products,
            defect_products=defect_products,
            passed_products=passed_products,
            products_returned=products_returned,
            customer_compliants=customer_compliants
        )
        data_to_add.save()
        return print("success")
    return render(request, 'data_entryDEUX.html')

from django.templatetags.static import static

def my_view(request):
    image_url = static('sneaker 6.jpg')
    image_static = static("splash 123.jpg")
    # Use image_url in your view logic

def select_attributes(request):
    if request.method == "POST":
        # process form data
        a_attribute = request.POST.get('aattribute')
        b_attribute = request.POST.get("battribute")


        # fetch data
        queryset = MyModel.objects.all()
        # convert queryset to pandas dataframe
        product = pd.DataFrame.from_records(queryset.values())

        # select column values that will be used for visualization
        selCol = product[[a_attribute, b_attribute]] 
        # pass dataframe as part of the context
        context = {'dataframe': selCol.to_html(classes='table table-striped')}

        return render(request, "display data.html", context)
    else:
        return render(request, 'column choice.html')
    
def process_data(start_dt, end_dt):
    # fetch data
    queryset = MyModel.objects.all()
    # convert queryset to pandas dataframe
    product = pd.DataFrame.from_records(queryset.values())

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
    # convert string to datetime datatype
    start_dtf = datetime.strptime(start_dt, "%d-%m-%Y")
    end_dtf = datetime.strptime(end_dt, "%d-%m-%Y")

    filt_product = product[(product['date'] >= start_dtf) & (product['date'] <= end_dtf)]


    return filt_product

def attribute_trainer(request):
    if request.method == "POST":
        list_attr = request.POST.getlist("aattributes")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        products = process_data(start_date, end_date)
        # get copy of list_attr
        selAttributes = list_attr.copy()
        # Dictionary with {database column values: real values}
        model_dict = {"date": "Date", "total_products": "Total Products", "passed_products": "Passed Products",
                    "products_returned": "Returned Products", "customer_compliants": "Customer Complaints",
                    "defect_products": "Defected Products"}
        # title dictionary
        title_dict = {"defect_products": "Defect Product Rate", "products_returned": "Returned Products Rate", 
                        "customer_compliants": "Customer Compliants Rate", "passed_products": "Passed Products Rate",
                        "total products": "Total Products Rate"}
        # list of color combinations
        mult_col = [['magenta', 'lawngreen'], ['mediumblue', 'mediumvioletred'], ['blue', 'gold'],
                        ['deepskyblue', 'orangered'], ['darkorange', 'yellow']]
        # Dict with labels
        label_dict = {"total_products": "total", "passed_products": "passed", "defect_products": "defected",
                          "products_returned":"returned", "customer_compliants": "complaints"} 
        if 'total_products' in selAttributes:
            selAttributes.remove("total_products")
            # returned and total products
            #rt_list = [label_dict[selAttributes[0]] for i in range(len(products['siku']))]
            return_df = products[["siku", selAttributes[0]]]    
            return_df['Product'] = label_dict[selAttributes[0]]
            return_df.columns = ["siku", "Number", "Product"]
            # total products
            #rt_list = ["total" for i in range(len(products['siku']))]
            total_df = products[["siku", "total_products"]]
            total_df['Product'] = "total"
            total_df.columns = ["siku", "Number", "Product"]
            # get the rate values
            return_df['Rate'] = (return_df['Number'] / total_df['Number']) * 100
            return_df['Rate'] = return_df['Rate'].round(2).values.astype(str)
            return_df['Rate'] = [str(rate) + "%" for rate in return_df["Rate"]]
            total_df['Rate'] = " "
            # concatenate dataframe
            viz_df = pd.concat([return_df, total_df], axis=0)
            viz_df.reset_index(drop=True, inplace=True)
            # create an array of colors
            colors = random.choice(mult_col)
            sns.set_palette(sns.color_palette(colors))
            # figsize
            plt.figure(figsize=(products.shape[0],5))
            ax = sns.barplot(x="siku", y="Number", hue="Product", data=viz_df)
            for value, p in zip(viz_df['Rate'],ax.patches):
                width, height = p.get_width(), p.get_height()
                x, y = p.get_xy()
                ax.text(x + width / 2, y + height  + 0.4, str(value), ha='center', va='bottom')
                plt.title("Returned Products Rate", fontproperties=prop, pad=20)
                plt.xlabel("Months")
                plt.legend()
        #plt.gcf().set_facecolor('none') DRIVEN bru
        # save plot to a BytesIO object
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        # encode the image as base64
        image_base64 = base64.b64encode(image_stream.read()).decode("utf-8")

        # get data for html table
        # add date to list_attr list
        list_attr.insert(0, "date")
        # sort values
        #products['date'] = pd.to_datetime(products['date'])
        #products.sort_values(by="date", ascending=False, inplace=False)
        # collect data by column names
        products.reset_index(drop=True, inplace=True)
        products.sort_values(by="date", ascending=False, inplace=True)
        prod_html = products.loc[:5, list_attr]
        # column names
        col_values= [model_dict[la] for la in list_attr]
        prod_html.columns = col_values
        # save to html
        html_table = prod_html.to_html(index=False, classes="custom-table", border=0)

        # pipeline to transfer color chosen in backend to frontend
        # convert color name to RGB
        rgb_tuple = webcolors.name_to_rgb(colors[0])
        # convert RGB to CSS RGB format
        css_color = 'rgb({}, {}, {})'.format(*rgb_tuple)

        # pass the base64-encoded image to the templates
        return render(request, "display data.html", {'image_base64': image_base64,  
                                                     "title_elem": title_dict[selAttributes[0]], "html_table": html_table,
                                                     "col_show": css_color})
# Big man ting, frosinone, bologna, stable, bar mit, FLY, one direction, dripped out, tripster,sevila, australia
    else:
        return render(request, 'sample deux.html')
     
def visualize_data(request):
    if request.method == "POST":
        list_attr = request.POST.getlist("aattributes")
        # get a copy of list_attr
        selAttributes = list_attr.copy()
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        products = process_data(start_date, end_date)
        # Dictionary with {database column values: real values}
        model_dict = {"date": "Date", "total_products": "Total Products", "passed_ rteproducts": "Passed Products",
                    "products_returned": "Returned Products", "customer_compliants": "Customer Complaints",
                    "defect_products": "Defected Products"}
        # title dictionary
        title_dict = {"defect_products": "Defect Product Rate", "products_returned": "Returned Products Rate", 
                        "customer_compliants": "Customer Compliants Rate", "passed_products": "Passed Products Rate",
                        "total products": "Total Products Rate"}
        # list of color combinations
        mult_col = [['magenta', 'lawngreen'], ['mediumblue', 'mediumvioletred'], ['blue', 'gold'],
                        ['deepskyblue', 'orangered'], ['darkorange', 'yellow']]
        # Dict with labels
        label_dict = {"total_products": "total", "passed_products": "passed", "defect_products": "defected",
                          "products_returned":"returned", "customer_compliants": "complaints"} 
        
    
        if len(selAttributes) == 1:
            # single color dict
            sinCol = {"total_products": "lightseagreen", "passed_products": "darkorange",
                    "products_returned": "fuchsia", "customer_compliants": "peru",
                    "defect_products": "crimson"
            }
            # line plots
            plt.figure(figsize=(products.shape[0],5))
            sns.lineplot(x='siku', y=selAttributes[0], data=products, linestyle='-',marker='o', markersize=8, color=sinCol[selAttributes[0]], drawstyle= "steps-post", label=model_dict[selAttributes[0]])
            plt.title(model_dict[selAttributes[0]], fontproperties=prop, pad=20)
            plt.xlabel("Months")
            plt.ylabel("Number")
            # pipeline to transfer color chosen in backend to frontend develop
            # convert color name to RGB
            rgb_tuple = webcolors.name_to_rgb(sinCol[selAttributes[0]])
            # convert RGB to CSS RGB format
            css_color = 'rgb({}, {}, {})'.format(*rgb_tuple)
        elif "passed_products" in selAttributes and "total_products" not in selAttributes:
            selAttributes.remove("passed_products")
            
            # Chosen title
            chosen = title_dict[selAttributes[0]]
            # options to get rate based on first attribute(passed rate)
            products[chosen] = (products[selAttributes[0]] / products['total_products']) * 100
            # have only 2 dp
            products[chosen] = products[chosen].round(2)

            # select color combination
            rand_col = random.choice(mult_col)
            # set background
            sns.set_theme(style='whitegrid')
            # bar chart bottom part
            plt.figure(figsize=(products.shape[0],5))
            bar2 = sns.barplot(x='siku', y='passed_products', data=products, color=rand_col[0], label="passed")
            # bar chart top part
            bar1 = sns.barplot(x='siku', y=selAttributes[0], data=products, color=rand_col[1], bottom=products['passed_products'], label=label_dict[selAttributes[0]])
            # add text annotation to each bar
            for patch, value, hgt_val in zip(bar2.patches, products[chosen], products[selAttributes[0]]):
                bar2.text(patch.get_x() + patch.get_width() / 2, patch.get_height() + hgt_val + 0.3, f'{value}%', ha='center', va='bottom')
            plt.title(title_dict[selAttributes[0]], fontproperties=prop, pad=20)
            plt.xlabel("Months")
            plt.ylabel("No. of Products")
            plt.legend()
            # pipeline to transfer color chosen in backend to frontend
            # convert color name to RGB
            rgb_tuple = webcolors.name_to_rgb(rand_col[0])
            # convert RGB to CSS RGB format
            css_color = 'rgb({}, {}, {})'.format(*rgb_tuple)
        elif 'total_products' in selAttributes:
            selAttributes.remove("total_products")
            # returned and total products
            #rt_list = [label_dict[selAttributes[0]] for i in range(len(products['siku']))]
            return_df = products[["siku", selAttributes[0]]]    
            return_df['Product'] = label_dict[selAttributes[0]]
            return_df.columns = ["siku", "Number", "Product"]
            # total products
            #rt_list = ["total" for i in range(len(products['siku']))]
            total_df = products[["siku", "total_products"]]
            total_df['Product'] = "total"
            total_df.columns = ["siku", "Number", "Product"]
            # get the rate value
            return_df['Rate'] = (return_df['Number'] / total_df['Number']) * 100
            return_df['Rate'] = return_df['Rate'].round(2).values.astype(str)
            return_df['Rate'] = [str(rate) + "%" for rate in return_df["Rate"]]
            total_df['Rate'] = " "
            # concatenate dataframe
            viz_df = pd.concat([return_df, total_df], axis=0)
            viz_df.reset_index(drop=True, inplace=True)
            # create an array of colors
            colors = random.choice(mult_col)
            sns.set_palette(sns.color_palette(colors))

            # figsize
            plt.figure(figsize=(products.shape[0],5))
            ax = sns.barplot(x="siku", y="Number", hue="Product", data=viz_df)
            for value, p in zip(viz_df['Rate'],ax.patches):
                width, height = p.get_width(), p.get_height()
                x, y = p.get_xy()
                ax.text(x + width / 2, y + height  + 0.4, str(value), ha='center', va='bottom')
                plt.title(title_dict[selAttributes[0]], fontproperties=prop, pad=20)
                plt.xlabel("Months")
                plt.legend()
            # pipeline to transfer color chosen in backend to frontend
            # convert color name to RGB
            rgb_tuple = webcolors.name_to_rgb(colors[0])
            # convert RGB to CSS RGB format
            css_color = 'rgb({}, {}, {})'.format(*rgb_tuple)
        # save plot to a BytesIO object
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        # encode the image as base64
        image_base64 = base64.b64encode(image_stream.read()).decode("utf-8")

        # get data for html table
        # add date to list_attr list
        list_attr.insert(0, "date")
        
        # collect data by column names
        products.reset_index(drop=True, inplace=True)
        products.sort_values(by="date", ascending=False, inplace=True)
        prod_html = products.loc[:5, list_attr]
        # column names
        col_values= [model_dict[la] for la in list_attr]
        prod_html.columns = col_values
        # save to html
        html_table = prod_html.to_html(index=False, classes="custom-table", border=0)
        # pass the base64-encoded image to the templates
        return render(request, "display data.html", {'image_base64': image_base64,  
                                                     "title_elem": title_dict[selAttributes[0]], "html_table": html_table,
                                                     "col_show": css_color})
    else:
        return render(request, 'sample deux.html')