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


dropdown_dispensa_medicamentos_tipo_1 = [
    {'label': 'Total (Hospitalar + Ambulatório)', 'value': 'total'},
    {'label': 'Hospitalar', 'value': 'encargos_sns_hospitalar'},
    {'label': 'Ambulatório (SNS + Utentes)', 'value': 'valor_pvp_ambulatorio'},
    {'label': 'Ambulatório Encargo SNS', 'value': 'encargos_sns_ambulatorio'},
    {'label': 'Ambulatório Encargo Utentes', 'value': 'encargos_utentes_ambulatorio'},
]

dropdown_dispensa_medicamentos_regiao_2 = [
    {'label': 'Nacional', 'value': 'Nacional'},
    {'label': 'Norte', 'value': 'Norte'},
    {'label': 'Centro', 'value': 'Centro'},
    {'label': 'Lisboa e Vale do Tejo', 'value': 'Lisboa e Vale do Tejo'},
    {'label': 'Alentejo', 'value': 'Alentejo'},
    {'label': 'Algarve', 'value': 'Algarve'},
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

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([

                html.Img(src=app.get_asset_url('logo.png'), style={'width': '60px', 'position': 'left'})
            ], id='logo')

        ], style={'width': '8%'}),
        html.Div([

            html.H1('Encargos com Medicamentos Comparticipados em Portugal')

            ],style={'width':'91%','position': 'right'}
        ),

    ],className='row container', style={'display': 'flex'}),

    html.Div([
        html.Div([
            html.Div([
                html.H3('Dashboard - Encargos com Medicamentos Comparticipados em Portugal'),
            ],style={'font-size': '17px'}),
            html.Label('O portal da transparência do SNS publica variados dados de saúde.'),
            html.Br(),
            html.Label('Este Dasboard analiza dados de encargos com medicação no Serviço Nacional de Saúde por região do país, por ano e por grupo farmacoterapêutico.'),
        ], className='row'),
    ]),

    html.Br(),

    html.Div([
        html.Div([
            html.H3('Qual a evolução dos encargos totais com medicamentos no SNS?')
        ], className='row', style={'text-align': 'center', 'font-size': '17px'}),
        html.Div([

            html.Div([
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
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
                        dcc.Checklist(
                            mostrar_nacional_checklist_1,
                            id='mostrar_nacional_checklist_1'
                        ),
                    ]),

                    html.Div([
                        dcc.Checklist(
                            normalizar_populacao_checklist_1,
                            id='normalizar_populacao_checklist_1'
                        )
                    ]),
                    html.Br(),
                ],className='row filter_container'),
            ], className='col2', style={'width': '25%', 'text-align': 'left'}),
            html.Div([
                dcc.Graph(id='line_chart_dispensa_medicamentos_1')
            ], className='col2', style={'width': '64%', 'text-align': 'center'}),
        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([
            html.H3('Qual a divisão entre encargos em ambulatório e em ambiente hospitalar?')
        ], className='row', style={'text-align': 'center', 'font-size': '17px'}),
        html.Div([
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
                        html.Div([
                            dcc.RadioItems(
                                id='radio_percentage_absoluto_2',
                                options=radio_percentage_absoluto_2,
                                value='percentagem'
                            ),
                        ]),
                    ], style={}),
                ], className='filter_container'),
            ], className='col2',style={'width':'35%'}),
            html.Div([
                html.Label('Comparação entre encargos com medicamentos Hospitalares versus Ambulatório, em percentagem ou valores absolutos, entre 2011 e 2021. Valores nacionais ou por região'),
                html.Br(),
                html.Label('Dentro dos medicamentos de Ambulatório, comparação dos encargos para o SNS e para o utente'),
                html.Br(),
            ], className='col2',style={'width': '64%', 'text-align': 'left'}),


        ], className='row', style={'display': 'flex'}),

        html.Br(),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='stacked_bar_chart_medicamentos_2'),
                ], className='col2', style={'width':'45%','text-align': 'center'}),
                html.Div([
                    dcc.Graph(id='stacked_bar_chart_medicamentos_3'),
                ], className='col2', style={'width': '45%', 'text-align': 'center'}),
            ], className='', style={'width':'99%','float':'center', 'text-align': 'center'}),
        ],className='row', style={'display': 'flex'}),
    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([

            html.H3('Qual a despesa de medicamentos por grupo farmacoterapêutico?')

        ], className='row', style={'text-align': 'center', 'font-size': '17px'}),
        html.Label('Evolução dos encargos em medicamentos por grupo farmacoterapêutico e por região.'),
        html.Br(),
        html.Label('Evolução entre 2011 e 2021'),
        html.Br(),
        html.Div([
            dcc.Graph(id='treemap_regiao_grupo_farmaceutico_4'),
        ],className='row', style={}),
        html.Div([
            html.Div([
                dcc.Slider(0,10,
                    marks={0:'2011',1:'2012',2:'2013',3:'2014',4:'2015',5:'2016',6:'2017',7:'2018',8:'2019',9:'2020',10:'2021'},
                    step=None,
                    value=10,
                    id='slider_ano_3'),
                ]),
        ],className='row', style={}),

    ], className='row container', style={'display': 'block'}),

    html.Br(),

    html.Div([
        html.Div([
            html.H3('Referências')
        ], className='row', style={'display': 'flex','text-align': 'center', 'font-size': '17px'}),

        html.Div([
            html.Label('​Ministério da Saúde. (junho de 2022). Portal da Transparência. Obtido de Portal da Transparência: https://www.sns.gov.pt/transparencia/'),
            html.Br(),
            html.Label('Munzner, T. (2015). Visualization Analysis and Design. CRC Press.'),
            html.Br(),
            html.Label('Plotly. (maio de 2022). Dash Python User Guide. Obtido de Dash Python User Guide: https://dash.plotly.com/ '),
        ], className='row', style={'display': 'block','text-align': 'center'})
    ], className='row container', style={'display': 'block'}),

    html.Div([
        html.Div([
            html.H3('Autores')
        ], className='row', style={'display': 'flex','text-align': 'center', 'font-size': '17px'}),
        html.Div([
            html.Label('Catarina Bragança (20210950), Diogo Carapito (20211202), Filipa Pardelha (20210949), Ricardo Martins (20211710)'),
            html.Br()
        ], className='row', style={'display': 'flex','text-align': 'center'})
    ], className='row container', style={'display': 'block'}),
])

