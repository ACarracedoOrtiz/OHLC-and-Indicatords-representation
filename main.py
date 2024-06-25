import streamlit as st
from libs.OHLC.importar_datos import *
from libs.OHLC.dibujar_graficos import *
from libs.OHLC.fechas import *


# Configura Streamlit para utilizar el ancho completo de la página
st.set_page_config(layout="wide")

# Titulo de la página de Streamlit
st.title('Visualización de pares de monedas')

# Obtener el diccionario de pares de monedas
pares_monedas = pares_monedas()

# Crea un calendario para seleccionar las fechas
desde, hasta = selector_fecha()

# Crear un desplegable para que el usuario seleccione el par de monedas
par_moneda_elegido = st.sidebar.selectbox('Seleccione un par de monedas:', list(pares_monedas.keys()),
                                          format_func=lambda x: pares_monedas[x])

# Obtener el intervalo de tiempo (en minutos)
intervalo = st.sidebar.selectbox('Seleccione el intervalo de tiempo:', ['1440', '1', '5', '15', '30', '60',
                                                                                '240', '10080', '21600'])
# Descarga los datos llamando a la APi de Kraken y los devuelve como df
datos_cotizaciones = descargar_datos_cotizaciones(par_moneda_elegido, intervalo, desde=desde, hasta=hasta)

# Título para el gráfico
titulo = f'Par {pares_monedas[par_moneda_elegido]}'

# Añadir un botón en la barra lateral para mostrar/ocultar el estocástico
show_volumen = st.sidebar.checkbox('Mostrar Gráfico de Volumen', value=True)
show_stochastic = st.sidebar.checkbox('Mostrar Indicador Estocástico', value=True)
show_media_movil_vwap = st.sidebar.checkbox('Mostrar Media Móvil VWAP', value=True)

# Llamada a la función para dibujar el gráfico OHLC con velas
plot_ohlc_candlestick(datos_cotizaciones, titulo, show_volumen, show_stochastic, show_media_movil_vwap)

# Mostrar los primeros registros del DataFrame en Streamlit
st.write('Formato de datos:')
st.dataframe(datos_cotizaciones.head(20))
st.dataframe(datos_cotizaciones.tail(20))




