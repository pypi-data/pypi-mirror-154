import datetime as __dt

def hora_op(fecha):
    if fecha.minute == 0:
        if fecha.hour == 0:
            hora_op = 24
        else:
            hora_op = fecha.hour
    else:
        hora_op = fecha.hour +1
    
    return hora_op

def fecha_op(fecha):  
    if hora_op(fecha) == 24 :
        if fecha.hour == 0:
            return (fecha.date() + __dt.timedelta(days=-1))
        else:
            return fecha.date()
    else:
        return fecha.date()
    
def iterar_entre_timestamps(ts_ini,ts_fin,timedelta):
    '''Itera entre dos objetos datetime. 
    El intervalo de iteración está dado por el objeto timedelta'''
    
    td = timedelta
    ts_loop = ts_ini
    ts_loop_end = ts_fin - td
    
    while ts_loop <= ts_loop_end:
        
        if ts_loop == ts_ini:
            ts_cur_ini = ts_ini
            ts_cur_end = ts_ini + td

        elif ts_loop == ts_loop_end:
            ts_cur_ini = ts_loop_end
            ts_cur_end = ts_fin
            
        else:
            ts_cur_ini = ts_loop
            ts_cur_end = ts_loop + td

        yield ts_cur_ini,ts_cur_end
        
        ts_loop += td
        
def sumar_mes(fecha):
    
    if fecha.month == 12:
        return fecha.replace(year=fecha.year +1, month=1)
    else:
        return fecha.replace(month=fecha.month +1)

def iterar_mensual(ts_ini,ts_fin):
    '''Itera entre dos objetos datetime, mensualmente.
    Descarta los valores diarios y horarios que tengan las fechas ingresadas.
    Sólo tomará los valores de año y mes'''
    
    ts_ini, ts_fin = check_fechas(ts_ini,ts_fin)
    
    ts_ini = ts_ini.replace(day=1)
    ts_fin = ts_fin.replace(day=1)
    
    ts_loop = ts_ini
    ts_loop_end = sumar_mes(ts_fin)

    while ts_loop < ts_fin:

        if ts_loop == ts_ini:
            ts_cur_ini = ts_ini
            ts_cur_end = sumar_mes(ts_ini)

        else:
            ts_cur_ini = ts_loop
            ts_cur_end = sumar_mes(ts_loop)

        yield ts_cur_ini,ts_cur_end
        
        ts_loop = sumar_mes(ts_loop)
        

def input_fecha(nombre=''):
    '''Se prueban distintas combinaciones para reconocer el formato de fecha ingresado en el input.
    Luego se ajusta el formato de la fecha al formato requerido por la API de CAMMESA.'''

    if not isinstance(nombre,str):
        raise ValueError('La variable "nombre" debe ser del tipo string')

    while True:
        fecha = input(f'- Ingresar fecha {nombre}: \n')
        try:
            fecha = __dt.datetime.strptime(fecha, '%d/%m/%y')
            break
        except ValueError:
            try:
                fecha = __dt.datetime.strptime(fecha, '%d/%m/%Y')
                break
            except:
                try:
                    fecha= __dt.datetime.strptime(fecha, '%d-%m-%y')
                    break
                except:
                    try:
                        fecha= __dt.datetime.strptime(fecha, '%d-%m-%Y')
                        break
                    except:
                        raise ValueError('Formato de fecha no reconocido.')
    return fecha
 
    
def input_fechas(**kwargs):
    '''Toma un conjunto de key-value pairs para solicitar fechas al usuario.
    Los valores deberían ser indicativos del tipo de fecha que se espera, ejemplos:
    
    "Inicial", "Final", etc. '''
    
    fechas = []
    
    for k,v in kwargs.items():
        if not (isinstance(k,str) and isinstance(v,str)):
            raise ValueError(f'Las variables {k} {v} ingresadas deben ser del tipo string')
        else:
            fechas.append(input_fecha(v))

    return fechas


def check_fechas(fecha_ini,fecha_fin):
    
    if not isinstance(fecha_ini,__dt.datetime):
        raise ValueError('La variable "fecha_ini" debe ser un objeto datetime.datetime')
    
    if not fecha_fin:
        fecha_fin=fecha_ini
    elif not isinstance(fecha_fin,__dt.datetime):
        raise ValueError('La variable "fecha_fin" debe ser un objeto datetime.datetime')
    
    if fecha_fin < fecha_ini:
        return fecha_fin, fecha_ini
    else:
        return fecha_ini, fecha_fin
    
