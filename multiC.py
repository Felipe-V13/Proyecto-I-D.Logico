# Función que convierte un número en una base determinada a decimal
def from_base(num, base):
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
print(f"{' ' * (bits + 4)}{to_base(a, 'b')} (multiplicando)")
print(f"x {' ' * (bits - len(to_base(b, 'b'))) + to_base(b, 'b')}")
print(f"{'-' * (bits + 4)}{'-' * len(to_base(b, 'b'))}")
for i in range(bits):
    if b & 1:
        print(f"{' ' * i}{to_base(a, 'b')} << {i} (desplazamiento izquierdo)")
        print(f"{' ' * (i + 4)}{'-' * (bits - i)}")
        shifted_a = a << i
        print(f"{' ' * (bits - len(to_base(shifted_a, 'b')))}{to_base(shifted_a, 'b')} (sumando)")
        result += shifted_a
    b >>= 1

# Si el resultado de la multiplicación es negativo, convertimos el resultado a signo magnitud
if result < 0:
    result = -result
    result = (1 << bits) - result

# Mostrar el resultado de la multiplicación en binario
print(f"{'-' * (bits + 4)}")
print(f"{' ' * (bits - len(to_base(result, 'b'))) + to_base(result, 'b')} (resultado en binario)")
