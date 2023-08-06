from . import dir as __dir
from . import fechas as __fechas


import json as __json
import pandas as __pd
import datetime as __dt
import requests as __req
import pyodbc as __pyodbc


def fechas_para_consulta(fecha_ini, fecha_fin=None):
    
    fecha_ini, fecha_fin = __fechas.check_fechas(fecha_ini,fecha_fin)
    
    fecha_ini = fecha_ini.strftime('%Y-%m-%d')
    fecha_fin = fecha_fin.strftime('%Y-%m-%d')
    
    return fecha_ini, fecha_fin


def docs_by_nemo_rango(fecha_ini, fecha_fin=None,nemo=''):
    '''Consulta de PPOs a la API de CAMMESA'''
    
    fecha_ini, fecha_fin = fechas_para_consulta(fecha_ini, fecha_fin)
    
    url = 'https://api.cammesa.com/pub-svc/public/' + \
          'findDocumentosByNemoRango?' + \
          f'fechadesde={fecha_ini}T03%3A00%3A00.000%2B00%3A00&' + \
          f'fechahasta={fecha_fin}T03%3A00%3A00.000%2B00%3A00&' + \
          f'nemo={nemo}'
    
    r = __req.get(url)
    
    return __json.loads(r.text)

def consultar(fecha_ini, fecha_fin,nemo,exportar_consulta=False,dir_consulta=None):
    """Se ingresa con objetos datetime de fechas.
    Devuelve un dataframe de pandas con todos los archivos ppo encontrados en dicho rango.
    En caso de existir PPO inicial y final para una misma fecha, devuelve sólo el ppo final"""
    
    r_parsed = docs_by_nemo_rango(fecha_ini, fecha_fin,nemo=nemo)

    df_inicial = __pd.DataFrame(list(r_parsed))
    df_inicial['adjuntos'] = df_inicial['adjuntos'].apply(list)
    df_inicial['fecha'] = __pd.to_datetime(df_inicial['fecha'], format='%d/%m/%Y')

    registros_adjuntos = [x[0] for x in df_inicial['adjuntos']]
    df_adjuntos = __pd.DataFrame(registros_adjuntos).rename(columns={'id':'Archivo'})

    df_disp = df_inicial\
                .drop(labels='adjuntos',axis=1)\
                .join(df_adjuntos)\
                .sort_values(by=['Archivo','fecha'],ascending=[1,1])\
                .drop_duplicates(subset='Archivo',keep='last')
    
    if exportar_consulta:
        fecha_consulta = __dt.datetime.now().strftime('%Y.%m.%d %H.%M.%S')
        nombre_archivo = f"Consulta {nemo} {fecha_consulta}.xlsx"
        
        dir_consulta = '' if dir_consulta is None else dir_consulta + '\\'
        
        df_disp.to_excel(dir_consulta + nombre_archivo)
    
    del df_inicial, df_adjuntos

    return df_disp

def get_link_descarga(archivo,id_doc,nemo_doc):
    """Simplemente devuelve un string que sirve para descargar un archivo PPO"""
    
    if not(isinstance(archivo,str) and isinstance(id_doc,str) and isinstance(nemo_doc,str)):
        raise ValueError('Las variables de entrada deben ser todas del tipo string')
    
    link_descarga = 'https://api.cammesa.com/pub-svc/public/' + \
                    'findAttachmentByNemoId?' + \
                    f'attachmentId={archivo}&' + \
                    f'docId={id_doc}&' + \
                    f'nemo={nemo_doc}'
    
    return link_descarga

def descargar_reporte(archivo,id_doc,nemo,dir_descarga):

        link_descarga = get_link_descarga(archivo,id_doc,nemo)
        ruta_descarga = dir_descarga + "\\" + archivo

        print(f"Descargando: {archivo} {nemo}.")
        respuesta = __req.get(link_descarga)

        with open(ruta_descarga, 'wb') as f:
            f.write(respuesta.content)
            
