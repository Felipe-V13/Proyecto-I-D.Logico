import sys
import argparse
import io
import subprocess

#"Es el constructor de la clase Titlepage. Inicializa las variables de instancia 
#de la clase, las cuales contienen las cadenas LaTeX para los diferentes elementos
#de la página de título (__title, __subtitle, __authors, __institute y __date"
class Titlepage:
    def __init__(self):
        self.__title = "\\title{}\n"
        self.__subtitle = "\subtitle{}\n"
        self.__authors = "\\author{}\n"
        self.__institute = "\institute{}\n"
        self.__date = "\date{}\n"

        self.__text = ""
    #title: Título de la página de título (cadena).
    #subtitle: Subtítulo de la página de título (cadena).
    #authors: Autores de la página de título (cadena).
    #institute: Institución de la página de título (cadena).
    #date: Fecha de la página de título (cadena).
    def setPageTitleInfo(self, title = "", subtitle = "", authors = "", institute = "", date = ""):
        self.__title = self.__title.replace("{}", "{"+title+"}")
        self.__subtitle = self.__subtitle.replace("{}", "{"+subtitle+"}")
        self.__institute = self.__institute.replace("{}", "{"+institute+"}")
        self.__authors = self.__authors.replace("{}", "{"+authors+"}")
        self.__date = self.__date.replace("{}", "{"+date+"}")
        
    #Esta función se utiliza para obtener la página de título completa. 
    # #Concatena las diferentes cadenas que componen la página de título 
    # #(__title, __subtitle, __authors, __institute y __date) y las devuelve 
    # #como una sola cadena.
    def getTitlePage(self):
        self.__text += self.__title
        self.__text += self.__subtitle
        self.__text += self.__authors
        self.__text += self.__institute
        self.__text += self.__date
        return self.__text

class Frame:
    #Es el constructor de la clase Frame. Inicializa las variables de instancia de la clase
    def __init__(self):
        self.__content = ""
        self.__frameTitle = ""
        self.__text = ""
        
    #Esta función se utiliza para establecer el contenido del marco y su título.
    #La función toma dos cadenas de entrada: title y content.
    def setContent(self, title = "", content = ""):
        self.__frameTitle = title
        self.__content = content
        
    #Esta función se utiliza para obtener el marco completo. Concatena las 
    # #diferentes cadenas que componen el marco (__frameTitle y __content) 
    # #y las devuelve como una sola cadena.
    def getFrame(self):
        self.__text += "\\begin{frame}\n"
        self.__text += "\\frametitle{"+self.__frameTitle+"}\n"
        self.__text += "\\begin{center}\n"
        self.__text += self.__content + "\n"
        self.__text += "\end{center}\n"
        self.__text += "\end{frame}\n"
        return self.__text

class Latex:
    #inicializa las variables
    def __init__(self):
        self.__text = ""
        self.__ficheroLatex = io.open("latex.tex", "w")
        self.__frames = []
        self.__titlepage = Titlepage()
        self.__framescounter = 0
        
    # Esta función se utiliza para crear un marco y agregarlo a la lista de marcos. 
    # #La función toma dos cadenas de entrada: title y content.
    def createFrame(self, title, content):
        self.__frames.append(Frame())
        self.__frames[self.__framescounter].setContent(title, content)
        self.__framescounter += 1
    
    #Esta función se utiliza para establecer el contenido de la página de título. 
    # #La función toma cinco entradas opcionales: title, subtitle, authors, institute
    # y date.
    def setTitlePageContent(self, title = "", subtitle = "", authors = [], institute = "", date = ""):
        authores = ""
        for autor in authors:
            authores += autor + " \\and "
        self.__titlepage.setPageTitleInfo(title, subtitle, authores, institute, date)

    #titulo
    def __maketitle__(self):
        self.__text += "\\frame{\\titlepage}\n"

    #Esta función se utiliza para crear el documento LaTeX completo. 
    # La función concatena las diferentes cadenas que componen el documento LaTeX 
    # (\documentclass{beamer}, el contenido de la página de título, \begin{document},
    # los marcos, la página de título y \end{document}) y los almacena en la 
    # variable __text
    def createBeamer(self):
        self.__text += "\documentclass{beamer}\n"
        self.__text += self.__titlepage.getTitlePage()
        self.__text += "\\begin{document}\n"
        for page in self.__frames:
            self.__text += page.getFrame()
        self.__maketitle__()
        self.__text += "\end{document}\n"
        self.__ficheroLatex.write(self.__text)
        self.__ficheroLatex.close()

    def __str__(self):
        return self.__text

    def CreatePDF(self):
        subprocess.call("pdflatex latex.tex")

    def __str__(self):
        return self.__text

