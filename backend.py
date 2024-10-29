# %% [markdown]
# # Telemindex

# %% [markdown]
# ## Importamos librerías

# %%
#En pruebas: Uso de la variables mes_seleccionado definida en el archivo 'globals.py'

# %%
import pandas as pd
import plotly.express as px
import globals

# %% [markdown]
# ## Importamos el fichero excel

# %%
df_in=pd.read_excel('data.xlsx')
df_in

# %% [markdown]
# ## Filtramos por el año 2024

# %%
año=2024 #con cambiar este valor ya sobra para filtrar la tabla
filtro_año=df_in['año']==año
dffa =df_in[filtro_año].set_index('fecha')
dffa 

# %% [markdown]
# ### Obtenemos el último registro

# %%
#usado como texto adicional en el gráfico si rango = todo el año
max_reg=dffa.index.max().strftime('%d-%m-%Y')
max_reg
texto_graf=f'Último día registrado: {max_reg}'


# %% [markdown]
# ### Interacción en streamlit: Listado de meses disponibles para usar en un select_box

# %%
lista_meses=dffa['mes_nombre'].unique().tolist()
lista_meses

# %%
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

# %%
lista_meses=sorted(lista_meses,key=lambda x:orden_meses[x])
lista_meses

# %% [markdown]
# ## Telemindex horario para streamlit

# %% [markdown]
# ### Inicializamos dffm, que es el la tabla filtrada por el usuario

# %%
dffa_copia=dffa.copy()

# %% [markdown]
# ## Filtramos el mes seleccionado por el usuario

# %%
def filtrar_mes(mes_seleccionado=None):
        if mes_seleccionado is None: 
                dffm=dffa_copia
        else:
                mes_filtro=dffa_copia['mes_nombre']==mes_seleccionado
                dffm=dffa_copia[mes_filtro]
                #texto_graf=f'{mes}'
        return dffm #,texto_graf
        


# %%
def aplicar_margen(mes_seleccionado,margen_aplicado):
    dffa_copia['precio_2.0']=dffa['precio_2.0'] #+=margen_aplicado #=dffm['precio_2.0']+margen
    dffa_copia['precio_3.0']=dffa['precio_3.0'] #+=margen_aplicado #dffm['precio_3.0']+margen
    dffa_copia['precio_6.1']=dffa['precio_6.1'] #+=margen_aplicado #dffm['precio_6.1']+margen
    dffa_copia['precio_2.0']+=margen_aplicado #=dffm['precio_2.0']+margen
    dffa_copia['precio_3.0']+=margen_aplicado #dffm['precio_3.0']+margen
    dffa_copia['precio_6.1']+=margen_aplicado #dffm['precio_6.1']+margen
    
    filtrar_mes(mes_seleccionado)

    return dffa_copia

# %% [markdown]
# ### De esta tabla sale el gráfico

# %%
def pt1():
    dffm=filtrar_mes(globals.mes_seleccionado)
    
    pt1=dffm.pivot_table(
        values=['spot','precio_2.0','precio_3.0','precio_6.1'],
        index='hora',
        aggfunc='mean'
    ).reset_index()

    pt20=dffm.pivot_table(
        values=['spot', 'ssaa', 'osom', 'Otros', 'ppcc_2.0', 'perd_2.0', 'pyc_2.0'],
        index='año',
        aggfunc='mean'
    )
    pt20['comp_perd']=pt20['spot']+pt20['ssaa']+pt20['osom']+pt20['Otros']+pt20['ppcc_2.0']
    pt20['perdidas_2.0']=pt20['comp_perd']*(pt20['perd_2.0'])
    pt20=pt20.drop(columns=['perd_2.0','comp_perd'])
    pt20_trans=pt20.transpose().reset_index()
    pt20_trans=pt20_trans.rename(columns={'index':'componente',2024:'valor'})
    pt20_trans['componente'] = pt20_trans['componente'].replace({'Otros': 'otros'})
    pt20_trans=pt20_trans.sort_values(by='valor',ascending=False)
    pt20_trans['valor']=round(pt20_trans['valor'],2)
    graf20=px.pie(pt20_trans,names='componente',values='valor', hole=.3, color_discrete_sequence=px.colors.sequential.Oranges_r)
    graf20.update_layout(
          title={'text':'Peaje de acceso 2.0','x':.5,'xanchor':'center'}
    )

    pt30=dffm.pivot_table(
        values=['spot', 'ssaa', 'osom', 'Otros', 'ppcc_3.0', 'perd_3.0', 'pyc_3.0'],
        index='año',
        aggfunc='mean'
    )
    pt30['comp_perd']=pt30['spot']+pt30['ssaa']+pt30['osom']+pt30['Otros']+pt30['ppcc_3.0']
    pt30['perdidas_3.0']=pt30['comp_perd']*(pt30['perd_3.0'])
    pt30=pt30.drop(columns=['perd_3.0','comp_perd'])
    pt30_trans=pt30.transpose().reset_index()
    pt30_trans=pt30_trans.rename(columns={'index':'componente',2024:'valor'})
    pt30_trans['componente'] = pt30_trans['componente'].replace({'Otros': 'otros'})
    pt30_trans=pt30_trans.sort_values(by='valor',ascending=False)
    pt30_trans['valor']=round(pt30_trans['valor'],2)
    graf30=px.pie(pt30_trans,names='componente',values='valor', hole=.3, color_discrete_sequence=px.colors.sequential.Reds_r)
    graf30.update_layout(
          title={'text':'Peaje de acceso 3.0','x':.5,'xanchor':'center'}
    )

    pt61=dffm.pivot_table(
        values=['spot', 'ssaa', 'osom', 'Otros', 'ppcc_6.1', 'perd_6.1', 'pyc_6.1'],
        index='año',
        aggfunc='mean'
    )
    pt61['comp_perd']=pt61['spot']+pt61['ssaa']+pt61['osom']+pt61['Otros']+pt61['ppcc_6.1']
    pt61['perdidas_6.1']=pt61['comp_perd']*(pt61['perd_6.1'])
    pt61=pt61.drop(columns=['perd_6.1','comp_perd'])
    pt61_trans=pt61.transpose().reset_index()
    pt61_trans=pt61_trans.rename(columns={'index':'componente',2024:'valor'})
    pt61_trans['componente'] = pt61_trans['componente'].replace({'Otros': 'otros'})
    pt61_trans=pt61_trans.sort_values(by='valor',ascending=False)
    pt61_trans['valor']=round(pt61_trans['valor'],2)
    graf61=px.pie(pt61_trans,names='componente',values='valor', hole=.3, color_discrete_sequence=px.colors.sequential.Blues_r)
    graf61.update_layout(
          title={'text':'Peaje de acceso 6.1','x':.5,'xanchor':'center'}
    )
    
    return pt1, graf20, graf30, graf61

