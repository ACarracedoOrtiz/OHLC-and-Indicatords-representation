import decimal
from datetime import datetime
import streamlit as st

#Gestiona el input de fechas y devuelve la fecha en formato decimal para poder pasar las fechas a la API de Kraken
def selector_fecha():
    hoy = datetime.now()
    hace_1_ano = datetime(hoy.year - 1, hoy.month, hoy.day)
    d = st.sidebar.date_input(
        "Selecciona el rango de fechas",
        (hace_1_ano.date(), hoy.date()), # Usamos .date() para obtener objetos date
        format="DD/MM/YYYY",
    )

    desde = datetime_a_decimal(datetime.combine(d[0], datetime.min.time()))  # Convierte date a datetime
    hasta = datetime_a_decimal(datetime.combine(d[1], datetime.min.time())) if len(d) > 1 else desde

    return desde, hasta


#Convierte las fechas a formato decimal
def datetime_a_decimal(fecha):
    if not isinstance(fecha, datetime):
        raise ValueError("El argumento proporcionado no es una fecha válida")

    numero_fecha = decimal.Decimal(fecha.timestamp())
    return numero_fecha
