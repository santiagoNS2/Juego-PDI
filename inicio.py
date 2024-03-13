#-------------------------------------------------------------------------------------------------
#------- DuckHunt -----------------------------------------------------------------------------
#------- Coceptos básicos de PDI------------------------------------------------------------------
#------- Por: Carolina jimenes - @udea.edu.co --------------------------------
#-------------Santiago Naranjo Sanchez - santiago.naranjo1@udea.edu.co-----------------------
#------- Presentado a: David Stephen Fernández MC CAN --------------------------------------------
#----------------------Profesor Facultad de Ingenieria BLQ 21-409  -------------------------------
#------- --------------CC 71629489, Tel 2198528,  Wpp 3007106588 ---------------------------------
#------- Curso Básico de Procesamiento de Imágenes y Visión Artificial----------------------------
#------- marzo de 2024-----------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------


#---------------------------------Inicio----------------------------------------------------------
import subprocess

archivo1 = "DuckHunt.py" #archivo principal
archivo2 = "Mouse.py"    #archivo control PDI

procesos = []

procesos.append(subprocess.Popen(["python", archivo1])) #abre el archivo principal
procesos.append(subprocess.Popen(["python", archivo2])) #abre el archivo control PDI

for proceso in procesos:                    #ciclo para cerrar los procesos
    proceso.wait()                          #espera a que el proceso termine

print("Todos los procesos han terminado")

#-----------------------------------------------------------------------------------------------
#---------------------------------Fin------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
