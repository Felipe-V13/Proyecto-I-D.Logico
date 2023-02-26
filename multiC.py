from pylatex import Document, Section, Subsection, Tabular
from pylatex.utils import NoEscape

# Función que convierte un número en una base determinada a decimal
def from_base(num, base='d'):
    if base == 'b':
        return int(num, 2)
    elif base == 'h':
        return int(num, 16)
    else:
        return int(num)

# Función que convierte un número decimal a una base determinada
def to_base(num, base):
    if base == 'b':
        return bin(num)[2:]
    elif base == 'h':
        return hex(num)[2:]
    else:
        return str(num)

# Pedir los datos de entrada
bits = int(input("Ingrese la cantidad de bits de los factores a multiplicar: "))
a_str = input("Ingrese el primer factor a multiplicar: ")
b_str = input("Ingrese el segundo factor a multiplicar: ")
config_file = input("Ingrese el nombre del archivo de configuración: ")

# Obtener los valores de los factores
# Identificamos la base del número (b, h, d) y lo convertimos a decimal para operar con ellos
a_base = a_str[0]
b_base = b_str[0]
a = from_base(a_str[1:], a_base)
b = from_base(b_str[1:], b_base)

# Si el número en la base binaria está en signo magnitud, cambiamos el signo si la primera letra es una 's'
if a_base == 's':
    a = -a
if b_base == 's':
    b = -b

# Realizar la multiplicación
result = 0
mult_table = []
mult_table.append([" " * (bits + 4) + to_base(a, 'b') + " (multiplicando)"])
mult_table.append(["x " + " " * (bits - len(to_base(b, 'b'))) + to_base(b, 'b')])
mult_table.append(["-" * (bits + 4) + "-" * len(to_base(b, 'b'))])
for i in range(bits):
    if b & 1:
        shifted_a = a << i
        mult_table.append([to_base(a, 'b') + " << " + str(i) + " (desplazamiento izquierdo)"])
        mult_table.append([" " * (i + 4) + "-" * (bits - i)])
        mult_table.append([" " * (bits - len(to_base(shifted_a, 'b'))) + to_base(shifted_a, 'b') + " (sumando)"])
        result += shifted_a
    b >>= 1

# Si el resultado de la multiplicación es negativo, convertimos el resultado a signo magnitud
if result < 0:
    result = -result
    result = (1 << bits) - result

# Crear el documento LaTeX
doc = Document('beamer')

# Agregar la primera diapositiva con los valores de entrada
with doc.create(Section('Valores de entrada')):
    doc.append(NoEscape(r'\begin{itemize}'))
    doc.append(NoEscape(r'\item Operandos: ' + a_str + ', ' + b_str))
