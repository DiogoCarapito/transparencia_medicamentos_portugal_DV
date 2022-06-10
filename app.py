import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px

path = 'databases/'
df_despesa_com_medicamentos_no_sns_por_ano_por_regiao = pd.DataFrame(data=pd.read_csv(path + 'despesa_com_medicamentos_no_sns_por_ano_por_regiao.csv'))

path = 'databases/'
df_despesa_com_medicamentos_no_sns_por_ano = pd.DataFrame(data=pd.read_csv(path + 'despesa_com_medicamentos_no_sns_por_ano.csv'))

path = 'databases/'
df_despesa_por_grupo_farmaceutico_por_ano_por_regiao = pd.DataFrame(data=pd.read_csv(path + 'dispensa_de_medicamentos_por_grupo_farmacoterapeutico_por_ano_por_regiao.csv'))


#Total = Hospitalar + Ambulatório PVP
#Ambulatório PVP = Ambulatório Encargo Utentes + Ambulatório Comparticipalção SNS

dropdown_dispensa_medicamentos_tipo_1 = [
    {'label': 'Total', 'value': 'total'},
    {'label': 'Hospitalar', 'value': 'encargos_sns_hospitalar'},
    {'label': 'Ambulatório PVP', 'value': 'valor_pvp_ambulatorio'},
    {'label': 'Ambulatório Comparticipalção SNS', 'value': 'encargos_sns_ambulatorio'},
    {'label': 'Ambulatório Encargo Utentes', 'value': 'encargos_utentes_ambulatorio'},
]

dropdown_dispensa_medicamentos_regiao_2 = [
    {'label': 'Nacional', 'value': 'Nacional'},
    {'label': 'Norte', 'value': 'Norte'},
    {'label': 'Centro', 'value': 'Centro'},
    {'label': 'LVT', 'value': 'LVT'},
    {'label': 'Alentejo', 'value': 'Alentejo'},
    {'label': 'Algarve', 'value': 'Algarve'},
]

#Total = Hospitalar + Ambulatório PVP
#Ambulatório PVP = Ambulatório Encargo Utentes + Ambulatório Comparticipalção SNS

dropdown_dispensa_medicamentos_tipo_1 = [
    {'label': 'Total', 'value': 'total'},
    {'label': 'Hospitalar', 'value': 'encargos_sns_hospitalar'},
    {'label': 'Ambulatório PVP', 'value': 'valor_pvp_ambulatorio'},
    {'label': 'Ambulatório Comparticipalção SNS', 'value': 'encargos_sns_ambulatorio'},
    {'label': 'Ambulatório Encargo Utentes', 'value': 'encargos_utentes_ambulatorio'},
]

radio_percentage_absoluto_2 = [
    {'label': 'Percentagem', 'value': 'percentagem'},
    {'label': 'Absoluto', 'value': 'absoluto'}
]


mostrar_nacional_checklist_1 = [
    'Mostrar Nacional'
]

normalizar_populacao_checklist_1 = [
    'Normalizar (por habitante)'
]

app = Dash(__name__)

## HTML em dash
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([

                html.Img(src=app.get_asset_url('logo.png'), style={'width': '60px', 'position': 'left'})
            ], id='logo')

        ], style={'width': '25%'}),
        html.Div([

            html.H2('Medicamentos - Portal da Transparência')

            ],style={'width':'79%','position': 'right'}
        ),

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
        ], className='row', style={'text-align': 'center'}),
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id='dropdown_dispensa_medicamentos_tipo_1',
                                options=dropdown_dispensa_medicamentos_tipo_1,
                                value='total',
                                searchable=False,
                                clearable=False
                            ),
                        ]),
                        html.Br(),
                        html.Div([
                            html.Div([
                                dcc.Checklist(
                                    mostrar_nacional_checklist_1,
                                    id = 'mostrar_nacional_checklist_1'
                                ),
                            ]),
                            html.Div([
                                dcc.Checklist(
                                    normalizar_populacao_checklist_1,
                                    id='normalizar_populacao_checklist_1'
                                )
                            ]),
                        ],style={'display':'block'}),
                    ],className='row filter_container', style={'text-align': 'center','justify-content': 'center', 'width': '50%'}),
                ],style={}),
                html.Br(),

                html.Div([
                    dcc.Graph(id='line_chart_dispensa_medicamentos_1')
                ], className='row', style={}),

            ], className='col2', style={'width':'49%','float':'center', 'text-align': 'center'}),
            html.Div([

                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_dispensa_medicamentos_regiao_2',
                            options=dropdown_dispensa_medicamentos_regiao_2,
                            value='Nacional',
                            searchable=False,
                            clearable=False
                        ),
                    ]),
                    html.Br(),
                    html.Div([
                        dcc.RadioItems(
                            id='radio_percentage_absoluto_2',
                            options=radio_percentage_absoluto_2,
                            value='percentagem'
                        ),
                    ]),
                    html.Br(),
                ],className='row filter_container', style={'text-align': 'center', 'width': '50%'}),

                html.Br(),

                html.Div([
                    dcc.Graph(id='stacked_bar_chart_medicamentos_2'),
                ],className='row', style={}),

            ], className='col2', style={'width':'49%','float':'right'}),
        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([

            html.H3('Gastos medicmaentos por ARS entre 2017 e 2021 texto grande so para testar coisas ')

        ], className='row', style={'text-align': 'center'}),
        html.Br(),
        html.Div([
            dcc.Graph(id='sunburst_regiao_grupo_farmaceutico_3'),
        ],className='row', style={}),
        html.Div([
            html.Div([
                dcc.Slider(min=2011,
                           max=2021,
                           step=1,
                           value=2021,
                           id='slider_ano_3'
                           ),
                ]),
        ],className='row', style={}),

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
    Output('line_chart_dispensa_medicamentos_1', 'figure'),
    Output('stacked_bar_chart_medicamentos_2', 'figure'),
    Output('sunburst_regiao_grupo_farmaceutico_3', 'figure'),
    Input('dropdown_dispensa_medicamentos_tipo_1', 'value'),
    Input('dropdown_dispensa_medicamentos_regiao_2', 'value'),
    Input('radio_percentage_absoluto_2', 'value'),
    Input('slider_ano_3', 'value'),
    Input('mostrar_nacional_checklist_1', 'value'),
    Input('normalizar_populacao_checklist_1', 'value'),



)

