import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

path = 'databases/'
df_despesa_com_medicamentos_no_sns_por_ano_por_regiao = pd.DataFrame(data=pd.read_csv(path + 'despesa_com_medicamentos_no_sns_por_ano_por_regiao.csv'))

path = 'databases/'
df_despesa_com_medicamentos_no_sns_por_ano = pd.DataFrame(data=pd.read_csv(path + 'despesa_com_medicamentos_no_sns_por_ano.csv'))



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

#Total = Hospitalar + Ambulatório PVP
#Ambulatório PVP = Ambulatório Encargo Utentes + Ambulatório Comparticipalção SNS

dropdown_ars_gasto_medicamentos_2 = [
    {'label': 'Total', 'value': 'total'},
    {'label': 'Hospitalar', 'value': 'encargos_sns_hospitalar'},
    {'label': 'Ambulatório PVP', 'value': 'valor_pvp_ambulatorio'},
    {'label': 'Ambulatório Comparticipalção SNS', 'value': 'encargos_sns_ambulatorio'},
    {'label': 'Ambulatório Encargo Utentes', 'value': 'encargos_utentes_ambulatorio'},
    {'label': 'Ambulatório Comparticipalção SNS - Genéricos', 'value': 'encargos_sns_genericos'},

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
                    value='total'
                )

            ], className='col2 ', style={'text-align': 'left','width':'19%','float': 'left'}),
            html.Div([

                dcc.Graph(id='line_chart_1'),

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

            dcc.Graph(id='barchart_gasto_medicamentos_1'),

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
    Output("line_chart_1", "figure"),
    Output("barchart_gasto_medicamentos_1", "figure"),
    Output("barchart_gasto_medicamentos_2", "figure"),
    Input("dropdown_ars_gasto_medicamentos_1", "value"),
    Input("dropdown_ars_gasto_medicamentos_2", "value")
)

def generate_chart(dropdown_ars_barchart_1,dropdown_ars_barchart_2,):
    
    # line_chart_1

    gasto_medicamentos_nacional_por_ano = df_despesa_com_medicamentos_no_sns_por_ano.sort_values(by='ano', ascending=True)
    gasto_medicamentos_regiao_por_ano = df_despesa_com_medicamentos_no_sns_por_ano_por_regiao.sort_values(by='ano', ascending=True)
    lista_de_regioes = gasto_medicamentos_regiao_por_ano['regiao'].tolist()
    lista_de_regioes = list(dict.fromkeys(lista_de_regioes))

    line_chart_1 = go.Figure()
    line_chart_1.add_trace(go.Scatter(x=gasto_medicamentos_nacional_por_ano['ano'],
                                      y=gasto_medicamentos_nacional_por_ano['total'],
                                      mode='lines+markers',
                                      name='Total'))

    '''for regiao in lista_de_regioes:

        gastos_por_regiao = gasto_medicamentos_regiao_por_ano.loc[gasto_medicamentos_regiao_por_ano['regiao'] == regiao]

        line_chart_1.add_trace(go.Scatter(x=gastos_por_regiao['ano'],
                                          y=gastos_por_regiao['total'],
                                          mode='lines+markers',
                                          name=regiao
                                          ))'''

    line_chart_1.update_layout(title='Evolução dos gastos em medicamentos entre 2017 e 2021',
                               xaxis_title='Anos',
                               yaxis_title='Gastos em milhões de €',
                               paper_bgcolor='#FFFFFF')


    # barchart_1
    ## filtro aplicado com a função .loc[] com logica para ter apenas dados da ars selecionada no dropdown menu correspondente
    if dropdown_ars_barchart_1 == 'nacional':
        gasto_medicamentos = df_despesa_com_medicamentos_no_sns_por_ano_por_regiao.loc[df_despesa_com_medicamentos_no_sns_por_ano_por_regiao['regiao'] == dropdown_ars_barchart_1]
    else:
        gasto_medicamentos = df_despesa_com_medicamentos_no_sns_por_ano


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
        gasto_medicamentos = df_despesa_com_medicamentos_no_sns_por_ano_por_regiao.loc[df_despesa_com_medicamentos_no_sns_por_ano_por_regiao['regiao'] == dropdown_ars_barchart_1]
    else:
        gasto_medicamentos = df_despesa_com_medicamentos_no_sns_por_ano_por_regiao

    layout_bar_2 = dict(title=dict(text='evolução em percentagem'),
                        yaxis=dict(title='Gastos em milhões de €'),
                        xaxis=dict(title='Ano'),
                        paper_bgcolor='#FFFFFF'
                        )
    bar_chart_2 = go.Figure(data=[go.Bar(x=gasto_medicamentos['ano'], y=gasto_medicamentos['encargos_sns_ambulatorio'])],
                            layout=layout_bar_2
                            )
    bar_chart_2.update_layout(barmode="relative")
    #layout_yaxis_range=[0, max(gasto_medicamentos['encargos_sns_ambulatorio'])]

    


    ## Execução dos diferentes gráficos

    return bar_chart_1, \
           bar_chart_2, \
           line_chart_1,


## linha necessária par execuar a app
if __name__ == '__main__':
    app.run_server(debug=True)