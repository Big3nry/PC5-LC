import pandas as pd
import requests

def limpieza_datos(df):
    df.columns = [col.lower().replace(' ', '_').replace('í', 'i').replace('ó', 'o') for col in df.columns]

    df = df.loc[:, ~df.columns.duplicated()]

    df['dispositivo_legal'] = df['dispositivo_legal'].replace({'\.': ''}, regex=True)

    tipo_cambio_api = "https://apis.net.pe/api-tipo-cambio.htm"
    tipo_cambio_response = requests.get(tipo_cambio_api)
    tipo_cambio = float(tipo_cambio_response.json()["venta"])

    df['monto_inversion_usd'] = df['monto_de_inversion'] / tipo_cambio
    df['monto_transferencia_usd'] = df['monto_de_transferencia_2020'] / tipo_cambio

    estado_mapping = {
        'Actos Previos': 1,
        'Resuelto': 0,
        'Ejecución': 2,
        'Concluido': 3
    }
    df['estado'] = df['estado'].map(estado_mapping)

    return df

def generar_reportes(df):
    for region, region_group in df.groupby('region'):
        for estado in [1, 2, 3]:
            obras_filtradas = region_group[(region_group['tipo_moneda'] == 'Urbano') & (region_group['estado'] == estado)]
            top5_obras = obras_filtradas.nlargest(5, 'monto_inversion_usd')
            
            if not top5_obras.empty:
                nombre_archivo = f'top5_{region}_estado_{estado}.xlsx'
                top5_obras.to_excel(nombre_archivo, index=False)
                print(f"Reporte generado: {nombre_archivo}")

def almacenar_ubicaciones(df):
    ubigeos_unicos = df[['ubigeo', 'region', 'provincia', 'distrito']].drop_duplicates()
    print("Ubigeos almacenados en la base de datos.")

if __name__ == "__main__":
    archivo_excel = 'reactiva.xlsx'

    df_reactiva = pd.read_excel(archivo_excel)

    df_reactiva_procesado = limpieza_datos(df_reactiva)

    generar_reportes(df_reactiva_procesado)
    almacenar_ubicaciones(df_reactiva_procesado)
