# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from matplotlib.pyplot import title
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# initialize app
app = Dash(__name__)

# set theme
colors = {
    'background': '#9BB6AA',
    'text': '#FFFFFF'
}

fonts = {
    'paragraph': 'Geneva'
}


# load data
df = pd.read_csv("app_data.csv")

# set header
page_title = 'Mental Health in the Workplace'

intro_text = 'Do employees feel their mental health is supported in the workplace? That is the question we are seeking to answer using data leveraged from the organization Open Sourcing Mental Health (OSMI). View some of our analysis and insights below.'

# respondent demographic plots

# age
# drop NaNs
df_drop = df.dropna(subset=['age'], inplace=True)

# bucket gender values
age_conds = [
        df.age.lt(20),
        df.age.between(20, 29),
        df.age.between(30, 39),
        df.age.between(40, 49),
        df.age.between(50, 59),
        df.age.between(60, 69),
        df.age.between(70, 79),
        df.age.between(80, 89),
        df.age.ge(90)
]

age_cats = ["less then 20 years old", "20-29 years old", "30-39 years old", "40-49 years old",
            "50-59 years old", "60-69 years old", "70-79 years old", "80-89 years old", 
            "90+ years old"]

df['age_group'] = np.select(age_conds, age_cats)

age_group_value_counts = df.age_group.value_counts()
age_donut = go.Figure(data=go.Pie(values=age_group_value_counts,
                                     labels=age_group_value_counts.index, hole=0.4))
age_donut.update_layout(
    title_text='Age Groups',
    title_x=0.5,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

# gender
gender_value_counts = df.gender.value_counts()
gender_donut = go.Figure(data=go.Pie(values=gender_value_counts,
                                     labels=gender_value_counts.index, hole=0.4))
gender_donut.update_layout(
    title_text='Gender Value Counts',
    title_x=0.5,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

# set up app front end structure
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children=page_title,
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': fonts['paragraph']
        }
    ),

    html.Div(children=intro_text, style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': fonts['paragraph']
    }),

    html.Div(
        dcc.Graph(id='age_donut', figure=age_donut)
    ), 
    html.Div(
        dcc.Graph(id='gender_donut', figure=gender_donut)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
