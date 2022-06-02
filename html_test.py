import pandas as pd
#import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

## dá para alternar entre a base de dados dummy ou a base de dados real

path = ''
#df = pd.DataFrame(data=pd.read_csv(path + 'registo__doença_cardiaca.csv'))
df = pd.DataFrame(data=pd.read_csv(path + 'heart_2020_cleaned.csv'))

## definições dos botões radio

radio_options_fumadores = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Não Fumadores', 'value': 'n_fumadores'},
    {'label': 'Fumadores', 'value': 'fumadores'}
]


## linha obrigatória para lançar a aplicação

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

## HTML

app.layout = html.Div([
    html.H1("Bootstrap TEST!", className="m-5"),
    html.Div([
        html.H3('analise doentes cardiacos, todos, fumadores e não fumadores'),
    ],className='container'),
    html.Div([
        html.Div([
            html.H4("Filtros:")
        ],className='col'),
        html.Div([
            dcc.RadioItems(
                id='radio_filtro_fumadores',
                options=radio_options_fumadores,
                value='todos')
        ], className='col')
    ],className='row align-items-center'),
    html.Div([
        dcc.Graph(id="pie_chart")
    ])
])

## Callbacks de output e input

@app.callback(
    Output("pie_chart", "figure"),
    Input("radio_filtro_fumadores", "value")
)

## procedssamento dos inputs para actualização dos outputs
## este está a dar luta no sistema de filtros específicos que estou a imaginar

def generate_chart(radio_filtro_fumadores):

## esta parte do codigo foi uma solução baratinha mas limitada, so funciona a parte do filto de fumador

    tabela_freq = df.groupby(['HeartDisease','Smoking']).size().unstack()
    if radio_filtro_fumadores == 'todos':
        sem_dc = tabela_freq.loc['No']['No'] + tabela_freq.loc['No']['Yes']
        com_dc = tabela_freq.loc['Yes']['No'] + tabela_freq.loc['Yes']['Yes']
    elif radio_filtro_fumadores == 'n_fumadores':
        sem_dc = tabela_freq.loc['No']['No']
        com_dc = tabela_freq.loc['Yes']['No']
    elif radio_filtro_fumadores == 'fumadores':
        sem_dc = tabela_freq.loc['No']['Yes']
        com_dc = tabela_freq.loc['Yes']['Yes']

    df_contagens = pd.DataFrame(data={'categoria': ['Sem DC', 'Com DC'], 'numero': [sem_dc,com_dc]})

## algumas configurações do piechart, mas segundo a documentação não tem o atributo especifico do layout, parece-me um pouco limitado...

    fig = go.Figure(data=[go.Pie(labels=df_contagens['categoria'], values=df_contagens['numero'], textinfo='label+percent',
                                 insidetextorientation='horizontal')])
    return fig

## os exemoplos mais simples pedem so esta limnnha de codico, mas noutros wxwemplos mais avançados tem que ter uma linhas com __main__ qualquercoisa
app.run_server(debug=True)
