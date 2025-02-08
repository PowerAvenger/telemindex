import streamlit as st
from backend import leer_excel, filtrar_mes, aplicar_margen, pt1_trans, graf_pt1, pt5_trans, pt1, pt7_trans, costes_indexado
import pandas as pd


st.set_page_config(
    page_title="Telemindex",
    page_icon=":bulb:",
    layout='wide',
    menu_items={
        'Get help':'https://www.linkedin.com/in/jfvidalsierra/',
        'About':'https://www.linkedin.com/in/jfvidalsierra/'
        }
    )


# Inicializamos variables
if 'año_seleccionado' not in st.session_state:
    st.session_state.año_seleccionado = 2025
if 'mes_seleccionado' not in st.session_state: 
    st.session_state.mes_seleccionado = None
if 'margen' not in st.session_state: 
    st.session_state.margen = 0


# Cargamos datos
df_in = leer_excel()
df_filtrado, max_reg, lista_meses = filtrar_mes(df_in)

#ELEMENTOS DE LA BARRA LATERAL ---------------------------------------------------------------------------------------

st.sidebar.subheader('Opciones')
st.sidebar.selectbox('Seleccione el año', options = [2025,2024,2023], key = 'año_seleccionado')
#seleccion del año completo o por meses
rango = st.sidebar.radio("Seleccionar rango temporal", ['Año completo', 'Por meses'], key = "rango_temporal")
if rango =='Por meses' : 
    st.sidebar.selectbox('Seleccionar mes', lista_meses, key = 'mes_seleccionado')
    texto_precios = f'Mes seleccionado: {st.session_state.mes_seleccionado}'
elif rango == 'Año completo':
    st.session_state.mes_seleccionado = None  
    texto_precios = f'Año {st.session_state.año_seleccionado}, hasta el día {max_reg}'


if st.sidebar.checkbox('Marca si quieres añadir margen'):
    st.sidebar.slider("Añadir margen al gusto (en €/MWh)", min_value = 0, max_value = 50,value = 0, key = 'margen', on_change = aplicar_margen, args=(df_in,) )
    texto_margen=f'Se ha añadido {st.session_state.margen} €/MWh'
    st.sidebar.caption(texto_margen)
else:
    st.session_state.margen = 0  


#ejecutamos la función para obtener la tabla resumen y precios medios
tabla_precios, media_20, media_30, media_61, media_spot = pt5_trans(df_in)
media_20 = round(media_20 / 10, 1)
media_30 = round(media_30 / 10, 1)
media_61 = round(media_61 / 10, 1)
media_spot = round(media_spot, 2)

#tabla resumen de costes ATR
tabla_atr = pt7_trans(df_in)
tabla_costes = costes_indexado(df_in)





## Layout de la página principal
st.title("Telemindex 2023-2025 :orange[e]PowerAPP©")
st.subheader("Tu aplicación para saber los precios minoristas de indexado")
st.caption("Copyright by Jose Vidal :ok_hand:")
url_apps = "https://powerappspy-josevidal.streamlit.app/"
st.write("Visita mi página de [ePowerAPPs](%s) con un montón de utilidades" % url_apps)
url_linkedin = "https://www.linkedin.com/posts/josefvidalsierra_epowerapps-spo2425-telemindex-activity-7281942697399967744-IpFK?utm_source=share&utm_medium=member_deskto"
url_bluesky = "https://bsky.app/profile/poweravenger.bsky.social"
st.markdown(f"Deja tus comentarios y propuestas en mi perfil de [Linkedin]({url_linkedin}) - ¡Sígueme en [Bluesky]({url_bluesky})!")

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
    st.plotly_chart(graf_pt1(df_in))
    st.empty()
    st.subheader("Peso de los componentes por peaje de acceso", divider='rainbow')
    _, graf20, graf30, graf61=pt1(df_in)
    col10,col11,col12=st.columns(3)
    with col10:
        st.write(graf20)    
    with col11:
        st.write(graf30)
    with col12:
        st.write(graf61)    
    

with col2:
    
    st.subheader("Tabla resumen de precios por peaje de acceso", divider='rainbow')
    with st.expander("Nota sobre los precios de indexado:"):
        st.caption("Basados en las fórmulas tipo con todos los componentes de mercado y costes regulados. Se incluye FNEE, SRAD y 2€ en desvíos. Por supuesto peajes y cargos según tarifa de acceso. Añadir margen al gusto en 'Opciones' de la barra lateral")
        
    with st.container():

        tabla_margen = pd.DataFrame(columns = tabla_precios.columns, index = ['margen_2.0', 'margen_3.0', 'margen_6.1'])
        tabla_margen = tabla_margen.fillna(st.session_state.margen / 10)

        # Extraer el índice común (2.0, 3.0, 6.1) de los nombres de las filas
        #indices = ["2.0", "3.0", "6.1"]
        #for i in indices:
        #    tabla_atr.loc[f"pyc_{i}", "Media"] = (
        #        tabla_precios.loc[f"precio_{i}", "Media"] - tabla_costes.loc[f"coste_{i}", "Media"] - tabla_margen.loc[f"margen_{i}", "Media"]
        #        )
            
        texto_precios=f'{texto_precios}. Precios en c€/kWh'
        st.caption(texto_precios)

        st.text ('Precios medios de indexado', help='PRECIO MEDIO (FINAL) DE LA ENERGÍA.Suma de costes (energía y ATR)')
        st.dataframe(tabla_precios, use_container_width=True)
        
        st.text ('Costes medios de indexado', help = 'COSTE MEDIO DE LA ENERGÍA, sin incluir ATR.')
        st.dataframe(tabla_costes, use_container_width=True)
        
        st.text ('Costes de ATR')
        #tabla_atr['Media'] = (tabla_precios['Media'] - tabla_costes['Media']).fillna(0)
        st.dataframe(tabla_atr, use_container_width=True )
        
        st.text ('Margen')
        st.dataframe(tabla_margen, use_container_width=True )


        print(tabla_precios)
        print(tabla_costes)
        print(tabla_atr)
        #with col4:
        #if st.checkbox ('Mostrar tabla de datos de la gráfica'):
            #ejecutamos la función para obtener la tabla de valores de la gráfica 
        #    st.write(pt1_trans(df_in))




