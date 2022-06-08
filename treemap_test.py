import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px

path = 'databases/'
df_treemap = pd.DataFrame(data=pd.read_csv(path + 'dispensa-de-medicamentos-por-grupo-farmacoterapeutico-por-ano.csv'))

'''path =''
df_treemap = pd.DataFrame(data=pd.read_csv(path + 'grupos_medicamentos_dummy.csv'))'''


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

    ''' treemap_selection = df_treemap.loc[df_treemap['ano'] == slider_ano]
    treemap_selection_sorted = treemap_selection.sort_values(by='soma_encargos_sns_ambulatorio', ascending=False)
    lista_grupos_terapeuticos = treemap_selection_sorted['grupo_terapeutico'].tolist()
    lista_grupos_terapeuticos = list(dict.fromkeys(lista_grupos_terapeuticos))

    lista_ars = treemap_selection_sorted['ars'].tolist()
    lista_ars = list(dict.fromkeys(lista_ars))

    labels = ['Nacional']
    #values = [sum(treemap_selection['soma_encargos_sns_ambulatorio'])]
    values = [0]
    parents = ['']

    for each in lista_ars:
        labels.append(each)
        dados_por_ars = treemap_selection.loc[treemap_selection['ars'] == each]
        #values.append(sum(dados_por_ars['soma_encargos_sns_ambulatorio']))
        values.append(0)
        parents.append('Nacional')

        for cada in lista_grupos_terapeuticos:
            labels.append(cada)
            gasto_ars_grupo = dados_por_ars.loc[dados_por_ars['grupo_terapeutico']==cada]['soma_encargos_sns_ambulatorio']
            values.append(gasto_ars_grupo.to_string(index=False))
            #values.append(float(gasto_ars_grupo.to_string(index=False)))
            #values.append(4000000.0)
            parents.append(each)'''

    values = [0, 11, 12, 13, 14, 15, 20, 30, 2, 5, 4, 12, 23]
    labels = ["container", "A1", "A2", "A3", "A4", "A5", "B1", "B2", 'A6', 'aw', 'wefdcs', '234rtfe', '234']
    parents = ["", "container", "A1", "A2", "A3", "A4", "container", "B1", 'A1', "B1", 'A1', "container", 'B1']

    fig = go.Figure(go.Treemap(
        labels = labels,
        values = values,
        parents = parents,
        marker_colorscale = 'Blues'
    ))

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    return fig

app.run_server(debug=True)