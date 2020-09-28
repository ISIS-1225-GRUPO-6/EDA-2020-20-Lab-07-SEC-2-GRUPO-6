"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""
def newAnalyzer():
    analyzer = { 'accidents': None,
                'date' : None
                }
    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['date'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return analyzer
# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


# Funciones para agregar informacion al catalogo
def addAcci(analyzer, acci):
    lt.addLast(analyzer['accidents'], acci)
    updateDateIndex(analyzer['date'], acci)
    return analyzer

def updateDateIndex(map, acci):

    occurreddate = acci['Start_Time']
    accidate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidate.date())
    if entry is None:
        datentry = newDataEntry(acci)
        om.put(map, accidate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDate(datentry, acci)
    return map

def newDataEntry(acci):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severity': None, 'lstacci': None}
    entry['severity'] = m.newMap(numelements=3,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
    entry['lstacci'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def addDate(datentry, acci):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstacci']
    lt.addLast(lst, acci)
    sevIndex = datentry['severity']
    seventry = m.get(sevIndex, acci['Severity'])
    if (seventry is None):
        entry = newSevEntry(acci['Severity'], acci)
        lt.addLast(entry['lstsev'], acci)
        m.put(sevIndex, acci['Severity'], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry['lstsev'], acci)
    return datentry

def newSevEntry(sevgroup, acci):#Esta crea severidad y una lista de severidades(?)
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    sventry = {'seve': None, 'lstsev': None}
    sventry['seve'] = sevgroup
    sventry['lstsev'] = lt.newList('SINGLELINKED', compareSeverities)
    return sventry
# ==============================
# Funciones de consulta
# ==============================

def accisSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['date'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['date'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['date'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['date'])

# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareSeverities(Sev1, Sev2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    Sev = me.getKey(Sev2)
    if (Sev1 == Sev):
        return 0
    elif (Sev1 > Sev):
        return 1
    else:
        return -1