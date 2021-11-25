#!/bin/bash

menuPrincipal(){
        echo "1)Opción 1. Probar Fortaleza."
        echo "2)Opción 2. Obtener “a” o “s”."
        echo "3)Opción 3. Guardar Informe."
        echo "4)Opción 4. Salir."
}

probarFortaleza(){
        echo "Ingrese la contraseña a probar."
        read contrasenia
        size=${#contrasenia}
        if [ $size -lt 3 ]; then
                echo "La contraseña es demasiado corta."
        fi
        if [[ ! $contrasenia =~ [0-9] ]]; then
                echo "Debe contener números."
        fi
        nueva=$(echo  "$contrasenia" | sed -e 's/[0-9]//g')
        retorno=$(cat ./diccionario.txt | grep -E "^$nueva{1}$")
        largoRetorno=${#retorno}
        if [[ ! largoRetorno -eq 0 ]]; then
                echo "Se encuentra en el diccionario"
        fi
}

obtenerAoS(){
        cat ./diccionario.txt | grep -E "^[s]|[a]$"
}

guardarInforme(){

        if [[ -d "./informes" ]]; then
                echo "Ya existe la carpeta informes"
        else
                mkdir informes
        fi

        if [[ -f "./informes/resultado.txt" ]]; then
                rm ./informes/letras.txt
        else
                touch ./informes/letras.txt
        fi
        date +%x_%X >> ./informes/letras.txt
        cat ./diccionario.txt | grep -E "^[s]|[a]$" >> ./informes/letras.txt
}

menuPrincipal
read opcion
while [ $opcion -ne 4 ]; do
        if [ $opcion = 1 ]; then
                probarFortaleza
        elif [ $opcion = 2 ]; then
                obtenerAoS
        elif [ $opcion = 3 ]; then
                guardarInforme
        else
                echo "No es una opción válida"
        fi
        menuPrincipal
        read opcion
done
exit
