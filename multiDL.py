import sys
import argparse
import io
import subprocess
class Titlepage:
    def __init__(self):
        self.__title = "\\title{}\n"
        self.__subtitle = "\subtitle{}\n"
        self.__authors = "\\author{}\n"
        self.__institute = "\institute{}\n"
        self.__date = "\date{}\n"

        self.__text = ""
    
    def setPageTitleInfo(self, title = "", subtitle = "", authors = "", institute = "", date = ""):
        self.__title = self.__title.replace("{}", "{"+title+"}")
        self.__subtitle = self.__subtitle.replace("{}", "{"+subtitle+"}")
        self.__institute = self.__institute.replace("{}", "{"+institute+"}")
        self.__authors = self.__authors.replace("{}", "{"+authors+"}")
        self.__date = self.__date.replace("{}", "{"+date+"}")
    
    def getTitlePage(self):
        self.__text += self.__title
        self.__text += self.__subtitle
        self.__text += self.__authors
        self.__text += self.__institute
        self.__text += self.__date
        return self.__text

class Frame:
    def __init__(self):
        self.__content = ""
        self.__frameTitle = ""
        self.__text = ""

    def setContent(self, title = "", content = ""):
        self.__frameTitle = title
        self.__content = content
    
    def getFrame(self):
        self.__text += "\\begin{frame}\n"
        self.__text += "\\frametitle{"+self.__frameTitle+"}\n"
        self.__text += "\\begin{center}\n"
        self.__text += self.__content + "\n"
        self.__text += "\end{center}\n"
        self.__text += "\end{frame}\n"
        return self.__text

class Latex:
    def __init__(self):
        self.__text = ""
        self.__ficheroLatex = io.open("latex.tex", "w")
        self.__frames = []
        self.__titlepage = Titlepage()
        self.__framescounter = 0
 
    def createFrame(self, title, content):
        self.__frames.append(Frame())
        self.__frames[self.__framescounter].setContent(title, content)
        self.__framescounter += 1
    
    def setTitlePageContent(self, title = "", subtitle = "", authors = [], institute = "", date = ""):
        authores = ""
        for autor in authors:
            authores += autor + " \\and "
        self.__titlepage.setPageTitleInfo(title, subtitle, authores, institute, date)

    def __maketitle__(self):
        self.__text += "\\frame{\\titlepage}\n"

    def beamer(self):
        self.__text += "\documentclass{beamer}\n"
        self.__text += self.__titlepage.getTitlePage()
        self.__text += "\\begin{document}\n"
        for page in self.__frames:
            self.__text += page.getFrame()
        self.__maketitle__()
        self.__text += "\end{document}\n"
        self.__ficheroLatex.write(self.__text)

    def CreatePDF(self):
        subprocess.call()

    def __str__(self):
        return self.__text

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
    commands_i = sys.argv[1:]
    parser = argparse.ArgumentParser()

    if len(commands_i) != 0:
        parser.add_argument('--bits', type = int, help="Numero de bits para representacion numerica", required= False)
        parser.add_argument('-a', type = str, help = "Multiplicando", required = ('--bits' == commands_i[0]))
        parser.add_argument('-b', type = str, help = "Operando", required = ('--bits' == commands_i[0]))

        parser.add_argument('-f', type = str, help = "Name file with factors and bits extension for representation", required=False)

    else:
        print('There aren\'t inputs')
        sys.exit(-1)

    args = parser.parse_args()
    bits = ""
    a_str = ""
    b_str = ""

    if commands_i[0] == "--bits":
        bits = args.bits
        a_str = args.a
        b_str = args.b

    if commands_i[0] == "-f":
        with io.open(args.f, 'r') as file:
            filetext = file.readline().split(' ')
            bits = int(filetext[1])
            a_str = filetext[3]
            b_str = filetext[5]

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