def descargar_reportes(df,dir_descarga):
    """Toma un dataframe de pandas formateado según la función consultar().
    Recorre el mismo y descarga todos los archivos en la carpeta designada como 'dir_descarga'"""

    registro_de_archivos = df.loc[:,['Archivo','id','nemo']].to_dict(orient='records')

    for r in registro_de_archivos:

        archivo = r['Archivo']
        id =  r['id']
        nemo = r['nemo']
        
        descargar_reporte(archivo,id,nemo,dir_descarga)
        
        
def __get_lista_sql(lista_python):
    '''Tome un iterable de python y lo convierte a un string tipo lista SQL'''
    lista_sql = [f"\'{elemento}\'" for elemento in lista_python]
    lista_sql = ', '.join(lista_sql)
    lista_sql = f"({lista_sql})"
    
    return lista_sql

def procesar_mdb(archivos,parques,tabla_datos,col_parques,tabla_fecha):
    '''Toma una lista de archivos MDB en formato objeto Path y una lista de parques.
    Abre y filtra todos los archivos MDB por dichos parques y devuelve un df de pandas unificado
    
    archivos = Lista de objetos Path, apuntando a archivos .mdb con datos PPO de CAMMESA.
    parques = Listado de MNEMOTÉCNICOS de CAMMESA para filtrar la tabla df_ppo
    tabla = Tabla PPO a procesar.
    '''
    
    driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    
    SQL_datos = f'SELECT * FROM {tabla_datos} WHERE {col_parques} IN {__get_lista_sql(parques)};'
    SQL_fecha = f'SELECT * FROM {tabla_fecha};'

    rutas_archivos = [__dir.ruta_completa(archivo) for archivo in archivos]
    
    data_total = []
    encabezados = []
    for ruta_archivo in rutas_archivos:

        str_conexion = f"Driver={driver};DBQ={ruta_archivo};"

        conexion = __pyodbc.connect(str_conexion)
        cursor = conexion.cursor()

        data_archivo = cursor.execute(SQL_datos).fetchall()

        if not encabezados:
            encabezados = [x[0] for x in cursor.description]

        fecha_archivo = cursor.execute(SQL_fecha).fetchall()

        for index,_ in enumerate(data_archivo):
            data_archivo[index] = (fecha_archivo[0][0],) + tuple(data_archivo[index])

        data_total += data_archivo

    cursor.close()
    conexion.close()
    encabezados = ['Fecha' ] + encabezados

    df = __pd.DataFrame(data_total,columns=encabezados)
    df['Fecha'] = __pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    
    return df

def exportar(df,dir_out,parques,tabla=''):
    '''Exporta a excel un dataframe de pandas con una tabla carga del PPO de CAMMESA.
    Previamente filtra por un listado de MNEMOTÉCNICOS de CAMMESA (parques).
    
    df_ppo = Dataframe de Pandas con los partes PPO procesados por la función "procesar"
    parques = Listado de MNEMOTÉCNICOS de CAMMESA para filtrar la tabla df_ppo
    dir_out = String con la ruta completa a la carpeta en la cual se exportará el archivo Excel.
    tabla = Tabla PPO a procesar. Se utiliza sólo para nombrar el archivo de salida.
    '''
    
    fecha_desde_real = df.loc[:,"Fecha"].min().strftime('%y-%m-%d')
    fecha_hasta_real = df.loc[:,"Fecha"].max().strftime('%y-%m-%d')

    df.loc[:,"Fecha"] = df.loc[:,"Fecha"].dt.date

    if tabla:
        if len(parques) == 1: 
            nombre_archivo = f"\\{tabla}_{parques[0]} {fecha_desde_real} a {fecha_hasta_real}.xlsx"
        else:
            nombre_archivo = f"\\{tabla} {fecha_desde_real} a {fecha_hasta_real}.xlsx"
    else:
        if len(parques) == 1: 
            nombre_archivo = f"\\{parques[0]} {fecha_desde_real} a {fecha_hasta_real}.xlsx"
        else:
            nombre_archivo = f"\\{fecha_desde_real} a {fecha_hasta_real}.xlsx"

    df.to_excel(dir_out + nombre_archivo, index=False,engine='openpyxl')