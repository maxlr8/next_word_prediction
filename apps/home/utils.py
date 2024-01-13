# Home.utils.py
import re 
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import ast

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def bar_chart(data, column_name, title_text, colorSheme='Tealgrn', top_n=20):
    print(column_name=='predicted' and type(data['predicted'][0]) == str)
    if column_name=='predicted' and type(data['predicted'][0]) == str:
        data['predicted'] = data['predicted'].apply(lambda x: ast.literal_eval(x))
    
    if type(data[column_name][0]) == list:
        df_predictions = data[column_name].explode(column_name).value_counts().rename_axis('words').reset_index(name='counts')
    else:
        df_predictions = data[column_name].value_counts().rename_axis('words').reset_index(name='counts')
    df_predictions = df_predictions.loc[df_predictions['words'] != 'None']
    fig = px.bar(df_predictions[:top_n], x = "words", y = "counts", title = title_text, color='counts', color_continuous_scale=colorSheme)
    return fig

def get_pie_chart(labels,counts):

    fig = px.pie(names=labels, values=counts, hole=0.5, title='How Useful Our Predictions Are', color_discrete_sequence=px.colors.sequential.RdBu)

    return fig


def past_activity_plot(data):

  fig = px.bar(data, x='days', y='predictions', title='Past 7 days activity', color='predictions', color_continuous_scale='Peach')

  return fig