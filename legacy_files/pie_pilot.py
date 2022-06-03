import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

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
radio_options_alcool = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Não consumidor Álcool', 'value': 'n_alcool'},
    {'label': 'Consumidor Álcool', 'value': 'AlcoholDrinking'}
]
radio_options_diabetes = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Não Diabético', 'value': 'n_diabetico'},
    {'label': 'Diabético', 'value': 'diabetico'}
]
radio_options_actividadefisica = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Não Actividade Física', 'value': 'n_actividadefisica'},
    {'label': 'Actividade Física', 'value': 'actividadefisica'}
]
radio_options_etnia = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Caucasiano', 'value': 'caucasiano'},
    {'label': 'Hispânico', 'value': 'hispanico'},
    {'label': 'Afroamericano', 'value': 'afroamericano'},
    {'label': 'American Indian/Alaskan Native', 'value': 'indian_alaskan_native'}
]

## linha obrigatória para lançar a aplicação

app = Dash(__name__)

## HTML

app.layout = html.Div([
    html.H1('TESTES'),
    html.H3('analise doentes cardiacos, todos, fumadores e não fumadores'),
    dcc.Graph(id="pie_chart"),
    html.H4("Filtros:"),
    dcc.RadioItems(
        id='radio_filtro_fumadores',
        options=radio_options_fumadores,
        value='todos'
    ),
    dcc.RadioItems(
        id='radio_filtro_alcool',
        options=radio_options_alcool,
        value='todos'
    ),
    dcc.RadioItems(
        id='radio_filtro_diabetes',
        options=radio_options_diabetes,
        value='todos'
    ),
    dcc.RadioItems(
        id='radio_filtro_actividadefisica',
        options=radio_options_actividadefisica,
        value='todos'
    ),
    dcc.RadioItems(
        id='radio_filtro_etnia',
        options=radio_options_etnia,
        value='todos'
    )
])

## Callbacks de output e input

@app.callback(
    Output("pie_chart", "figure"),
    Input("radio_filtro_fumadores", "value"),
    Input("radio_filtro_alcool", "value"),
    Input("radio_filtro_diabetes", "value"),
    Input("radio_filtro_actividadefisica", "value"),
    Input("radio_filtro_etnia", "value")
)

## procedssamento dos inputs para actualização dos outputs
## este está a dar luta no sistema de filtros específicos que estou a imaginar

def generate_chart(radio_filtro_fumadores,radio_filtro_alcool,radio_filtro_diabetes,radio_filtro_actividadefisica,radio_filtro_etnia):

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