class Number:
    #inicializacion de varables
    # Constructor que inicializa las variables de la clase
    def __init__(self, number, bits):
        self.__bits = bits    # Cantidad de bits del número
        self.__number = number    # Valor del número
        self.__base = self.getbase()    # Base numérica del número
        self.bitextension()    # Extensión del número a la cantidad de bits especificada
        
    # Función que extiende el número a la cantidad de bits especificada
    def bitextension(self):
        # Si la base es 2, se llama a la función de extensión de bits
        if self.__base == 2:
            self.__bitextension__()
        # Si no es base 2, se convierte el número a binario, se extiende y se vuelve a la base original
        else:
            oldbase = self.__getbaseindicator__()    # Se guarda la base original del número
            self.toBase('b')    # Se convierte el número a binario
            self.__base = self.getbase()    # Se actualiza la base del número a binario
            self.__bitextension__()    # Se extiende el número a la cantidad de bits especificada
            self.toBase(oldbase)    # Se convierte el número a la base original
            self.__base = self.getbase()    # Se actualiza la base del número a la original

    def __bitextension__(self):
    #Comprobamos si la longitud del número es mayor que la cantidad de bits que se definen en la clase.
        if len(self.__number[1:]) > self.__bits:
            #Si es mayor, entonces se elimina la parte más significativa de los bits para que el número tenga la longitud de bits deseada.
            self.__number = self.__getbaseindicator__() + self.__number[len(self.__number) - self.__bits:]
        else:
            #En caso contrario, calculamos la cantidad de bits que faltan para alcanzar la longitud deseada.
            neededbits = self.__bits - len(self.__number[1:])
            #Si el número es un número con signo, entonces añadimos el bit de signo en el número.
            if self.isSignedNumber():
                self.__number = self.__getbaseindicator__() + 's' + '0'*neededbits + self.__number[2:]
            else:
                #En caso contrario, añadimos ceros a la izquierda para alcanzar la longitud deseada.
                self.__number = self.__getbaseindicator__() + '0'*neededbits + self.__number[1:]

    def getNumber(self):
        #Método para obtener el número.
        return self.__number
        
    def __getbaseindicator__(self):
        #Método privado para obtener el indicador de la base en la que está representado el número.
        if self.__base == 2:
            return 'b'
        elif self.__base == 16:
            return 'h'
        else:
            return 'd'

    def getbase(self):
        if self.__number[0] ==  'd':
            return 10
        elif self.__number[0] == 'b':
            return 2
        elif self.__number[0] == 'h':
            return 16
        else:
            self.__number = 'd' + self.__number
            return 10
    
        # Función que verifica si el número es de tipo "signed"
    def isSignedNumber(self):
        if self.__number[1] == 's':
            return True
        return False

    # Función para cambiar la base del número
    def toBase(self, base):
        # Actualizar la base del número
        self.__base = base
        # Variables para almacenar el signo y número
        sign = ''
        number_t = ''
        
        # Si el número es de tipo "signed", entonces se remueve la letra 's'
        if self.isSignedNumber():
            number_t = self.__number[2:]
            sign = 's'
        else:
            number_t = self.__number[1:]
        
        # Convertir el número a la base especificada
        if base == 'd':
            self.__number = self.__base + sign + str(int(number_t, self.getbase()))
        elif base == 'h':
            self.__number = self.__base + sign + hex(int(number_t, self.getbase())).replace('0x','')
        elif base == 'b':
            self.__number = self.__base + sign + bin(int(number_t, self.getbase())).replace('0b', '')
        else:
            print("Not valid base")

    def __len__(self):
        return self.__bits

    def __getitem__(self, index):
        return self.__number[index]
    
    def __str__(self):
        return self.__number

