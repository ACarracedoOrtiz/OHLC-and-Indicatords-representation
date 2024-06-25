import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


#st.set_page_config(layout="wide")

# Dibuja todos los gráficos
def plot_ohlc_candlestick(df, titulo=None, show_volumen=True, show_stochastic=False, show_media_movil_vwap=False):
    """
    Función para crear y mostrar un gráfico de velas OHLC junto con gráficos opcionales de volumen y estocástico en Streamlit.
    inputs:
        df: DataFrame que contiene las columnas 'timestamp', 'open', 'high', 'low', 'close', 'volume', '%K', '%D'.
        titulo: Título opcional para el gráfico.
        show_volumen: Booleano para controlar la visualización del gráfico de volumen.
        show_stochastic: Booleano para controlar la visualización del indicador estocástico.
    """

    # Parametros para que el slider de fecha no se represente sobre otro gráfico
    espacio_entre_filas = 0.05  # Espacio entre subplots no adyacentes
    fila_espacio = 0.12  # Altura de la fila que actúa como espacio
    altura_grafico_principal = 0.5
    altura_otros_graficos = 0.25

    # Calcula las alturas de las filas teniendo en cuenta los espacios
    total_rows = 1 + int(show_volumen) + +int(show_stochastic)
    row_heights = [altura_grafico_principal] + [fila_espacio] + [altura_otros_graficos] * (total_rows - 1)

    # Crea un gráfico con los subgráficos necesarios
    fig = make_subplots(
        rows=total_rows + 1,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=espacio_entre_filas,
        subplot_titles=(
            'Cotización',
            '',
            'Volumen' if show_volumen else '',
            'Estocástico' if show_stochastic else ''
        ),
        row_heights=row_heights,
    )

    # Crea el gráfico OHLC
    candlestick = go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='OHLC'
    )
    fig.add_trace(candlestick, row=1, col=1)

    # Agrega un trazo vacío en la fila de "espacio"
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers'), row=2, col=1)

    if show_volumen:
        # Crear el gráfico de volumen
        volume_line = go.Scatter(
            x=df['timestamp'],
            y=df['volume'],
            name='Volumen',
            fill='tozeroy',
            line=dict(color='darkblue', width=2),
            fillcolor='lightblue'
        )
        fig.add_trace(volume_line, row=3, col=1)

    if show_stochastic:
        # Agregar los gráficos para el indicador estocástico
        stoch_k = go.Scatter(
            x=df['timestamp'],
            y=df['%K'],
            mode='lines',
            name='%K',
            line=dict(width=2)
        )
        stoch_d = go.Scatter(
            x=df['timestamp'],
            y=df['%D'],
            mode='lines',
            name='%D',
            line=dict(width=2)
        )
        fig.add_trace(stoch_k, row=total_rows + 1, col=1)
        fig.add_trace(stoch_d, row=total_rows + 1, col=1)

    if show_media_movil_vwap:
        # Agregar el gráfico para la media móvil del VWAP
        media_movil_vwap_line = go.Scatter(
            x=df['timestamp'],
            y=df['Media_Movil_VWAP'],
            mode='lines',
            name='Media Móvil VWAP',
            line=dict(color='purple', width=2)
        )
        fig.add_trace(media_movil_vwap_line, row=1, col=1)

    # Configurar las propiedades de los ejes y
    fig.update_yaxes(autorange=True, title_text="Cotización", row=1, col=1)
    if show_volumen:
        fig.update_yaxes(autorange=True, title_text="Volumen", row=3, col=1, showgrid=True, gridcolor='lightgray')
    if show_stochastic:
        fig.update_yaxes(autorange=True, title_text="Estocástico", row=total_rows + 1, col=1, showgrid=True,
                         gridcolor='lightgray')

    # Configurar el eje X para el gráfico OHLC con el RangeSlider
    fig.update_xaxes(
        tickformat='%b %d, %Y',
        row=1,  # Asegúrate de que este es el eje X para el gráfico OHLC
        col=1,
        rangeslider_visible=True  # Habilitar el RangeSlider solo para el gráfico OHLC
    )

    # Desactivar el RangeSlider para todos los otros subplots
    for i in range(2, total_rows + 1):
        fig.update_xaxes(
            tickformat='%b %d, %Y',
            row=i,
            col=1,
            rangeslider_visible=False
        )

    # Actualizar el diseño
    fig.update_layout(
        title=titulo,
        showlegend=False,
        height=1050
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