@app.callback(
    Output('line_chart_dispensa_medicamentos_1', 'figure'),
    Output('stacked_bar_chart_medicamentos_2', 'figure'),
    Output('stacked_bar_chart_medicamentos_3', 'figure'),
    Output('treemap_regiao_grupo_farmaceutico_4', 'figure'),
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
        populacao={'Nacional':10493410, 'Norte':3765539,'Lisboa e Vale do Tejo':3869536,'Centro':1819360,'Alentejo':528126,'Algarve':510849}
        y_axis='Encargos per capita em €'
    else:
        populacao={'Nacional': 1, 'Norte': 1, 'Lisboa e Vale do Tejo': 1, 'Centro': 1, 'Alentejo': 1,'Algarve': 1}
        y_axis='Encargos em Euros'

    cor = {'Nacional': 'rgba(23, 16, 90, 1)', 'Norte': 'rgba(128, 168, 214, 1)', 'Lisboa e Vale do Tejo': '#C8C3F8', 'Centro': '#8AF0CE', 'Alentejo': 'rgba(234, 150, 126, 1)','Algarve': 'rgba(246, 210, 129, 1)'}

    for regiao in lista_de_regioes:
        Encargos_por_regiao = gasto_medicamentos_regiao_por_ano.loc[gasto_medicamentos_regiao_por_ano['regiao'] == regiao]
        line_chart_dispensa_medicamentos_1.add_trace(go.Scatter(
            x=Encargos_por_regiao['ano'],
            y=(Encargos_por_regiao[dropdown_dispensa_medicamentos_tipo_1]/populacao[regiao]).round(decimals = 0),
            mode='lines+markers',
            name=regiao,
            marker_color= cor[regiao]
        ))

    if mostrar_nacional_checklist_1 == ['Mostrar Nacional']:
        gasto_medicamentos_nacional_por_ano = df_despesa_com_medicamentos_no_sns_por_ano.sort_values(by='ano',ascending=True)
        gasto_medicamentos_nacional_por_ano['ano'] = gasto_medicamentos_nacional_por_ano['ano'].apply(str)
        line_chart_dispensa_medicamentos_1.add_trace(go.Scatter(
            x=gasto_medicamentos_nacional_por_ano['ano'],
            y=(gasto_medicamentos_nacional_por_ano[dropdown_dispensa_medicamentos_tipo_1]/populacao['Nacional']).round(decimals = 0),
            mode='lines+markers',
            name='Nacional',
            marker_color=cor['Nacional']
        ))

    line_chart_dispensa_medicamentos_1.update_layout(
        title='Evolução dos Encargos em medicamentos entre 2011 e 2021 por Região',
        xaxis_title='Ano',
        yaxis_title=y_axis,
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#F3F6F8',
    )

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
        y_valor_pvp_ambulatorio = (((data_base['valor_pvp_ambulatorio'] / data_base['total']).round(decimals = 3)*100).tolist())
        y_axis_title = '% de Encargos por categoria'
    else:
        y_encargos_sns_hospitalar = (data_base['encargos_sns_hospitalar'].tolist())
        y_valor_pvp_ambulatorio = (data_base['valor_pvp_ambulatorio'].tolist())
        y_axis_title = 'Encargos por categoria em Euros'

    layout_stacked_bar_chart_medicamentos_2 = dict(title=dict(text='Encargos por categoria entre 2011 e 2021'),
                      yaxis=dict(title=y_axis_title),
                      xaxis=dict(title='Ano'),
                      paper_bgcolor='#FFFFFF',
                      plot_bgcolor='#F3F6F8',
                      barmode='stack'
    )

    stacked_bar_chart_medicamentos_2 = go.Figure(
        data=[
            go.Bar(
                name='Encargos SNS Hospitalar',
                x=data_base['ano'].tolist(),
                y=y_encargos_sns_hospitalar,
                marker_color = '#545F8D'
            ),
            go.Bar(
                name='Encargos SNS Ambulatório',
                x=data_base['ano'].tolist(),
                y=y_valor_pvp_ambulatorio,
                marker_color = '#B8EAA9'
            ),
        ],layout=layout_stacked_bar_chart_medicamentos_2,)

    # stacked_bar_chart_medicamentos_3

    if radio_percentage_absoluto_2 == 'percentagem':
        y_encargos_sns_ambulatorio = (((data_base['encargos_sns_ambulatorio'] / data_base['valor_pvp_ambulatorio']).round(decimals = 3)*100).tolist())
        y_encargos_utentes_ambulatorio = (((data_base['encargos_utentes_ambulatorio'] / data_base['valor_pvp_ambulatorio']).round(decimals = 3)*100).tolist())
        y_axis_title_3 = '% de Encargos por categoria'
    else:
        y_encargos_sns_ambulatorio = (data_base['encargos_sns_ambulatorio'].tolist())
        y_encargos_utentes_ambulatorio = (data_base['encargos_utentes_ambulatorio'].tolist())
        y_axis_title_3 = 'Encargos por categoria em Euros'

    layout_stacked_bar_chart_medicamentos_3 = dict(
        title=dict(text='Encargos no Ambulatório por categoria entre 2011 e 2021'),
        yaxis=dict(title=y_axis_title_3),
        xaxis=dict(title='Ano'),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#F3F6F8',
    )

    stacked_bar_chart_medicamentos_3 = go.Figure(
        data=[
            go.Bar(
                name='Ambulatório Enacargos SNS',
                x=data_base['ano'].tolist(),
                y=y_encargos_sns_ambulatorio,
                marker_color='#85C575'
            ),
            go.Bar(
                name='Ambulatório Enacargos Utente',
                x=data_base['ano'].tolist(),
                y=y_encargos_utentes_ambulatorio,
                marker_color='#D7E17F'

            ),
        ],layout=layout_stacked_bar_chart_medicamentos_3,)

    stacked_bar_chart_medicamentos_3.update_layout(barmode='stack')

    # treemap

    slider_converter = {0:2011, 1:2012, 2:2013, 3:2014, 4:2015, 5:2016, 6:2017, 7:2018, 8:2019, 9:2020, 10:2021}
    grupo_farmaceutico_por_ano_por_regiao = df_despesa_por_grupo_farmaceutico_por_ano_por_regiao.loc[df_despesa_por_grupo_farmaceutico_por_ano_por_regiao['ano'] == slider_converter[slider_ano_3]]

    treemap_regiao_grupo_farmaceutico_4=px.treemap(
        grupo_farmaceutico_por_ano_por_regiao,
        path=['regiao','grupo_terapeutico'],
        values='encargos_sns_ambulatorio',
        color='encargos_sns_ambulatorio',
        color_continuous_scale='emrld',
    )

    treemap_regiao_grupo_farmaceutico_4.update_traces(root_color="lightgrey")
    treemap_regiao_grupo_farmaceutico_4.update_layout(margin=dict(t=10, l=10, r=10, b=10))

    return line_chart_dispensa_medicamentos_1, stacked_bar_chart_medicamentos_2,stacked_bar_chart_medicamentos_3,treemap_regiao_grupo_farmaceutico_4

if __name__ == '__main__':
    app.run_server(debug=True)