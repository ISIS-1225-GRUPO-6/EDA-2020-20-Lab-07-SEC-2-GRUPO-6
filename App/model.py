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
                'date' : None,
                '2016': None,
                '2017': None,
                '2018': None,
                '2019': None
                }
    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)

    analyzer['date'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)

    analyzer['2016'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)

    analyzer['2017'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)

    analyzer['2018'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)

    analyzer['2019'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer
# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


# Funciones para agregar informacion al catalogo
def addAccident(analyzer,accident):
    dia = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(dia, '%Y-%m-%d %H:%M:%S')
    accidentYear = str(accidentDate.year)
    lt.addLast(analyzer['accidents'],accident)
    uptadeAccidentInDate(analyzer[accidentYear],accident)
    uptadeAccidentInDate(analyzer['date'],accident) 
    return analyzer

def uptadeAccidentInDate(map,accident):
    date = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentDate.date())

    if entry is None:
        date_entry = newDateEntry()
        om.put(map ,accidentDate.date(), date_entry)  
    else:
        date_entry = me.getValue(entry)
    
    addSeverityToDate(date_entry,accident)
    return map

def addSeverityToDate(dateEntry,accident):
    
    lt.addLast(dateEntry['accidents'],accident)
    severity = accident['Severity']
    entry = m.get(dateEntry['severities'], severity)

    if entry is None:
        severity_entry = newSeverityEntry(accident)
        m.put(dateEntry['severities'] , severity, severity_entry)
    else:
        severity_entry = me.getValue(entry)
        
    lt.addLast(severity_entry['listBySeverity'],accident)
    return dateEntry

def newDateEntry():
 
    entry = {'severities': None, 'Accidents': None}
    entry['severities'] = m.newMap(numelements=15,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
    entry['accidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newSeverityEntry(accident):
  
    severity_entry = {'severity': None, 'listBySeverity': None}
    severity_entry['severity'] = accident['Severity']
    severity_entry['listBySeverity'] = lt.newList('SINGLE_LINKED', compareSeverities)
    return severity_entry
# ==============================
# Funciones de consulta
# ==============================

def accisSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    return om.height(analyzer['date'])

def indexSize(analyzer):
    return om.size(analyzer['date'])

def minKey(analyzer):
    return om.minKey(analyzer['date'])

def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['date'])

def getAccidentsByDate(analyzer, day, severity):
    """
    Para una fecha determinada, retorna el numero de accidentes
    por severidad.
    """
    aDate = om.get(analyzer['date'], day)
    if aDate['key'] is not None:
        Accismap = me.getValue(aDate)['severities']
        numaccis = m.get(Accismap,severity)
        lista= numaccis['value']
        cuantas = lt.size(lista['listBySeverity'])
        if lista is not None:
            return cuantas
        return 0

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