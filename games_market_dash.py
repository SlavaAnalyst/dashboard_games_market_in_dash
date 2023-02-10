from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ____________________CLEANING DATA____________________
path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSKWg6_bEndzMnuCQ8ZWGrBTfsZfI9UM3ilmqeOO2-xZeRZSm54oeIkdxeiI_ZYCr7kEy1bE2RFmFD9/pub?gid=73997209&single=true&output=csv'
df = pd.read_csv(path)
df = df[df.Year_of_Release >= 2000]
df = df.dropna()
# User_Score = object
# df['User_Score'].astype('float')
# ValueError: could not convert string to float: 'tbd'
df = df[df.User_Score != 'tbd']
df['User_Score'] = df['User_Score'].astype('float')
df['Year_of_Release'] = df['Year_of_Release'].apply(lambda x: round(x))
df['Year_of_Release'] = pd.to_datetime(df['Year_of_Release'], format='%Y')
df = df.sort_values('Year_of_Release')

app = Dash(__name__,
           external_stylesheets=[dbc.themes.CERULEAN])

# ____________________BUILD GRAPHS____________________
area = df.groupby(['Year_of_Release', 'Platform']).Name.count().to_frame().reset_index().rename(
    columns={'Name': 'Количество игр'})
px_area = px.area(area, x='Year_of_Release', y='Количество игр', color='Platform')
px_scatter = px.scatter(df, x='Critic_Score', y='User_Score', color='Genre')

markdown_text = '''
## Развитие игровой индустрии с 2000 по 2016 годы

Назначения дашборда - отслеживание динамики выпуска игровый платформ и наблюдение за успешностью игры в зависимости от года релиза, жанра и рейтинга игры.
'''

# ____________________FILTERS____________________
# Фильтр года
date_filter = dcc.DatePickerRange(
    id='date_picker_range',
    min_date_allowed=df['Year_of_Release'].min(),
    max_date_allowed=df['Year_of_Release'].max(),
    start_date=df['Year_of_Release'].min(),
    end_date=df['Year_of_Release'].max(),
    display_format='YYYY'
)
# Фильтр жанра
Genre_filter = dcc.Dropdown(df.Genre.value_counts().index.to_list(),
                            df.Genre.value_counts().index.to_list(),
                            id='genre_dropdown',
                            multi=True
                            )
# Фильтр рейтинга
Rating_filter = dcc.Dropdown(df.Rating.value_counts().index.to_list(),
                             df.Rating.value_counts().index.to_list(),
                             id='rating_dropdown',
                             multi=True
                             )

# ____________________LAYOUT____________________
app.layout = html.Div(children=[

    # Заголовок
    dbc.Row([
        dcc.Markdown(markdown_text,
                     style={'margin-left': '40px', 'margin-top': '30px', 'margin-bottom': '10px'})
    ]),

    # Фильтр жанра
    dbc.Row([
        html.Div('Выберите жанр',
                 style={'text-align': 'center', 'color': '#555555'}),
        html.Div(Genre_filter)
    ],
        style={'margin-left': '115px', 'margin-bottom': '0px', 'margin-right': '115px'}
    ),

    # Фильтр года
    dbc.Row([
        dbc.Col([
            html.Div('Введите год (2000-2016)',
                     style={'text-align': 'center', 'color': '#555555'}),
            html.Div(date_filter,
                     style={'margin-left': '130px', 'margin-bottom': '10px', 'margin-right': '1px'})
        ],
            width=5
        ),

        # Фильтр рейтинга
        dbc.Col([
            html.Div('Выберите рейтинг',
                     style={'text-align': 'center', 'color': '#555555'}),
            html.Div(Rating_filter,
                     style={'margin-bottom': '10px', 'margin-left': '250px', 'margin-right': '130px'})
        ]
        )
    ], style={'margin-bottom': '30px'}),

    # График area и интерактивный текст
    dbc.Row([
        dbc.Col([
            html.Label(id="count_games",
                       style={'margin-left': '190px', 'font-size': 20}),
            html.Div([
                dcc.Graph(id="px_area", figure=px_area)
            ]),
        ], width=6
        ),

        # Фильтр рейтинга
        dbc.Col([
            html.Label("Оценки игроков и критиков по жанру",
                       style={'margin-left': '180px', 'margin-bottom': '20px',
                              'font-size': 20}),
            dcc.Graph(id="px_scatter", figure=px_scatter)
        ], width=6
        )
    ], style={'margin-bottom': '30px'}
    )
], style={'margin-left': '20px',
          'margin-right': '20px'}
)


# ____________________CALLBACK____________________
@app.callback(
    [
        Output(component_id='px_area', component_property='figure'),
        Output(component_id='px_scatter', component_property='figure'),
        Output(component_id='count_games', component_property='children')
    ],
    [
        Input(component_id='date_picker_range', component_property='start_date'),
        Input(component_id='date_picker_range', component_property='end_date'),
        Input(component_id='rating_dropdown', component_property='value'),
        Input(component_id='genre_dropdown', component_property='value')
    ]
)

def update_date(start_date, end_date, rating, genre):
    between_df = df[df['Year_of_Release'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))]
    df_full_filters = between_df.query('Rating == @rating and Genre == @genre')

    df_area = df_full_filters.groupby(['Year_of_Release', 'Platform']).Name.count().to_frame().reset_index().rename(
        columns={'Name': 'Количество игр'})
    px_area = px.area(df_area, x='Year_of_Release', y='Количество игр', color='Platform',
                      labels={"Platform": "", "Количество игр": "Количество игр",
                              "Year_of_Release": "Год релиза"}).update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'},
                                                                              margin=dict(l=0, r=0, t=20, b=30),
                                                                              legend_orientation="h")

    px_scatter = px.scatter(df_full_filters, x='Critic_Score', y='User_Score', color='Genre', opacity=0.75,
                            labels={"Genre": "", "User_Score": "Оценка игрока",
                                    "Critic_Score": "Оценка критика"}).update_layout(
        {'plot_bgcolor': 'rgba(0, 0, 0, 0)'},
        margin=dict(l=0, r=0, t=20, b=30))

    children = f'Количество выпущенных игр ({df_full_filters.Name.count()} шт)'
    return px_area, px_scatter, children

if __name__ == '__main__':
    app.run_server(debug=True, port=5004)  # port=8050