def generate_chart(dropdown_dispensa_medicamentos_tipo_1,dropdown_dispensa_medicamentos_regiao_2,radio_percentage_absoluto_2,slider_ano_3,mostrar_nacional_checklist_1,normalizar_populacao_checklist_1):
    
    # line_chart_dispensa_medicamentos_1

    gasto_medicamentos_regiao_por_ano = df_despesa_com_medicamentos_no_sns_por_ano_por_regiao.sort_values(by='ano', ascending=True)

    gasto_medicamentos_regiao_por_ano_ordenado = gasto_medicamentos_regiao_por_ano.sort_values(by='total', ascending=False)
    lista_de_regioes = gasto_medicamentos_regiao_por_ano_ordenado['regiao'].tolist()
    lista_de_regioes = list(dict.fromkeys(lista_de_regioes))

    gasto_medicamentos_regiao_por_ano['ano'] = gasto_medicamentos_regiao_por_ano['ano'].apply(str)

    line_chart_dispensa_medicamentos_1 = go.Figure()

    if normalizar_populacao_checklist_1 == ['Normalizar (por habitante)']:
        populacao={'Nacional':10493410, 'Norte':3765539,'LVT':3869536,'Centro':1819360,'Alentejo':528126,'Algarve':510849}
        y_axis='Gastos per capita em €'
    else:
        populacao={'Nacional': 1, 'Norte': 1, 'LVT': 1, 'Centro': 1, 'Alentejo': 1,'Algarve': 1}
        y_axis='Gastos em milhões de €'


    for regiao in lista_de_regioes:
        gastos_por_regiao = gasto_medicamentos_regiao_por_ano.loc[gasto_medicamentos_regiao_por_ano['regiao'] == regiao]
        line_chart_dispensa_medicamentos_1.add_trace(go.Scatter(
            x=gastos_por_regiao['ano'],
            y=(gastos_por_regiao[dropdown_dispensa_medicamentos_tipo_1]/populacao[regiao]).round(decimals = 0),
            mode='lines+markers',
            name=regiao
        ))


    if mostrar_nacional_checklist_1 == ['Mostrar Nacional']:
        gasto_medicamentos_nacional_por_ano = df_despesa_com_medicamentos_no_sns_por_ano.sort_values(by='ano',ascending=True)
        gasto_medicamentos_nacional_por_ano['ano'] = gasto_medicamentos_nacional_por_ano['ano'].apply(str)
        line_chart_dispensa_medicamentos_1.add_trace(go.Scatter(
            x=gasto_medicamentos_nacional_por_ano['ano'],
            y=(gasto_medicamentos_nacional_por_ano[dropdown_dispensa_medicamentos_tipo_1]/populacao['Nacional']).round(decimals = 0),
            mode='lines+markers',
            name='Nacional'
        ))


    line_chart_dispensa_medicamentos_1.update_layout(
        title='Evolução dos gastos em medicamentos entre 2017 e 2021 por Região',
        xaxis_title='Ano',
        yaxis_title=y_axis,
        paper_bgcolor='#FFFFFF')


    # stacked_bar_chart_medicamentos_2

    if dropdown_dispensa_medicamentos_regiao_2 == 'Nacional':
        data_base = df_despesa_com_medicamentos_no_sns_por_ano.sort_values(by='ano', ascending=True)
        data_base['ano'] = data_base['ano'].apply(str)
    else:
        data_base = df_despesa_com_medicamentos_no_sns_por_ano_por_regiao.sort_values(by='ano', ascending=True)
        data_base['ano'] = data_base['ano'].apply(str)
        data_base = data_base.loc[data_base['regiao'] == dropdown_dispensa_medicamentos_regiao_2]

    if radio_percentage_absoluto_2 == 'percentagem':
        y_encargos_sns_hospitalar = (((data_base['encargos_sns_hospitalar'] / data_base['total']).round(decimals = 3)*100).tolist())
        y_encargos_sns_ambulatorio = (((data_base['encargos_sns_ambulatorio'] / data_base['total']).round(decimals = 3)*100).tolist())
        y_encargos_utentes_ambulatorio = (((data_base['encargos_utentes_ambulatorio'] / data_base['total']).round(decimals = 3)*100).tolist())
        y_axis_title = '% de Gastos por categoria'
    else:
        y_encargos_sns_hospitalar = (data_base['encargos_sns_hospitalar'].tolist())
        y_encargos_sns_ambulatorio = (data_base['encargos_sns_ambulatorio'].tolist())
        y_encargos_utentes_ambulatorio = (data_base['encargos_utentes_ambulatorio'].tolist())
        y_axis_title = 'M€ Gastos por categoria'

    layout_stacked_bar_chart_medicamentos_2 = dict(title=dict(text='Gastros por categoria entre 2017 e 2021'),
                      yaxis=dict(title=y_axis_title),
                      xaxis=dict(title='Ano'),
                      paper_bgcolor='#FFFFFF',
    )

    stacked_bar_chart_medicamentos_2 = go.Figure(
        data=[
            go.Bar(name='Gastos SNS Hospitalar', x=data_base['ano'].tolist(), y=y_encargos_sns_hospitalar),
            go.Bar(name='Gastos SNS Ambulatório', x=data_base['ano'].tolist(), y=y_encargos_sns_ambulatorio),
            go.Bar(name='Gastos Utentes Ambulatório', x=data_base['ano'].tolist(), y=y_encargos_utentes_ambulatorio),
        ],layout=layout_stacked_bar_chart_medicamentos_2,)

    stacked_bar_chart_medicamentos_2.update_layout(barmode='stack')

    # sunburst

    grupo_farmaceutico_por_ano_por_regiao = df_despesa_por_grupo_farmaceutico_por_ano_por_regiao.loc[df_despesa_por_grupo_farmaceutico_por_ano_por_regiao['ano'] == slider_ano_3]

    '''grupo_farmaceutico_por_ano_por_regiao_ordenado = grupo_farmaceutico_por_ano_por_regiao.sort_values(by='encargos_sns_ambulatorio',ascending=True)
    lista_de_grupo_terapeutico = grupo_farmaceutico_por_ano_por_regiao_ordenado['grupo_terapeutico'].tolist()
    lista_de_grupo_terapeutico = list(dict.fromkeys(lista_de_grupo_terapeutico))'''

    sunburst_regiao_grupo_farmaceutico_3=px.treemap(grupo_farmaceutico_por_ano_por_regiao,path=['regiao','grupo_terapeutico'], values='encargos_sns_ambulatorio')


    '''
    l= ['Nacional']
    p=['']
    v=[0]

    for regi in lista_de_regioes:
        l.append(regi)
        p.append('Nacional')
        v.append(0)
        for cada in lista_de_grupo_terapeutico:
            l.append(cada)
            p.append(regi)
            v.append(10)

    l = ['Nacinal', 'Norte', 'Centro', 'Enos', 'Noam', 'Alentejo', 'LVT', 'Enoch', 'Algarve','cenas']
    p = ['', 'Nacinal', 'Nacinal', 'Centro', 'Centro', 'Nacinal', 'Nacinal', 'LVT', 'Nacinal','Norte']
    v = [0, 0, 0, 10, 2, 0, 0, 4, 0,3]
    
    sunburst_regiao_grupo_farmaceutico_3 = go.Figure(go.Sunburst(
        labels=l,
        parents= p,
        values= v,
    ))
    
    # Update layout for tight margin
    # See https://plotly.com/python/creating-and-updating-figures/
    '''
    sunburst_regiao_grupo_farmaceutico_3.update_layout(margin=dict(t=10, l=10, r=10, b=10))


    return line_chart_dispensa_medicamentos_1, stacked_bar_chart_medicamentos_2,sunburst_regiao_grupo_farmaceutico_3



## linha necessária par execuar a app
if __name__ == '__main__':
    app.run_server(debug=True)