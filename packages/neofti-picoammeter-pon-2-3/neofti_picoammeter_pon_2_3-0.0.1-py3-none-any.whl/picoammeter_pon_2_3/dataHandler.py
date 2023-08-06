#Project module

#Third party module

import numpy as np
#Python module



ELEMENTARYCHARGE:float = 1.6 *10**-19

def __getCoulombByVoltageCh1__(voltage:float):
    charge = 3.9*10**-10
    return  ((-voltage + 8) *charge * 10**-3)*0.1-3*10**(-10)    
def __getCoulombByVoltageCh2__(voltage:float):
    charge = 10**-10
    return  (((-voltage + 36) *charge * 10**-3)*0.3-9*10**(-11))*3.2
def __getCoulombByVoltageCh3__(voltage:float):
    charge = 4*10**-11
    return  ((-voltage + 85)*charge * 10**-3)*0.87 -3.36*10**(-14)
def getCoulombByVoltage(data):
    result = list()
    result.append(__getCoulombByVoltageCh1__(data[0]))
    result.append(__getCoulombByVoltageCh2__(data[1]))
    result.append(__getCoulombByVoltageCh3__(data[2]))
    return result
def getFluenceByCoulomb(data,chargeNumberZ):
    result = list()
    result.append(data[0])#/(chargeNumberZ*ELEMENTARYCHARGE))
    result.append(data[1])#/(chargeNumberZ*ELEMENTARYCHARGE))
    result.append((data[2]))#/(chargeNumberZ*ELEMENTARYCHARGE))*1.66+7.8)
    return result
def getColoumbsByVoltages(data):
    result = list()
    for item in data:
        result.append(getCoulombByVoltage(item))
    return np.array(result)
def getFluencesByCoulombs(data,chargeNumberZ):
    result = list()
    for item in data:
        result.append(getFluenceByCoulomb(item,chargeNumberZ))
    return np.array(result)

    