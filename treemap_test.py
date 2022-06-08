import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

path = 'databases/'
df_treemap = pd.DataFrame(data=pd.read_csv(path + 'dispensa-de-medicamentos-por-grupo-farmacoterapeutico-por-ano.csv'))



values = [0, 11, 12, 13, 14, 15, 20, 30]
labels = ["Nacional", "LVT", "A2", "Norte", "B2", 'Centro']
parents = ["", "Nacional", "LVT", "Nacional", "Norte"]

treemap_anos = list(dict.fromkeys(df_treemap['ano'].tolist()))

year_slider = dcc.Slider(
    id = 'slider_ano',
    min=min(treemap_anos),
    max=max(treemap_anos),
    step=1,
    value=max(treemap_anos),

)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='treemap'),
    year_slider,

])

@app.callback(
    Output("treemap", "figure"),
    Input('slider_ano', 'value'),
)

def generate_chart(slider_ano):

    treemap_selection = df_treemap.loc[df_treemap['ano'] == slider_ano]
    treemap_selection_sorted = treemap_selection.sort_values(by='soma_encargos_sns_ambulatorio', ascending=False)
    lista_grupos_terapeuticos = treemap_selection_sorted['grupo_terapeutico'].tolist()
    lista_grupos_terapeuticos = list(dict.fromkeys(lista_grupos_terapeuticos))

    lista_ars = treemap_selection_sorted['ars'].tolist()
    lista_ars = list(dict.fromkeys(lista_ars))

    labels = ['Nacional']
    values = [sum(treemap_selection['soma_encargos_sns_ambulatorio'])]
    parents = ['']
    for each in lista_ars:
        labels.append(each)
        dados_por_ars = treemap_selection.loc[df_treemap['ars'] == each]
        values.append(sum(dados_por_ars))
        parents.append('Nacional')
        for cada in lista_grupos_terapeuticos:
            labels.append(cada)
            values.append(dados_por_ars[cada])
            parents.append(each)

    fig = go.Figure(go.Treemap(
        labels = labels,
        values = values,
        parents = parents,
        marker_colorscale = 'Blues'
    ))

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    return fig

app.run_server(debug=True)