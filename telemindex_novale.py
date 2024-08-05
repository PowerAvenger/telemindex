import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='centered')

df_in=pd.read_excel('telemindex_2023_2024.xlsx')

#con cambiar este valor ya sobra para filtrar la tabla
año=2024 
filtro_año=df_in['año']==año
dffa =df_in[filtro_año].set_index('fecha')

#usado como texto adicional en el gráfico
max_reg=dffa.index.max().strftime('%d-%m-%Y')

# Interacción en streamlit
lista_meses=dffa['mes_nombre'].unique().tolist()

orden_meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}
lista_meses=sorted(lista_meses,key=lambda x:orden_meses[x])
st.sidebar.text('Opciones')
#seleccion del año completo o por meses
rango=st.sidebar.selectbox('Seleccionar rango temporal',['Año completo', 'Por meses'] )
if rango =='Por meses': 
        box_mes=st.sidebar.selectbox('Seleccionar mes', lista_meses)
        mes=box_mes
else :
        mes =''

st.sidebar.write(f'El filtro es {mes}')

# %%
if mes is None: 
    dffm=dffa
else:
    mes_filtro=dffa['mes_nombre']==mes
    dffm=dffa[mes_filtro]


# %%
pt1=dffm.pivot_table(
    values=['spot','precio_2.0','precio_3.0','precio_6.1'],
    index='hora',
    aggfunc='mean'
)
pt1=pt1.reset_index()


# %% [markdown]
# ### Transponemos para visualizar en stremalit

# %%
pt1_trans=pt1.transpose()
pt1_trans=pt1_trans.drop(['hora'])
pt1_trans.columns.name='peajes'
pt1_trans=pt1_trans.round(2)


# %%
colores_precios = {'precio_2.0': 'goldenrod', 'precio_3.0': 'darkred', 'precio_6.1': 'blue'}

# %%
graf_pt1=px.line(pt1,x='hora',y=['precio_2.0','precio_3.0','precio_6.1'],
    height=600,
    width=1000,
    title="Telemindex 2024: Precios medios horarios de indexado según tarifas de acceso",
    labels={'value':'€/MWh','variable':'Precios s/ ATR'},
    color_discrete_map=colores_precios,
)
graf_pt1.update_traces(line=dict(width=4))


# %%
graf_pt1=graf_pt1.add_bar(y=pt1['spot'], name='spot', marker_color='green', width=0.5)
graf_pt1.update_layout(
    title_font_size=16,
    )


# %%
### Vamos a añadir un texto debajo del título
texto = f'Último día registrado: {max_reg}'

# %%
graf_pt1.add_annotation(
    dict(
        font=dict(size=12),
        x=0.5,
        y=1.05,
        showarrow=False,
        text=texto,
        xref="paper",
        yref="paper"
    )
)

# Actualizar el margen superior del gráfico para evitar superposición
graf_pt1.update_layout(margin=dict(t=100))

# %%






#elementos de la barra lateral





## Datos de la página principal
st.title("Telemindex 2024 webapp")
st.text("Tu aplicación para saber los precios minoristas de indexado")
st.plotly_chart(graf_pt1)
if st.checkbox ('Mostrar tabla de datos'): 
    st.write(pt1_trans)

