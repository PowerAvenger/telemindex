import streamlit as st
import pandas as pd
import plotly.express as px
import globals

from backend import  max_reg, lista_meses, aplicar_margen, pt1_trans, graf_pt1, pt5_trans, pt1



st.set_page_config(
    page_title="Telemindex",
    page_icon=":bulb:",
    layout='wide',
    menu_items={
        'Get help':'https://www.linkedin.com/in/jfvidalsierra/',
        'About':'https://www.linkedin.com/in/jfvidalsierra/'
        }
    )

if 'mes_seleccionado' not in st.session_state: 
    st.session_state.mes_seleccionado= None
if 'margen' not in st.session_state: 
    st.session_state.margen = 0

#elementos de la barra lateral

st.sidebar.subheader('Opciones')
#seleccion del año completo o por meses
rango=st.sidebar.radio("Seleccionar rango temporal", ['Año completo', 'Por meses'], key="rango_temporal")
if rango =='Por meses' : 
    st.sidebar.selectbox('Seleccionar mes', lista_meses, key='mes_seleccionado')
    texto_precios = f'Mes seleccionado: {st.session_state.mes_seleccionado}'
elif rango=='Año completo':
    st.session_state.mes_seleccionado=None  
    texto_precios = f'Año 2024, hasta el día {max_reg}'

globals.mes_seleccionado=st.session_state.mes_seleccionado
#ejecutamos la función para obtener el mes seleccionado
#y que sea usado en backend.py


if st.sidebar.checkbox('Marca si quieres añadir margen'):
    globals.margen_aplicado=st.sidebar.slider("Añadir margen al gusto (en €/MWh)", min_value=0, max_value=50,value=0) #key="margen"
    texto_margen=f'Se ha añadido {globals.margen_aplicado} €/MWh'
    st.sidebar.caption(texto_margen)
    #st.session_state.margen
else:
    #st.session_state.margen=0
    globals.margen_aplicado=0  

#globals.margen_aplicado=st.session_state.margen
#aplicar_margen(globals.margen_aplicado)
aplicar_margen(globals.mes_seleccionado,globals.margen_aplicado)
#filtrar_mes(globals.mes_seleccionado)


#esta linea sobrará
#st.sidebar.write("st.session_state object:", st.session_state)

#ejecutamos la función para obtener la tabla resumen y precios medios
pt6_trans, media_20, media_30, media_61, media_spot=pt5_trans()
media_20 =round(media_20 / 10,1)
media_30 =round(media_30 / 10,1)
media_61 =round(media_61 / 10,1)
media_spot=round(media_spot,2)
#ejecutamos la función para graficar
#graf_pt2=graf_pt1()
#ejecutamos la función para obtener la tabla de valores de la gráfica
pt1_trans2=pt1_trans()



## Layout de la página principal
st.title("Telemindex 2024 webapp")
st.subheader("Tu aplicación para saber los precios minoristas de indexado")
st.caption("Copyright by Jose Vidal :ok_hand:")
url_apps = "https://powerappspy-josevidal.streamlit.app/"
st.write("Visita mi página de [PowerAPPs](%s) con un montón de utilidades" % url_apps)


col1, col2 = st.columns([.7,.3])

#COLUMNA PRINCIPAL
with col1:
    st.subheader("Resumen de precios medios minoristas por peaje de acceso. Totales y horarios.", divider='rainbow')
    st.caption(texto_precios)
    with st.container():
        col5, col6,col7,col8=st.columns(4)
        with col5:
            st.metric(':orange[Precio medio 2.0]',value=media_20)
        with col6:
            st.metric(':red[Precio medio 3.0]',value=media_30)
        with col7:
            st.metric(':blue[Precio medio 6.1]',value=media_61)
        with col8:
            st.metric(':green[Precio medio Spot €/MWh]',value=media_spot)
    st.empty()
    st.plotly_chart(graf_pt1())
    st.empty()
    st.subheader("Peso de los componentes por peaje de acceso", divider='rainbow')
    _, graf20, graf30, graf61=pt1()
    col10,col11,col12=st.columns(3)
    with col10:
        st.write(graf20)    
    with col11:
        st.write(graf30)
    with col12:
        st.write(graf61)    
    

with col2:
    
    st.subheader("Tabla resumen de precios por peaje de acceso", divider='rainbow')
    with st.container():
        #col3, col4=st.columns([0.65,0.35])
        #with col3:
        texto_precios=f'{texto_precios}. Precios en c€/kWh'
        st.caption(texto_precios)
        st.write(pt6_trans,)
        #with col4:
        with st.expander("Nota sobre la Fórmula de indexado:"):
            st.caption("Se incluye fnee, SRAD y 2€ en desvíos. Añadir margen al gusto en 'opciones' de la barra lateral")
        if st.checkbox ('Mostrar tabla de datos de la gráfica'): 
            st.write(pt1_trans2)




