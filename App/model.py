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
from DISClib.DataStructures import listiterator as it
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
                '2019': None,
                '2020':None
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
    analyzer['2020'] = om.newMap(omaptype='RBT',
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
    
    lt.addLast(date_entry['accidents'], accident)
    addSeverityToDate(date_entry['severities'],accident)
    addStateToDate(date_entry['state'],accident)
    return map

def addSeverityToDate(dateEntry,accident):
    
    severity = accident['Severity']
    entry = m.get(dateEntry, severity)

    if entry is None:
        severity_entry = newSeverityEntry(accident)
        m.put(dateEntry , severity, severity_entry)
    else:
        severity_entry = me.getValue(entry)
        
    lt.addLast(severity_entry['listBySeverity'],accident)
    return dateEntry

def addStateToDate(dateEntry,accident):
    
    state = accident['State']
    entry = m.get(dateEntry, state)

    if entry is None:
        state_entry = newState(accident)
        m.put(dateEntry , state, state_entry)
    else:
        state_entry = me.getValue(entry)
        
    lt.addLast(state_entry['listByState'],accident)
    return dateEntry

def newDateEntry():
 
    entry = {'severities': None, 'accidents': None, 'categories': None, 'state':None}
    entry['severities'] = m.newMap(numelements=15,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
    entry['categories'] = m.newMap(numelements=15, maptype='PROBING',comparefunction=comparecategories)
   
    entry['state'] = m.newMap(numelements=15, maptype='PROBING',comparefunction=comparestates)

    entry['accidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newCategory(accident):
  
    category_entry = {'category': None, 'listByCategory': None}
    category_entry['category'] = accident['']
    category_entry['listByCategory'] = lt.newList('SINGLE_LINKED', comparecategories)
    return category_entry

def newState(accident):
  
    state_entry = {'state': None, 'listByState': None}
    state_entry['state'] = accident['State']
    state_entry['listByState'] = lt.newList('SINGLE_LINKED', comparestates)
    return state_entry

def newSeverityEntry(accident):
  
    severity_entry = {'severity': None, 'listBySeverity': None}
    severity_entry['severity'] = accident['Severity']
    severity_entry['listBySeverity'] = lt.newList('SINGLE_LINKED', compareSeverities)
    return severity_entry
# ==============================
# Funciones de consulta
# ==============================

def accisSize(analyzer):
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    return om.height(analyzer['date'])

def indexSize(analyzer):
    return om.size(analyzer['date'])

def minKey(analyzer):
    return om.minKey(analyzer['date'])

def maxKey(analyzer):
    return om.maxKey(analyzer['date'])

def getAccidentsByDate(analyzer, day):
    """
    Para una fecha determinada, retorna el numero de accidentes
    por severidad.
    """
    aDate = om.get(analyzer[str(day.year)], day)
    if aDate['key'] is not None:
        Accismap = me.getValue(aDate)['severities']
        sev=m.keySet(Accismap)
        iterator= it.newIterator(sev)
        totales=0
        while(it.hasNext(iterator)):
            severity1= it.next(iterator)
            numaccis = m.get(Accismap,severity1)
            lista= numaccis['value']
            cuantas = lt.size(lista['listBySeverity'])
            totales+=cuantas
            if lista is not None:
                print("severidad: "+ str(severity1) + " tiene : " +str(cuantas) +" accidentes")
        print("accidentes totales: "+str(totales))

def getAccidentsLast(analyzer, day):
    
    aDate = om.keys(analyzer['date'],om.minKey(analyzer['date']),day)
    iterator= it.newIterator(aDate)
    cuantos=0
    diaMayor=None
    cuantosMayor=0
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['date'],info)['value']
        cuantos += lt.size(valor['accidents'])
        if(lt.size(valor['accidents'])>cuantosMayor):
            cuantosMayor=lt.size(valor['accidents'])
            diaMayor=info
    print("accidentes totales: "+str(cuantos)+", la fecha con mayor accidentes es : "+str(diaMayor))

def getAccidentsState(analyzer, dayin, dayend):
    
    aDate = om.keys(analyzer['date'],dayin,dayend)
    iterator= it.newIterator(aDate)
    cuantos=0
    diaMayor=None
    cuantosMayor=0
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['date'],info)['value']
        cuantos += lt.size(valor['accidents'])
        llaves = m.keySet(valor['state'])
        iterator1= it.newIterator(llaves)
        while(it.hasNext(iterator1)):
            info1= it.next(iterator1)
            val = m.get(valor['state'], info1)['value']['listByState']
            if(lt.size(val)>cuantosMayor):
                cuantosMayor=lt.size(val)
                diaMayor=info1
    print("accidentes totales: "+str(cuantos)+", el estado con mayor accidentes es : "+str(diaMayor))

def getAccidentsCategory(analyzer, dayin, dayend):
    
    aDate = om.keys(analyzer['date'],dayin,dayend)
    iterator= it.newIterator(aDate)
    cuantos=0
    diaMayor=None
    cuantosMayor=0
    
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['date'],info)['value']
        cuantos += lt.size(valor['accidents'])
        if(lt.size(valor['accidents'])>cuantosMayor):
            cuantosMayor=lt.size(valor['accidents'])
            diaMayor=info
    print("accidentes totales: "+str(cuantos)+", la fecha con mayor accidentes es : "+str(diaMayor))
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

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else: 
        return -1

def compareSeverities(Sev1, Sev2):
    if (Sev1 == Sev2):
        return 0
    elif (Sev1 > Sev2) :
        return 1
    else:
        return -1

def comparecategories(cat1, cat2):
    if (cat1 == cat2):
        return 0
    elif (cat1 > cat2):
        return 1
    else:
        return -1

def comparestates(state1, state2):
    if (state1 == state2):
        return 0
    elif (state1 > state2) :
        return 1
    else:
        return -1