import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

path = ''
df = pd.DataFrame(data=pd.read_csv(path + 'registo__doença_cardiaca.csv'))
#df = pd.DataFrame(data=pd.read_csv(path + 'heart_2020_cleaned.csv'))

radio_options_fumadores = [
    {'label': 'Todos', 'value': 0},
    {'label': 'Não Fumadores', 'value': 'No"},
    {'label': 'Fumadores', 'value': 'Yes"}
]

radio_options_alcool = [
    {'label': 'Todos', 'value': 0},
    {'label': 'Não consumidor Álcool', 'value': 'No"},
    {'label': 'Consumidor Álcool', 'value': 'Yes"}
]

radio_options_diabetes = [
    {'label': 'Todos', 'value': 0},
    {'label': 'Não Diabético', 'value': 'No"},
    {'label': 'Diabético', 'value': 'Yes"}
]

radio_options_actividadefisica = [
    {'label': 'Todos', 'value': 0},
    {'label': 'Actividade Física', 'value': 'Yes'}
    {'label': 'Não Actividade Física', 'value': 'No'},
]

radio_options_etnia = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Caucasiano', 'value': 'caucasiano'},
    {'label': 'Hispânico', 'value': 'hispanico'},
    {'label': 'Afroamericano', 'value': 'afroamericano'},
    {'label': 'American Indian/Alaskan Native', 'value': 'indian_alaskan_native'}
]

app = Dash(__name__)

app.layout = html.Div([
    html.H1('TESTES'),
    html.H3('analise doentes cardiacos, todos, fumadores e não fumadores'),
    dcc.Graph(id='pie_chart'),
    html.H4('Filtros:'),
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

@app.callback(
    Output("pie_chart", "figure"),
    Input("radio_filtro_fumadores", "value"),
    Input("radio_filtro_alcool", "value"),
    Input("radio_filtro_diabetes", "value"),
    Input("radio_filtro_actividadefisica", "value"),
    Input("radio_filtro_etnia", "value")
)

def generate_chart(radio_filtro_fumadores,radio_filtro_alcool,radio_filtro_diabetes,radio_filtro_actividadefisica,radio_filtro_etnia):
    # a rersposta pode estar aqui
    # https://www.geeksforgeeks.org/count-all-rows-or-those-that-satisfy-some-condition-in-pandas-dataframe/

    radios = {'Smoking': radio_filtro_fumadores, 'AlcoholDrinking': radio_filtro_alcool, 'Diabetic': radio_filtro_diabetes, 'PhysicalActivity': radio_filtro_actividadefisica}
    doenca_cardiaca = ['Sem DC', 'Com DC']
    tabela_freq = pd.DataFrame(data={'HD': ['Sem DC', 'Com DC'], })
    for each in radios:
        for cada in doenca_cardiaca:
            tabela_freq

    sem_dc = df[(df['HeartDisease']=='No') & (df['Smoking'] == radio_filtro_fumadores) & (df['AlcoholDrinking'] == radio_filtro_alcool) & (df['Diabetic'] == radio_filtro_diabetes) & (df['PhysicalActivity'] == radio_filtro_actividadefisica)].count()
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

    fig = go.Figure(data=[go.Pie(labels=df_contagens['categoria'], values=df_contagens['numero'], textinfo='label+percent',
                                 insidetextorientation='horizontal')])
    return fig

app.run_server(debug=True)