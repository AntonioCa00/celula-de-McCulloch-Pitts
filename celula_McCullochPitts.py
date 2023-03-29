import numpy as np
import random
import json

#
def mcculloch_pitts(num_bits, operation):
    print ("Numero de bits: ", str(num_bits), " Operacion logica: ", operation)
    bit_sequences = [[int(j) for j in list('{0:b}'.format(i).zfill(num_bits))] for i in range(2**num_bits)]
    print("Secuencias de bits generadas:")
    print(bit_sequences)
    
    if operation == "and":
        op_func = all
    elif operation == "or":
        op_func = any
    elif operation == "not":
        op_func = lambda x: not x
    
    threshold = random.random()
    print("Umbral generado: ", threshold)
    
    for seq in bit_sequences:
        weights = [random.random() for i in range(num_bits)]
        weighted_sum = sum([seq[i] * weights[i] for i in range(num_bits)])
        output = op_func([weighted_sum >= threshold])
        
        print("{}= {}. Pesos: {}".format(seq, output, weights))

mcculloch_pitts(3, "or")
mcculloch_pitts(4, "and")
mcculloch_pitts(1, "not")

class Celula():

    def __init__(self, compuerta="AND", epoch=50, n_bits=2):
        self.n_bits = n_bits
        self.compuerta = compuerta
        self.epoch = epoch
        if compuerta == "NOT":
            print("Para la compuerta NOT el numero de bits es, por defecto, 1")
            self.n_bits = 1
        self.tt = self._tabla_de_verdad(self.n_bits, self.compuerta)
        self.pesos_sinapticos = []
        self.umbral = None 

    def _tabla_de_verdad(self, n_bits, compuerta="AND"):
        matrix = []
        aux = {}
        tt = {}
        for i in range(n_bits):
            aux[i] = 2**(n_bits-(i+1))
        for k,v in aux.items():
            matrix.insert(k,[])
            bit_actual = 1
            for _ in range(n_bits):
                if matrix[k][-v:].count(bit_actual) == v:
                    matrix[k].append(1^bit_actual)
                    bit_actual = 1^bit_actual
                else:
                    matrix[k].append(bit_actual)
        for j in range(len(matrix[0])):
            expression = []
            for i in range(n_bits):
                expression.append(matrix[i][j])
            if compuerta == "AND":
                tt[str(expression)] = True if expression.count(1) == n_bits else False
            if compuerta == "OR":
                tt[str(expression)] = True if expression.count(1) >= 1 else False
            if compuerta == "NOT":
                tt[str(expression)] = not expression[0]
        return tt

    def _fit(self):
        correct = False
        p_sinapticos = []
        actual_epoch = 0
        while actual_epoch < self.epoch and not correct:
            self.p_sinapticos = [round(random.random()*20-10) for _ in range(self.n_bits)]
            self.umbral = round(random.random()*20-10)
            for k,v in self.tt.items():
                suma = 0
                for i, bit in enumerate(json.loads(k)):
                    suma += bit*self.p_sinapticos[i]
                result = True if suma > self.umbral else False
                if result == self.tt[k]:
                    correct = True
                else:
                    correct = False
                    break
            actual_epoch += 1
        return correct, actual_epoch  

    def entrenar(self):
        result, actual_epoch = self._fit()
        if result:
            print("Se aprendió correctamente: {}".format(actual_epoch))
        else:
            print("No ha aprendido correctamente")
            
    def evaluar(self, bits=[]):
        if len(bits) != self.n_bits:
            print("El numero de bits ingresado es diferente al numero de bits de la compuerta")
        else:
            try:
                suma = 0
                for i, bit in enumerate(bits):
                    suma += bit * self.p_sinapticos[i]
                result = True if suma > self.umbral else False
            except IndexError:
                raise IndexError ("¡Error! No se ha entrenado la neurona")
            return result