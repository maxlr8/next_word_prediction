
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import itertools
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

# from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import re
from apps.nwp.models import NWP
from django.contrib.auth.models import User
# Create your views here.
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from apps.home.utils import bar_chart, get_pie_chart,past_activity_plot
from datetime import date, timedelta

startdate = date.today() - timedelta(days=6)
enddate = date.today()+ timedelta(days=1)

@login_required(login_url="/login/")
@api_view(['GET'])
def index(request):
    #overall_data = pd.DataFrame(list(NWP.objects.all().values()))
    user_data = pd.DataFrame(list(NWP.objects.filter(user__username=request.user).values()))
    if 'sentence' not in user_data:
        user_data['sentence'] = ''
    sents = list(user_data.sentence.apply(lambda l: l.split()))
    user_sents_len = len(list(itertools.chain(*sents)))
    try:
        range_user_data = pd.DataFrame(list(NWP.objects.filter(user__username=request.user,created__range=[startdate, enddate]).values()))
        today_user_data =  pd.DataFrame(list(NWP.objects.filter(user__username=request.user,created__day=str(date.today().day)).values()))
    except Exception as e:
        print(str(e))
        range_user_data = pd.DataFrame()
        today_user_data = pd.DataFrame()
    
    context = {}
    if len(range_user_data) > 0:
        range_user_data.created = range_user_data.created.apply(lambda l: l.day)
        range_user_data = range_user_data.groupby('created').size().rename_axis('days').reset_index(name='predictions')
        bar_fig_3 = past_activity_plot(range_user_data)
        bar_plot_3 = bar_fig_3.to_html(full_html=False, include_plotlyjs='cdn')
        context['plot4'] = bar_plot_3
    if len(user_data) < 1:
        html_template = loader.get_template('home/welcome.html')
        context={}
        return HttpResponse(html_template.render(context, request))
    context['n_user_preds'] = len(user_data)
    context['n_user_today_preds'] = len(today_user_data)
    context['user_sents_len'] = user_sents_len
    if 'selected' not in user_data:
        user_data['selected'] = None
    
    data_len = len(user_data)
    ignored = user_data.selected.isna().sum()
    selected_none = user_data.selected.str.fullmatch('None').sum()
    selected_predictions = data_len-(ignored+selected_none)
    labels = ['Selected Prediction','Selected None', 'Ignored']
    pie_fig = get_pie_chart(labels,[selected_predictions,selected_none,ignored])

    bar_fig = bar_chart(user_data,'predicted', 'Top Words We Predicted For You')
    bar_fig_2 = bar_chart(user_data, 'selected', 'Words You Selected the Most from Predictions','Purpor')
    # bar_plot_ = plot(bar_fig,output_type="div")
    bar_plot_ = bar_fig.to_html(full_html=False, include_plotlyjs='cdn')
    bar_plot_2 = bar_fig_2.to_html(full_html=False, include_plotlyjs='cdn')
    pie_plot_ = pie_fig.to_html(full_html=False, include_plotlyjs='cdn')
    context['plot1'] = bar_plot_
    context['plot2'] = pie_plot_
    context['plot3'] = bar_plot_2
    # context={'plot1':bar_plot_, 'plot2':pie_plot_, 'plot3':bar_plot_2}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
# def (request):
#     context = {'segment': 'index'}

#     html_template = loader.get_template('home/index.html')
#     return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
