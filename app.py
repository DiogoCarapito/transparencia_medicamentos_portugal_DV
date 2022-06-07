import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

## CSV para o pie chart
path = ''
df = pd.DataFrame(data=pd.read_csv(path + 'registo__doença_cardiaca.csv'))

## CSV para o bar chart 1
df_bar_chart = pd.DataFrame(data=pd.read_csv(path + 'bar_chart_dummy.csv'))

## CSV para o bar chart 1
path = ''
df_bar_chart = pd.DataFrame(data=pd.read_csv(path + 'bar_chart_dummy.csv'))

radio_options_fumadores = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Não Fumadores', 'value': 'n_fumadores'},
    {'label': 'Fumadores', 'value': 'fumadores'}
]

dropdown_ars_barchart_1 = [
    {'label': 'Norte', 'value': 'norte'},
    {'label': 'Centro', 'value': 'centro'},
    {'label': 'LVT', 'value': 'lvt'},
    {'label': 'Alentejo', 'value': 'alentejo'},
    {'label': 'Algarve', 'value': 'algarve'},
]

## aqui o value tem que ser em integer porque aparentemente a exctração do CSV inicial interpreta os valores numéricos como integer, e para a logica lá em baixo funcionar tem que cuspir um inteiro e não um texto, ou então teria de necessitar de uma reconversão str par int
dropdown_ars_barchart_2 = [
    {'label': '2017', 'value': 2017},
    {'label': '2018', 'value': 2018},
    {'label': '2019', 'value': 2019},
    {'label': '2020', 'value': 2020},
    {'label': '2021', 'value': 2021},
]

app = Dash(__name__)

