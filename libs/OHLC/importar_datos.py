import krakenex
import pandas as pd


# Descarga los datos OHLC de la cotización necesaria
def descargar_datos_cotizaciones(par_moneda, intervalo, desde=None, hasta=None):
    """
    Descarga los datos de cotizaciones desde Kraken y los guarda en un DataFrame.
    Inputs:
        par_moneda: Par de monedas a descargar (por ejemplo, 'XBTUSD' para Bitcoin/USD).
        Intervalo: Intervalo de tiempo de las cotizaciones (en minutos).
        Desde: Fecha de inicio en formato decimal.
        Hasta: Fecha de fin en formato decimal.
    Return:
        DataFrame de Pandas con los datos de cotizaciones.
    """
    # Realiza la conexión con Kraken
    k = krakenex.API()

    # Parámetros para la consulta
    params = {'pair': par_moneda, 'interval': intervalo}

    # Agrega las fechas si se especifican
    if desde:
        params['since'] = desde

    # Realiza la consulta para recibir los datos OHLC según los parámetros, devuelve un diccionario
    respuesta = k.query_public('OHLC', data=params)

    # Accede a las claves 'result' y 'par_moneda' y devuelve una lista compuesta de listas con los datos
    datos = respuesta['result'][par_moneda]

    # Se establecen las columnas del DataFrame
    # Timestamp: Marca de tiempo
    # Vwap: Precio Promedio Ponderado por volumen
    # Volumen: Volumen total de activos negociados
    columnas = ['timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']

    # Se crea el DF con los datos
    df = pd.DataFrame(datos, columns=columnas)

    # Filtra la fecha final
    df = df[(df['timestamp'] >= desde) & (df['timestamp'] <= hasta)]

    # Convierte el timestamp a formato de fecha
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Se llama a las funciones para añadir el estocástico y la media móvil al DF
    df = calcular_estocastico(df)
    df = calcular_media_movil_vwap(df)

    return df


# Importa un diccionario con los pares de monedas disponibles en kraken
def pares_monedas():
    # Crear una instancia del cliente API de Kraken
    k = krakenex.API()

    # Obtener la lista de todos los pares de monedas disponibles en Kraken
    response = k.query_public('AssetPairs')

    # Inicializar un diccionario vacío para los pares de monedas
    currency_pairs_dict = {}

    # Verificar si la respuesta es válida
    if 'result' in response:
        # Iterar sobre cada par de monedas en el resultado
        for pair, details in response['result'].items():
            # Obtener el nombre legible del par de monedas
            nombre_par = details.get('wsname')

            # Si el nombre del par existe, lo agrega al diccionario junto a su identificador
            if nombre_par:
                currency_pairs_dict[pair] = nombre_par

    return currency_pairs_dict


# Calcula y añade en dos nuevas columnas %K y %D para graficar el estocástico
def calcular_estocastico(df, k_period=14, d_period=3):
    # Asegúrate de que 'close', 'low' y 'high' sean de tipo float
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')

    # Inicializa las columnas para %K y %D
    df['%K'] = None
    df['%D'] = None

    for i in range(len(df)):
        # Determina el período actual para el cálculo
        current_period = min(i + 1, k_period)

        # Calcula el %K con el período actual
        low_min = df['low'][max(0, i - current_period + 1):i + 1].min()  # Minimo del último periodo
        high_max = df['high'][max(0, i - current_period + 1):i + 1].max()  # Máximo del último periodo
        df.loc[i, '%K'] = ((df.loc[i, 'close'] - low_min) / (high_max - low_min)) * 100 if high_max > low_min else 0

    # Calcula el %D después de completar todos los %K
    for i in range(len(df)):
        current_period = min(i + 1, d_period)
        k_sum = df['%K'][max(0, i - current_period + 1):i + 1].sum()
        df.loc[i, '%D'] = k_sum / current_period

    return df


# Añade una columna con la media móvil del Vwap
def calcular_media_movil_vwap(df, periodo=14):
    # Asegura que 'vwap', 'volume' sean de tipo float
    df['vwap'] = pd.to_numeric(df['vwap'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')

    # Inicializa la columna para la media móvil del VWAP
    df['Media_Movil_VWAP'] = None

    for i in range(len(df)):
        # Determina el período actual para el cálculo
        current_period = min(i + 1, periodo)

        # Calcula la media móvil del VWAP
        vwap_sum = df['vwap'][max(0, i - current_period + 1):i + 1].sum()
        df.loc[i, 'Media_Movil_VWAP'] = vwap_sum / current_period

    return df
