import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import tabula
from dash.dependencies import Input, Output
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go

## inicio app
app = Dash(__name__)
server = app.server

########## limpieza y lectura desde el PDF #########
df = tabula.read_pdf("DIPLOMADOS-OFERTA-Fondo-Un-Ticket-para-el-Futuro.pdf",
                     pages="all", pandas_options={'header': None})
becas = pd.concat([ df[x] for x in range(len(df)) ], ignore_index=True)
becas.columns = becas.iloc[0]
becas.drop(0, axis=0, inplace= True)
becas["Nombre"] = becas["Nombre"].replace(["Fundación Universidad de Bogotá Jorge\rTadeo Lozano"],"Fundación Universidad de Bogotá Jorge Tadeo Lozano")
becas["Nombre"] = becas["Nombre"].replace(["Areandina - Fundación Universitaria del\rAreandina"],"Fundación Universitaria del Areandina")
becas.dropna(subset=["Nombre del programa"] , inplace=True)



# layout
app.layout= html.Div([

    html.H1("DashBoard becas Mintic ", style={'color':'orange', 'text-align':'center'}),
    html.H2("Acá encontrara la información sobre la oferta educativa respecto a becas de diplomados que ofrecerán ciertas universidades de Colombia junto con el MinTic",
    style={'color':'black', 'text-align':'center'}),

    dcc.Dropdown( id='selector-beca', multi=False, value='Universidad Nacional', options=becas['Nombre'].unique().tolist(),
    style={'width':'60%'}),
    dcc.Graph(id='tabla-becas', figure={}, style={'width':'100%'}),
    html.H5("+ info en: https://web.icetex.gov.co/es/-/un-ticket-para-el-futuro-pais-diplomado ", style={'color':'black', 'text-align':'center'}),
    html.H5("Codigo en: https://github.com/santigordillo15/Data-analysis-Pandas--Plotly--Dash/tree/Diplomados ", style={'color':'black', 'text-align':'center'})



])

# conectamos los plotly graphs con los dash components
@app.callback(

    Output(component_id='tabla-becas', component_property='figure'),
    [Input(component_id='selector-beca', component_property='value')]
)


  ##funcion callback
  ############### a continuacion filtraremos por universidad ###################
def update_graph(universidad):

    dff = becas.copy()

    dff = dff [ dff['Nombre']== universidad ] #nuevo Dataframe
    # graficamos la tabla
    #grafico1 = px.bar(dff,y ="NOMBRE INSTITUCIÓN", x="NOMBRE DEL PROGRAMA", title="becasXuniversidad ")
    grafico1 = go.Figure(data=[go.Table(header=dict(values=['Nombre del programa',"Ciudad","Modalidad" ]),
                 cells=dict(values=[dff['Nombre del programa'], dff['Ciudad'], dff.Modalidad],align='left'),
                  columnorder = [1,2,3], columnwidth = [200,50,50])
                     ])
    return grafico1

# corremos servidor
if __name__== '__main__':
    app.run_server(debug=True)

