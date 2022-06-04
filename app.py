import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

## CSV para o pie chart
path = ''
df = pd.DataFrame(data=pd.read_csv(path + 'registo__doença_cardiaca.csv'))
#df = pd.DataFrame(data=pd.read_csv(path + 'heart_2020_cleaned.csv'))

## CSV para o bar chart
df_bar_chart_1 = pd.DataFrame(data=pd.read_csv(path + 'bar_chart_dummy.csv'))


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

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('TESTE')
            ],style={'width':'79%','position': 'center'}
        ),
        html.Div([
            html.Div([html.Img(src=app.get_asset_url('logo.png'),style={'width': '50px', 'position': 'center'})], id='logo'),
        ],style={'width':'20%'}),
    ],className='row container', style={'display': 'flex'}),

    html.Div([
        html.Div([
            html.H3('Explicação sobre o trabalho de DV'),
            html.Label('Explicações nevessárias sobre vários motivos e razões relativa a situações variadas e essenciais para uma boa relação entre as difrentes consistências ')
        ], className='row'),
    ]),

    html.Div([
        html.Div([
            html.H3('Analise doentes cardiacos, todos, fumadores e não fumadores')
        ], className='row'),
        html.Div([
            html.Div([
                html.H3('Filtros:'),
                dcc.RadioItems(
                    id='radio_filtro_fumadores',
                    options=radio_options_fumadores,
                    value='todos'
                )
            ], className='col2 ', style={'text-align': 'left','width':'34%','float': 'left'}),
            html.Div([
                    dcc.Graph(id='pie_graph'),
                ], className='col2', style={'width':'65%','float':'right'}),
        ],className='row'),
    ], className='row container',style={'hight':'40%'}),

    html.Br(),
    html.Br(),

    html.Div([
        html.Div([
            html.H3('Gastos medicmaentos por ARS entre 2017 e 2021')
        ], className='row'),
        html.Div([
            html.Div([
                html.H3('Filtros:'),
                dcc.Dropdown(
                    id='dropdown_ars_barchart_1',
                    options=dropdown_ars_barchart_1,
                    value='norte'
                )
            ], className='col2 ', style={'text-align': 'left','width':'34%','float': 'left'}),
            html.Div([
                dcc.Graph(id='bar_chart_1'),
            ], className='col2', style={'width':'65%','float':'right'}),
        ],className='row'),
    ], className='row container',style={'hight':'40%'}),


])

@app.callback(
    Output("pie_graph", "figure"),
    Output("bar_chart_1", "figure"),
    Input("radio_filtro_fumadores", "value"),
    Input("dropdown_ars_barchart_1", "value")
)

def generate_chart(radio_filtro_fumadores,dropdown_ars_barchart_1):

    tabela_freq = df.groupby(['HeartDisease', 'Smoking']).size().unstack()

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

    ## algumas configurações do piechart, mas segundo a documentação não tem o atributo especifico do layout, parece-me um pouco limitado...
    pie_chart = go.Figure(
        data=[go.Pie(labels=df_contagens['categoria'], values=df_contagens['numero'], textinfo='label+percent',
                     insidetextorientation='horizontal',showlegend=False)])

    ## barchart
    table_barchart_1 = df_bar_chart_1.loc[df_bar_chart_1['ars'] == dropdown_ars_barchart_1]

    #data_bar_1= ('type'='bar', 'x'=table_barchart_1['ano'], 'y'=table_barchart_1['gasto_medicamentos'])

    layout_bar_1 = dict(title=dict(text='Gastros entre 2017 e 2021'),
                      yaxis=dict(title='Gastos em milhões de €'),
                      paper_bgcolor='#f9f9f9'
                      )
    bar_chart_1 = go.Figure(data=[go.Bar(x=table_barchart_1['ano'], y=table_barchart_1['gasto_medicamentos'])],
                            layout=layout_bar_1,
                            layout_yaxis_range=[0,max(df_bar_chart_1['gasto_medicamentos'])])

    return pie_chart, \
           bar_chart_1

if __name__ == '__main__':
    app.run_server(debug=True)