import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

path = 'databases/'
df_gasto_medicamentos_por_ano = pd.DataFrame(data=pd.read_csv(path + 'despesa-com-medicamentos-no-sns-por-ano.csv'))

path = 'databases/'
df_gasto_medicamentos = pd.DataFrame(data=pd.read_csv(path + 'despesa-com-medicamentos-no-sns-por-ano-por-regiao.csv'))

path = 'databases/'
df_treemap = pd.DataFrame(data=pd.read_csv(path + 'dispensa-de-medicamentos-por-grupo-farmacoterapeutico-por-ano-por-regiao.csv'))


path = ''
df_bar_chart = pd.DataFrame(data=pd.read_csv(path + 'bar_chart_dummy.csv'))

dropdown_ars_gasto_medicamentos_1 = [
    {'label': 'Nacional', 'value': 'nacional'},
    {'label': 'Norte', 'value': 'norte'},
    {'label': 'Centro', 'value': 'centro'},
    {'label': 'LVT', 'value': 'lvt'},
    {'label': 'Alentejo', 'value': 'alentejo'},
    {'label': 'Algarve', 'value': 'algarve'},
]

## aqui o value tem que ser em integer porque aparentemente a exctração do CSV inicial interpreta os valores numéricos como integer, e para a logica lá em baixo funcionar tem que cuspir um inteiro e não um texto, ou então teria de necessitar de uma reconversão str par int
dropdown_ars_gasto_medicamentos_2 = [
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
            html.H3('Gastos medicmaentos por ARS entre 2017 e 2021 texto grande so para testar coisas ')
        ], className='row', style={'display': 'flex','text-align': 'center'}),
        html.Br(),
        html.Div([
            html.Div([
                html.H3('Filtros:'),

                dcc.Dropdown(
                    id='dropdown_ars_gasto_medicamentos_1',
                    options=dropdown_ars_gasto_medicamentos_1,
                    value='nacional'
                ),

                html.Br(),

                dcc.Dropdown(
                    id='dropdown_ars_gasto_medicamentos_2',
                    options=dropdown_ars_gasto_medicamentos_2,
                    value=2021
                )

            ], className='col2 ', style={'text-align': 'left','width':'19%','float': 'left'}),
            html.Div([

                dcc.Graph(id='barchart_gasto_medicamentos_1'),

            ], className='col2', style={'width':'40%','float':'center'}),
            html.Div([

                dcc.Graph(id='barchart_gasto_medicamentos_2'),

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

            dcc.Graph(id='line_chart_1'),

        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([

            html.H3('considerações finais')

        ], className='row', style={'display': 'flex','text-align': 'center'}),
        html.Br(),
        html.Div([

            html.Label('tesxto bonito com as referencias')

        ], className='row', style={'display': 'flex','text-align': 'center'})
    ], className='row container', style={'display': 'block'}),
])

@app.callback(
    Output("barchart_gasto_medicamentos_1", "figure"),
    Output("barchart_gasto_medicamentos_2", "figure"),
    Output("line_chart_1", "figure"),
    Input("dropdown_ars_gasto_medicamentos_1", "value"),
    Input("dropdown_ars_gasto_medicamentos_2", "value")
)

def generate_chart(dropdown_ars_barchart_1,dropdown_ars_barchart_2,):

    # barchart_1
    ## filtro aplicado com a função .loc[] com logica para ter apenas dados da ars selecionada no dropdown menu correspondente
    if dropdown_ars_barchart_1 == 'nacional':
        gasto_medicamentos = df_gasto_medicamentos.loc[df_gasto_medicamentos['regiao'] == dropdown_ars_barchart_1]
    else:
        gasto_medicamentos = df_gasto_medicamentos_por_ano


    layout_bar_1 = dict(title=dict(text='Gastros entre 2017 e 2021'),
                      yaxis=dict(title='Gastos em milhões de €'),
                      xaxis=dict(title='Ano'),
                      paper_bgcolor='#f9f9f9'
                      )
    bar_chart_1 = go.Figure(data=[go.Bar(x=gasto_medicamentos['ano'], y=gasto_medicamentos['encargos_sns_ambulatorio'])],
                            layout=layout_bar_1,
                            )
    bar_chart_1.update_layout(barmode="relative")
    # layout_yaxis_range=[0,max(gasto_medicamentos['encargos_sns_ambulatorio'])]

    # barchart_2
    ## filtro aplicado com a função .loc[] com logica para ter apenas dados do ano selecionado no dropdown menu correspondente
    if dropdown_ars_barchart_1 == 'nacional':
        gasto_medicamentos = df_gasto_medicamentos.loc[df_gasto_medicamentos['regiao'] == dropdown_ars_barchart_1]
    else:
        gasto_medicamentos = df_gasto_medicamentos

    layout_bar_2 = dict(title=dict(text='evolução em percentagem'),
                        yaxis=dict(title='Gastos em milhões de €'),
                        xaxis=dict(title='Ano'),
                        paper_bgcolor='#FFFFFF'
                        )
    bar_chart_2 = go.Figure(data=[go.Bar(x=gasto_medicamentos['ano'], y=gasto_medicamentos['encargos_sns_ambulatorio'])],
                            layout=layout_bar_2,
                            )
    bar_chart_2.update_layout(barmode="relative")
    # layout_yaxis_range=[0, max(gasto_medicamentos['encargos_sns_ambulatorio'])]

    # line_chart_1
    ## https://plotly.com/python/line-charts/

    ## ordenar o dataframe por ordem descendente de gastos para a legenda ficar bem
    ## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    gasto_medicamentos_ambulatorio = df_gasto_medicamentos.sort_values(by='ano', ascending=False)

    ## a partir do dataframe original, saber qual é a lista de ARSs (.tolist) e remover os duplicados (.fromkeys)
    ## https://www.geeksforgeeks.org/get-a-list-of-a-particular-column-values-of-a-pandas-dataframe/
    ## https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    lista_de_regioes = gasto_medicamentos_ambulatorio['regiao'].tolist()
    lista_de_regioes = list(dict.fromkeys(lista_de_regioes))
    line_chart_1 = go.Figure()

    ## loop para percorrer cada uma das ARSs e desenhar a linha correspondente
    ## https://plotly.com/python/line-charts/
    for regiao in lista_de_regioes:

        ## codigo para filtrar (*.loc[*] == *)por ARS ao longo da lista de ars e alicação a uma linha no linechart
        gastos_por_regiao = gasto_medicamentos_ambulatorio.loc[gasto_medicamentos_ambulatorio['regiao']==regiao]

        ## parte que adiciona cada uma das linhas
        line_chart_1.add_trace(go.Scatter(x=gastos_por_regiao['ano'],
                                          y=gastos_por_regiao['encargos_sns_ambulatorio'],
                                          mode='lines+markers',
                                          name=regiao,
                                          line_shape='spline'))

    line_chart_1.update_layout(title='Evolução dos gastos entre 2017 e 2021',
                      xaxis_title='Anos',
                      yaxis_title='Gastos em milhões de €',
                      paper_bgcolor = '#FFFFFF')


    ## Execução dos diferentes gráficos

    return bar_chart_1, \
           bar_chart_2, \
           line_chart_1,


## linha necessária par execuar a app
if __name__ == '__main__':
    app.run_server(debug=True)