## HTML em dash
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2('Medicamentos - Portal da Transparência')
            ],style={'width':'79%','position': 'center'}
        ),
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('logo.png'),style={'width': '60px', 'position': 'center'})
            ], id='logo')
        ],style={'width':'25%'}),
    ],className='row container', style={'display': 'flex'}),

    html.Div([
        html.Div([
            html.H3('Explicação sobre o trabalho de DV'),
            html.Label('Explicações nevessárias sobre vários motivos e razões relativa a situações variadas e essenciais para uma boa relação entre as difrentes consistências ')
        ], className='row'),
    ]),
    html.Br(),
    html.Div([
        html.Div([
            html.H3('Analise doentes cardiacos, todos, fumadores e não fumadores')
        ], className='row', style={'display': 'flex','text-align': 'center'}),
        html.Div([
            html.Div([
                html.H3('Filtros:'),
                dcc.RadioItems(
                    id='radio_filtro_fumadores',
                    options=radio_options_fumadores,
                    value='todos'
                )
            ], className='col2 ', style={'text-align': 'left','width':'19%','float': 'left'}),
            html.Div([
                dcc.Graph(id='pie_graph'),
            ], className='col2', style={'width':'80%','float':'right'}),
        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([
            html.H3('Gastos medicmaentos por ARS entre 2017 e 2021 texto grande so para testar coisas ')
        ], className='row', style={'display': 'flex','text-align': 'center'}),
        html.Br(),
        html.Div([
            html.Div([
                html.H3('Filtros:'),
                dcc.Dropdown(
                    id='dropdown_ars_barchart_1',
                    options=dropdown_ars_barchart_1,
                    value='norte'
                ),
                html.Br(),
                dcc.Dropdown(
                    id='dropdown_ars_barchart_2',
                    options=dropdown_ars_barchart_2,
                    value=2021
                )
            ], className='col2 ', style={'text-align': 'left','width':'19%','float': 'left'}),
            html.Div([
                dcc.Graph(id='bar_chart_1'),

            ], className='col2', style={'width':'40%','float':'center'}),
            html.Div([
                dcc.Graph(id='bar_chart_2'),
            ], className='col2', style={'width':'40%','float':'right'}),
        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([
            html.H3('Gastos medicmaentos por ARS entre 2017 e 2021 texto grande so para testar coisas ')
        ], className='row', style={'display': 'flex','text-align': 'center'}),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Graph(id='line_chart_1'),
            ]),
        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

])

@app.callback(
    Output("pie_graph", "figure"),
    Output("bar_chart_1", "figure"),
    Output("bar_chart_2", "figure"),
    Output("line_chart_1", "figure"),
    Input("radio_filtro_fumadores", "value"),
    Input("dropdown_ars_barchart_1", "value"),
    Input("dropdown_ars_barchart_2", "value")
)

def generate_chart(radio_filtro_fumadores,dropdown_ars_barchart_1,dropdown_ars_barchart_2):

    ## filtro so para ter um dataframe com as colunas de HD e smoking através da função .groupby()
    ## https://www.geeksforgeeks.org/pandas-groupby/
    tabela_freq = df.groupby(['HeartDisease', 'Smoking']).size().unstack()

    ## logica para funcionamento do pie chart, filtro com logica booleana para
    if radio_filtro_fumadores == 'todos':
        sem_dc = tabela_freq.loc['No']['No'] + tabela_freq.loc['No']['Yes']
        com_dc = tabela_freq.loc['Yes']['No'] + tabela_freq.loc['Yes']['Yes']
    if radio_filtro_fumadores == 'n_fumadores':
        sem_dc = tabela_freq.loc['No']['No']
        com_dc = tabela_freq.loc['Yes']['No']
    elif radio_filtro_fumadores == 'fumadores':
        sem_dc = tabela_freq.loc['No']['Yes']
        com_dc = tabela_freq.loc['Yes']['Yes']

    df_contagens = pd.DataFrame(data={'categoria': ['Sem DC', 'Com DC'], 'numero': [sem_dc, com_dc]})
    pie_chart = go.Figure(
        data=[go.Pie(labels=df_contagens['categoria'], values=df_contagens['numero'], textinfo='label+percent',
                     insidetextorientation='horizontal',showlegend=False)])

    # barchart_1
    ## filtro aplicado com a função .loc[] com logica para ter apenas dados da ars selecionada no dropdown menu correspondente
    table_barchart_1 = df_bar_chart.loc[df_bar_chart['ars'] == dropdown_ars_barchart_1]

    layout_bar_1 = dict(title=dict(text='Gastros entre 2017 e 2021'),
                      yaxis=dict(title='Gastos em milhões de €'),
                      xaxis=dict(title='Ano'),
                      paper_bgcolor='#f9f9f9'
                      )
    bar_chart_1 = go.Figure(data=[go.Bar(x=table_barchart_1['ano'], y=table_barchart_1['gasto_medicamentos'])],
                            layout=layout_bar_1,
                            layout_yaxis_range=[0,max(df_bar_chart['gasto_medicamentos'])])

    # barchart_2
    ## filtro aplicado com a função .loc[] com logica para ter apenas dados do ano selecionado no dropdown menu correspondente
    table_barchart_2 = df_bar_chart.loc[df_bar_chart['ano'] == dropdown_ars_barchart_2]

    layout_bar_2 = dict(title=dict(text='Gastros por ARS'),
                        yaxis=dict(title='Gastos em milhões de €'),
                        xaxis=dict(title='ARS'),
                        paper_bgcolor='#FFFFFF'
                        )
    bar_chart_2 = go.Figure(data=[go.Bar(x=table_barchart_2['ars'], y=table_barchart_2['gasto_medicamentos'])],
                            layout=layout_bar_2,
                            layout_yaxis_range=[0, max(df_bar_chart['gasto_medicamentos'])])

    # line_chart_1
    ## https://plotly.com/python/line-charts/

    ## ordenar o dataframe por ordem descendente de gastos para a legenda ficar bem
    ## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    df_bar_chart_sorted = df_bar_chart.sort_values(by='gasto_medicamentos', ascending=False)

    ## a partir do dataframe original, saber qual é a lista de ARSs (.tolist) e remover os duplicados (.fromkeys)
    ## https://www.geeksforgeeks.org/get-a-list-of-a-particular-column-values-of-a-pandas-dataframe/
    ## https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    lista_de_arss = df_bar_chart_sorted['ars'].tolist()
    lista_de_arss = list(dict.fromkeys(lista_de_arss))
    line_chart_1 = go.Figure()

    ## loop para percorrer cada uma das ARSs e desenhar a linha correspondente
    ## https://plotly.com/python/line-charts/
    for ars in lista_de_arss:

        ## codigo para filtrar (*.loc[*] == *)por ARS ao longo da lista de ars e alicação a uma linha no linechart
        gastos_por_ars = df_bar_chart.loc[df_bar_chart['ars']==ars]

        ## parte que adiciona cada uma das linhas
        line_chart_1.add_trace(go.Scatter(x=gastos_por_ars['ano'],
                                          y=gastos_por_ars['gasto_medicamentos'],
                                          mode='lines+markers',
                                          name=ars,
                                          line_shape='spline'))

    line_chart_1.update_layout(title='Evolução dos gastos entre 2017 e 2021',
                      xaxis_title='Anos',
                      yaxis_title='Gastos em milhões de €',
                      paper_bgcolor = '#FFFFFF')


    ## Execução dos diferentes gráficos
    return pie_chart, \
           bar_chart_1, \
           bar_chart_2, \
           line_chart_1

## linha necessária par execuar a app
if __name__ == '__main__':
    app.run_server(debug=True)