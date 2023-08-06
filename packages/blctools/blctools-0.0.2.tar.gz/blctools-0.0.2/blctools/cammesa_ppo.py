
from . import dir as __dir
from . import fechas as __fechas
from . import cammesa_api as __api

import datetime as __dt
from pathlib import Path as __Path


def nombre(fecha):
    '''Toma una fecha determinada y devuelve un string indicando cómo debería llamarse el archivo PPO de dicho día'''
    return fecha.strftime('PO%y%m%d')

def nombres(fecha_ini, fecha_fin):
    '''Devuelve una lista con los nombres de los archivos PPO que habría entre dos fechas (inclusive)'''
    td = __dt.timedelta(days=1)
    fecha_fin += td
    iterable = __fechas.iterar_entre_timestamps(fecha_ini, fecha_fin, td)    
    
    return [nombre(fechas[0]) for fechas in iterable]

def fecha_archivo(nombre):
    '''Toma un nombre de archivo PPO y devuelve un objeto Datetime con la fecha a la que corresponde'''
    nombre = nombre.split('.')[0]
    
    return __dt.datetime.strptime(nombre,'PO%y%m%d')


def disponibles():
    '''Devuelve el nombre de todos los archivos disponibles en la carpeta MDB de los PPO'''
    dir_mdbs = __dir.get_dc_ppod() + '\\01 MDB'
    archivos_disponibles = __dir.filtra_archivos(__Path(dir_mdbs).iterdir(),'mdb')

    return archivos_disponibles

def __encontrar_procesables(fecha_ini,fecha_fin):
    '''Compila una lista de los nombres que tendrían los PPOS entre las fechas deseadas.
    Luego crea una la lista de archivos .mdb disponibles en la nube.
    
    Devuelve una lista de aquellos archivos que sean deseados y estén disponibles'''
    
    archivos_necesarios = nombres(fecha_ini,fecha_fin)
    archivos_disponibles = disponibles()

    archivos_a_procesar = __dir.encontrar_archivos_procesables(
        archivos_necesarios,
        archivos_disponibles
    )
    
    return archivos_a_procesar

def __encontrar_faltantes(fecha_ini,fecha_fin):
    '''Compara los archivos necesarios en el rango de fechas ingresadas y los archivos existentes.
    Devuelve lista de archivos faltantes como objetos path'''
    archivos_necesarios = nombres(fecha_ini,fecha_fin)
    archivos_disponibles = disponibles()

    archivos_faltantes = __dir.encontrar_archivos_faltantes(
        archivos_necesarios,
        archivos_disponibles
    )
    
    return archivos_faltantes

def consultar(fecha_ini, fecha_fin,exportar_consulta=False,dir_consulta=None):
    """Se ingresa con objetos datetime de fechas.
    Devuelve un dataframe de pandas con todos los archivos ppo encontrados en dicho rango.
    En caso de existir PPO inicial y final para una misma fecha, devuelve sólo el ppo final"""
    
    df_disponibles = __api.consultar(
        fecha_ini, 
        fecha_fin,
        nemo='PARTE_POST_OPERATIVO_UNIF',
        exportar_consulta=exportar_consulta,
        dir_consulta=dir_consulta
        )
    
    return df_disponibles

def descargar(fecha_ini, fecha_fin,exportar_consulta=False,dir_consulta=None):
    """Toma un dataframe de pandas formateado según la función consultar() del módulo cammesa_api.py.
    Recorre el mismo y descarga todos los archivos en la carpeta designada como 'dir_descarga' """

    dir_descarga = __dir.get_dc_ppod() + '\\00 ZIP'
    
    df = consultar(fecha_ini, fecha_fin,exportar_consulta=exportar_consulta,dir_consulta=dir_consulta)
    __api.descargar_reportes(df,dir_descarga)

def descargar_faltantes(fecha_ini,fecha_fin,exportar_consulta=False,dir_consulta=False):
    '''Ubica huecos de datos e intenta cubrirlos sin dejar huecos en el medio'''
    archivos_faltantes = __encontrar_faltantes(fecha_ini,fecha_fin)
    fechas_faltantes = [fecha_archivo(archivo) for archivo in archivos_faltantes]
    fechas_faltantes = sorted(fechas_faltantes)
    
    fecha_ini = fechas_faltantes[0]
    fecha_fin = fechas_faltantes[-1]
    
    descargar(fecha_ini, fecha_fin,exportar_consulta=exportar_consulta,dir_consulta=dir_consulta)
    
def extraer():
    '''Busca archivos zip en el directiorio dir_zips. 
    Luego extrae en el directorio dir_extraccion todos los archivos dentro del zip que terminen con la extensión provista '''

    dir_zips = __dir.get_dc_ppod() + '\\00 ZIP'
    dir_extraccion = __dir.get_dc_ppod() + '\\01 MDB'
    __dir.extraer(dir_zips, dir_extraccion,extension='mdb')

def cargar(fecha_ini,fecha_fin,parques,tabla_datos,descargar=False):
    '''Función que realiza la consulta en CAMMESA por PPOS en un rango de fechas, descarga los archivos .zip,
    extrae los archivos .mdb dentro de los archivos .zip, 
    filtra la tabla PPO seleccionada según el listado de parques provisto y 
    devuelve el resultado como un dataframe de pandas
    '''
    if descargar=='Faltantes':
        descargar_faltantes(fecha_ini,fecha_fin,exportar_consulta=False,dir_consulta=False)
        extraer(extension='mdb')
    elif descargar==True:
        descargar(fecha_ini, fecha_fin,exportar_consulta=False)
        extraer(extension='mdb')
        
    archivos_procesables = __encontrar_procesables(fecha_ini,fecha_fin)

    df_ppo = __api.procesar_mdb(archivos_procesables,parques,tabla_datos,col_parques='GRUPO',tabla_fecha='Fecha')

    return df_ppo


def a_excel(df,dir_out,parques,tabla_datos):
    '''
    Exportar DataFrame de pandas con algunas simplificaciones
    
    df = Dataframe con archivos MDB de CAMMESA procesados
    parques = Lista de parques contenidos en la exportación
    tabla_datos = Tabla de PPO a consultar (VALORES_GENERADORES / EnerRenovables / etc.)
    dir_out = String con la ruta completa a la carpeta en la cual se colocarán los archivos Excel resultantes del proceso
    '''

    __api.exportar(df,dir_out,parques,tabla_datos)





