import pyvisa
import numpy as np
import csv
from helpers import ScopeTools

SCOPE_IP = '172.16.206.60'

rm = pyvisa.ResourceManager('@py')
scope = rm.open_resource(f'TCPIP0::{SCOPE_IP}::INSTR')

print("Connected to:", scope.query("*IDN?"))

print(scope.query(":WAVeform:SOURce?"))
scope.write(":WAVeform:SOURce CHANnel1")
print(scope.query(":WAVeform:SOURce?"))

print(scope.query(":WAVeform:MODE?"))
scope.write(":WAVeform:MODE NORMal")
print(scope.query(":WAVeform:MODE?"))

print(scope.query(":WAVeform:FORMat?"))
scope.write(":WAVeform:FORMat BYTE")
print(scope.query(":WAVeform:FORMat?"))

print(scope.query(":WAVeform:POINts?"))
scope.write(":WAVeform:POINts 1000")
print(scope.query(":WAVeform:POINts?"))

print(scope.query(":WAVeform:PREamble?"))