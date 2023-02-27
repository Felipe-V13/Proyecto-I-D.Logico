import argparse
import io
import subprocess
class Latex:
    def __init__(self):
        self.__text = ""
        self.__ficheroLatex = io.open("latex.tex", "w")

    def Beammer(self, operacion, resultado):
        self.__text = "\documentclass{beamer}\n"
        self.__text += "\\begin{document}\n"
        self.__text += "\\begin{frame}\n"
        self.__text += "\\frametitle{Operacion}\n"
        self.__text += "\\begin{center}\n"
        self.__text +=  operacion +"\n"
        self.__text += "\end{center}\n"
        self.__text += "\end{frame}\n"
        self.__text += "\\begin{frame}\n"
        self.__text += "\\frametitle{Resultado}\n"
        self.__text += "\\begin{center}\n"
        self.__text += resultado + "\n"
        self.__text += "\end{center}\n"
        self.__text += "\end{frame}\n"
        self.__text += "\end{document}\n"

        self.__ficheroLatex.write(self.__text)

    def CreatePDF(self):
        subprocess.run("pdflatex latex.tex")

    def __str__(self):
        return self.__text

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
        return int(num)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multiplicación de números en diferentes bases')
    parser.add_argument('--bits', type=int, help='Número de bits para la representación de los números', required=True)
    parser.add_argument('-a', type=str, help='Primer factor a multiplicar', required=True)
    parser.add_argument('-b', type=str, help='Segundo factor a multiplicar', required=True)
    args = parser.parse_args()

    bits = args.bits
    a_str = args.a
    b_str = args.b

    # Obtener los valores de los factores
    # Identificamos la base del número (b, h, d) y lo convertimos a decimal para operar con ellos
    a_base = a_str[0]
    a_sign = ''
    if a_str[0] == '-':
        a_sign = '-'
        a_str = a_str[1:]
    a_num = a_str[1:]
    a = from_base(a_num, a_base)
    if a_base == 'b' and a_sign == '-':
        a = -((1 << (bits - 1)) - a)

    b_base = b_str[0]
    b_sign = ''
    if b_str[0] == '-':
        b_sign = '-'
        b_str = b_str[1:]
    b_num = b_str[1:]
    b = from_base(b_num, b_base)
    if b_base == 'b' and b_sign == '-':
        b = -((1 << (bits - 1)) - b)

    # Realizar la multiplicación
    result = 0
    print(f"{' ' * (bits + 4)}{to_base(a, 'b')} (multiplicando)")
    print(f"x {' ' * (bits - len(to_base(b, 'b'))) + to_base(b, 'b')}")

    for i, bit in enumerate(reversed(to_base(b, 'b'))):
        if bit == '1':
            partial = a << i
            result += partial
            print(f"{' ' * (bits - len(to_base(partial, 'b'))) + to_base(partial, 'b')} {' ' * (i)}(parcial desplazado {i} bits a la izquierda)")
        else:
            print(f"{' ' * (bits)} {' ' * (i)}(parcial desplazado {i} bits a la izquierda)")

    # Comprobar si el resultado es negativo y representarlo en complemento a dos si es el caso
    if result < 0:
        result = 2**(bits) + result
    result_str = to_base(result, 'b')
    if len(result_str) > bits:
        print("Error: el resultado no puede ser representado con la cantidad de bits especificada.")
    else:
        print(f"{' ' * (bits + 4)}{'-' * (bits + 4)}")
        print(f"{' ' * (bits - len(result_str))}{result_str} (resultado)")