class BinaryCalculator:
    def __init__(self, multiplicand, multiplier, bits):
        # Se inicializan las variables del objeto
        self.__multiplicand = Number(multiplicand, bits)
        self.__multiplier = Number(multiplier, bits)
        self.__operationsteps = ''
        self.__operation = ''
        self.__lastoperationresult = ''
        # Se convierten los factores a binario
        self.__setFactorsToBinary__()

    def getoperationtext(self):
        return self.__operation

    def getoperationsteps(self):
        return self.__operationsteps

    def getlastoperationresult(self):
        return self.__lastoperationresult

    def __setFactorsToBinary__(self):
        # Se convierten los factores a binario si no lo están
        if self.__multiplicand[0] != 'b':
            self.__multiplicand.toBase('b')
        if self.__multiplier[0] != 'b':
            self.__multiplier.toBase('b')

    def __setOperation__(self, operand):
        #Se establece la operación a realizar en la variable de instancia __operation
        self.__operation = self.__multiplicand.getNumber() + '\n'
        self.__operation += operand + self.__multiplier.getNumber() + '\n'

    def __getabsolutefactor__(self, factor):
        #Se obtiene el factor real eliminando la posible "s" que indica que es un número con signo
        absolutefactor = factor[1:]
        if factor.isSignedNumber():
            absolutefactor = factor[2:]
        return absolutefactor

    def __getProcediment__(self, multiplicand, multiplier):
        #Se obtiene el procedimiento de la multiplicación de los dos factores
        subproduc = ''
        for i in range(len(multiplier) - 1, -1, -1):
            for j in range(len(multiplicand) - 1, -1, -1):
                subproduc = self.__bit_to_bit_multiplication__(multiplier[i], multiplicand[j]) + subproduc
            self.__operationsteps += subproduc + "0"*(len(multiplier) - (i + 1)) + '\n'
            subproduc = ''

    def __bit_to_bit_multiplication__(self, multiplicand, multiplier):
        #Realiza la multiplicación de dos bits y devuelve el resultado
        if (multiplicand == multiplier):
            return multiplier
        else:
            return '0'

    def __setsign__(self, resultado):
        ismultiplicandsigned = self.__multiplicand.isSignedNumber()
        ismultipliersigned = self.__multiplier.isSignedNumber()

        # Verificar si ambos números son firmados
        if (ismultiplicandsigned and ismultipliersigned):
            resultado = 'b' + resultado  # Si ambos números son firmados, el resultado es un número binario firmado
        # Verificar si ambos números no son firmados
        elif not (ismultiplicandsigned or ismultipliersigned):
            resultado = 'b' + resultado  # Si ambos números no son firmados, el resultado es un número binario sin signo
        else:
            resultado = 'bs' + resultado  # Si solo uno de los números es firmado, el resultado es un número binario con signo
        return resultado

    def Multiplication(self):
        self.__setOperation__('x')
        multiplicand = self.__getabsolutefactor__(self.__multiplicand)
        multiplier = self.__getabsolutefactor__(self.__multiplier)

        self.__getProcediment__(multiplicand, multiplier)  # Obtener el procedimiento de la multiplicación
        result = self.__binary_addition__()  # Realizar la suma binaria de cada paso del procedimiento de la multiplicación
        result = self.__setsign__(result)  # Establecer el signo del resultado
        self.__lastoperationresult = result  # Guardar el resultado de la multiplicación como un objeto Number con la misma cantidad de bits que el multiplicando

    def __binary_addition__(self):
        result = 0
        for step in self.__operationsteps.split('\n')[:-1]:
            result += int(step, 2)
        result = bin(result)
        return str(result.replace('0b', ''))
    
    def __str__(self):
        text = ''
        text += self.getoperationtext() + '\n'
        text += self.getoperationsteps() + '\n'
        text += self.getlastoperationresult()
        return text

if __name__ == '__main__':
    commands_i = sys.argv[1:]  # obtener los argumentos de línea de comando después del nombre del script
    parser = argparse.ArgumentParser()  # Crear un objeto analizador de argumentos para el script

    # Verificar si se proporcionaron argumentos de línea de comando
    if len(commands_i) != 0:
        # Agregar argumentos al analizador de argumentos
        parser.add_argument('--bits', type=int, help="Número de bits para representación numérica", required=False)
        parser.add_argument('-a', type=str, help="Multiplicando", required=('--bits' in commands_i))
        parser.add_argument('-b', type=str, help="Operando", required=('--bits' in commands_i))
        parser.add_argument('-f', type=str, help="Nombre del archivo con factores y extensión de bits para la representación", required=False)

        # Analizar los argumentos proporcionados en la línea de comando
        args = parser.parse_args()

        # Verificar si el valor de bits es válido
        if args.bits and not (1 <= args.bits <= 8):
            print('Error: bits debe ser un entero entre 1 y 8')
            exit()

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

    calculator = BinaryCalculator(a_str, b_str, bits)
    calculator.Multiplication()
    latex = Latex()
    latex.createFrame('Operation', calculator.getoperationtext().replace('\n', '\\\\'))
    latex.createFrame('Result', calculator.getoperationsteps().replace('\n', '\\\\') + calculator.getlastoperationresult())
    latex.setTitlePageContent('Multiplicacion binaria', 'EL3307:Dise\~no l\\\'ogico', ['Justin Corea', 'Felipe Vargas', 'Jesus Alfaro'], 'Instituto tecnol\\\'ogico de Costa Rica', '16/marzo/2023')
    latex.createBeamer()
    latex.CreatePDF()
    print(calculator)
