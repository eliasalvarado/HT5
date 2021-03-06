'''
Autor: Elias Alvarado - 21808
Fecha: 13/03/2022
Simulador de memoria RAM con distinta cantidad de procesos los cuales tendran distintas instrucciones por completar.
Se utilizara para poder medir el tiempo utilizado en distintos escenarios.
'''

import simpy
import random

def proceso(noProceso, env, ram, procesadores, llegada, numInstruc, solicitud, velocidad):
    global tiempoTotal
    global tiempos
    
    yield env.timeout(llegada)
    llegadaProceso = env.now
    print(f"[NEW] - Proceso No.{noProceso} llego en {llegada} y solicita {solicitud} de memoria RAM. |{ram.level} de RAM disponible|")
    yield ram.get(solicitud)
    print(f"[ADMITTED] - Proceso No.{noProceso} recibio {solicitud}. |{ram.level} de RAM disponible|")
    
    while numInstruc != 0:
        print(f"[READY] - Proceso No.{noProceso} tiene {numInstruc} pendientes.")
        
        with procesadores.request() as req:
            yield req
            numInstruc -= velocidad
            if numInstruc < 0:
                numInstruc = 0
            yield env.timeout(1)
            print(f"[RUNNING] - Se han ejecutado {velocidad} instrucciones del Proceso No.{noProceso} tiene {numInstruc} pendientes. |{ram.level} de RAM disponible|")
            
        if numInstruc > 0:
            wating = random.randint(1,2)
            if wating == 1:
                print(f"[WAITING] - Proceso No.{noProceso} realizando operaciones I/O.")
                yield env.timeout(1)
    yield ram.put(solicitud)
    print("[TERMINATED] - Proceso No.{:.0f} termino sus instrucciones en {:.2f}s, se dispone de {:.0f} mas de memoria. |{:.0f} de RAM disponible|".format(noProceso,env.now,solicitud,ram.level))
    tiempos.append(env.now - llegadaProceso)
    tiempoTotal += (env.now - llegadaProceso)
    print("Proceso No.{:.0f} tardo {:.2f}s.".format(noProceso,env.now - llegadaProceso))

random.seed(213)

tiempoTotal = 0
tiempos = []
#------------------
numProcesos = 200    #Numero de procesos
velocidad = 3       #Cantidad de procesos que realiza en un tiempo
capacidadRam = 100  #Capacidad de la RAM
numProcesadores = 2 #Numero de CPUs
intervalos = 1     #Llegada de los procesos
#-----------------
env = simpy.Environment()
ram = simpy.Container(env, init = capacidadRam, capacity = capacidadRam)
procesadores = simpy.Resource(env, capacity = numProcesadores)

for noProceso in range(numProcesos):
    llegada = random.expovariate(1.0 / intervalos)
    numInstruc = random.randint(1, 10)
    solicitud = random.randint(1, 10)
    env.process(proceso(noProceso, env, ram, procesadores, llegada, numInstruc, solicitud, velocidad))

env.run()

tiempoPromedio = (tiempoTotal / numProcesos)
suma = 0
for i in tiempos:
    suma += (i - tiempoPromedio)**2
desviacionEst = (suma/(numProcesos-1))**0.5
print("---------------------INFORMACION------------------------------")
print("\tTiempo promedio: {:.2f} segundos".format(tiempoPromedio))
print("\tDesviacion Estandar: {:.2f} segundos".format(desviacionEst))