# %%
pt1()

# %% [markdown]
# ### Transponemos para visualizar en stremalit

# %%
def pt1_trans():
    pt2=pt1()[0]
    pt1_trans=pt2.transpose()
    pt1_trans=pt1_trans.drop(['hora'])
    pt1_trans.columns.name='peajes'
    pt1_trans=pt1_trans.round(2)
    
    return pt1_trans

# %% [markdown]
# ### Gráfico de salida para visualizar en streamlit

# %%
def graf_pt1():
    pt2=pt1()[0]
    colores_precios = {'precio_2.0': 'goldenrod', 'precio_3.0': 'darkred', 'precio_6.1': 'blue'}
    graf_pt1=px.line(pt2,x='hora',y=['precio_2.0','precio_3.0','precio_6.1'],
        height=600,
        #width=1000,
        title="Telemindex 2024: Precios medios horarios de indexado según tarifas de acceso",
        labels={'value':'€/MWh','variable':'Precios s/ ATR'},
        color_discrete_map=colores_precios,
    )
    graf_pt1.update_traces(line=dict(width=4))
    graf_pt1.add_annotation(
        dict(
            font=dict(size=12),
            x=0.5,
            y=1.05,
            showarrow=False,
            text=texto_graf,
            xref="paper",
            yref="paper"
        )
    )
    graf_pt1.update_layout(
        margin=dict(t=100),
        title_font_size=16,
        title={'x':.5,'xanchor':'center'},
        xaxis=dict(
              tickmode='array',
              tickvals=pt2['hora']
        )
    )
    graf_pt1=graf_pt1.add_bar(y=pt2['spot'], name='spot', marker_color='green', width=0.5)
    
    return graf_pt1

# %% [markdown]
# ## Obtención de la tabla resumen de precios

# %%
#dffm=filtrar_mes(globals.mes_seleccionado)
def pt5_trans():
        dffm=filtrar_mes(globals.mes_seleccionado)    
        pt3=dffm.pivot_table(
                values=['precio_2.0'],
                aggfunc='mean',
                index='dh_3p'
                )
        pt4=dffm.pivot_table(
                values=['precio_3.0','precio_6.1'],
                aggfunc='mean',
                index='dh_6p',
                )
        pt5=pd.concat([pt3,pt4],axis=1)
        
        
        media_20=dffm['precio_2.0'].mean()
        media_30=dffm['precio_3.0'].mean()
        media_61=dffm['precio_6.1'].mean()
        media_spot=dffm['spot'].mean()
        precios_medios=[media_20,media_30,media_61]
        pt5_trans=pt5.transpose()
        pt5_trans['Media']=precios_medios
        pt5_trans=pt5_trans.div(10)
        pt5_trans=pt5_trans.round(1)
        pt5_trans=pt5_trans.fillna('')

        return pt5_trans, media_20,media_30,media_61,media_spot

        



