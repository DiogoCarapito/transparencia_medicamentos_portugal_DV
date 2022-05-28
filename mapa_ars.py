import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import geojson

## import da base de dados

path = ''
df = pd.DataFrame(data=pd.read_csv(path + 'medicamentos_ars.csv'))

dropdown_mes = dcc.Dropdown(
        id='mes_drop',
        options=[dict(label=mes, value=mes) for mes in df['mes'].unique()],
        value=['jan'],
        multi=True
    )
## import de dados geojson
with open("file.geojson", "r", encoding="utf-8") as f:
    geometry = geojson.load(f)


## linha obrigatória para lançar a aplicação

app = Dash(__name__)

## HTML

app.layout = html.Div([
    html.H1('Consumo Medicamento ARS'),
    html.H3('custos de medicamentos por ARS'),
    dropdown_mes,
    html.Br(),
    dcc.Graph(id='choropleth'),

])

## Callbacks de output e input

@app.callback(
    Output('choropleth', 'figure'),
    Input('mes_drop','value')
)





with open("file.geojson", "r", encoding="utf-8") as f:
    geometry = geojson.load(f)

fig = go.Figure([
    go.Choropleth(
        geojson = geometry,
        locations = df["code"],
        z = df["crude_rate"],
        text = df["label"]
)])

fig.update_geos(
    fitbounds="locations",
    resolution=50,
    visible=False,
    showframe=False,
    projection={"type": "mercator"},
)



def generate_chart(mes_drop):
    a=mes_drop
    z=df['mes']
    data_choropleth = dict(type='choropleth',
                           locations=df['ARS'],
                           locationmode='prt',
                           z=z,
                           text=df['ARS'],
                           colorscale='inferno',
                           colorbar=dict(title=str(df['custo_medicamento'])),

                           #hovertemplate='Country: %{text} <br>' + str(gas.replace('_', ' ')) + ': %{z}',
                           name=''
                           )

    layout_choropleth = dict(geo=dict(scope='portugal',  # default
                                      projection='equirectangular',
                                      # showland=True,   # default = True
                                      landcolor='black',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure',
                                      bgcolor='#f9f9f9'
                                      ),

                             title=dict(
                                 text='Portugal',
                                 x=.5  # Title relative position according to the xaxis, range (0,1)

                             ),
                             paper_bgcolor='#f9f9f9'
                             )

    return go.Figure(data=data_choropleth, layout=layout_choropleth)

## os exemoplos mais simples pedem so esta limnnha de codico, mas noutros wxwemplos mais avançados tem que ter uma linhas com __main__ qualquercoisa
app.run_server(debug=True)
