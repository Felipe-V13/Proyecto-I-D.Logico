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

    def createBeamer(self):
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

class Number:
    def __init__(self, number, bits):
        self.__bits = bits
        self.__number = number
        self.__base = self.getbase()
        self.bitextension()

    def bitextension(self):
        if self.__base == 2:
            self.__bitextension__()
        else:
            oldbase = self.__getbaseindicator__()
            self.toBase('b')
            self.__base = self.getbase()
            self.__bitextension__()
            self.toBase(oldbase)
            self.__base = self.getbase()

    def __bitextension__(self):
        if len(self.__number[1:]) > self.__bits:
            print('esto era yo w: ', self.__number)
            self.__number = self.__getbaseindicator__() + self.__number[len(self.__number) - self.__bits:]
            print('en esto me converti: ', self.__number)
        else:
            neededbits = bits - len(self.__number[1:])
            if self.isSignedNumber():
                self.__number = self.__getbaseindicator__() + 's' + '0'*neededbits + self.__number[2:]
            else:
                self.__number = self.__getbaseindicator__() + '0'*neededbits + self.__number[1:]

    def getNumber(self):
        return self.__number
    
    def __getbaseindicator__(self):
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
    
    def isSignedNumber(self):
        if self.__number[1] == 's':
            return True
        return False
    
    def toBase(self, base):
        self.__base = base
        sign = ''
        number_t = ''
        
        if self.isSignedNumber():
            number_t = self.__number[2:]
            sign = 's'
        else:
            number_t = self.__number[1:]
        
        if base == 'd':
            self.__number = self.__base + sign + str(int(number_t, self.getbase()))
        elif base == 'h':
            self.__number = self.__base + sign + hex(int(number_t, self.getbase())).replace('0x','')
        elif base == 'b':
            self.__number = self.__base + sign + bin(int(number_t, self.getbase())).replace('0b', '')
        else:
            print("Not valid base")
    
    def __getitem__(self, index):
        return self.__number[index]
    
    def __str__(self):
        return self.__number

class BinaryCalculator:
    def __init__(self, multiplicand, multiplier, bits):
        self.__multiplicand = Number(multiplicand, bits)
        self.__multiplier = Number(multiplier, bits)
        self.__operationsteps = ''
        self.__operation = ''
        self.__lastoperationresult = ''
        self.__setFactorsToBinary__()
    
    def getoperationtext(self):
        return self.__operation

    def getoperationsteps(self):
        return self.__operationsteps

    def getlastoperationresult(self):
        return self.__lastoperationresult
    
    def __setFactorsToBinary__(self):
        if self.__multiplicand[0] != 'b':
            self.__multiplicand.toBase('b')
        if self.__multiplier[0] != 'b':
            self.__multiplier.toBase('b')
    
    def __setOperation__(self, operand):
        self.__operation = self.__multiplicand.getNumber() + '\n'
        self.__operation += operand + self.__multiplier.getNumber() + '\n'
    
    def __getRealFactor__(self, factor):
        realfactor = factor[1:]
        if factor.isSignedNumber():
            realfactor = factor[2:]
        return realfactor

    def __getProcediment__(self, multiplicand, multiplier):
        subproduc = ''
        for i in range(len(multiplier) - 1, -1, -1):
            for j in range(len(multiplicand) - 1, -1, -1):
                subproduc = self.__bit_to_bit_multiplication__(multiplier[i], multiplicand[j]) + subproduc
            self.__operationsteps += subproduc + "0"*(len(multiplier) - (i + 1)) + '\n'
            subproduc = ''

    def __bit_to_bit_multiplication__(self, multiplicand, multiplier):
        if (multiplicand == multiplier):
            return multiplier
        else:
            return '0'
    
    def __setsign__(self, resultado):
        ismultiplicandsigned = self.__multiplicand.isSignedNumber()
        ismultipliersigned = self.__multiplier.isSignedNumber()
        
        if (ismultiplicandsigned and ismultipliersigned):
            resultado = 'b' + resultado
        elif not (ismultiplicandsigned or ismultipliersigned):
            resultado = 'b' + resultado
        else:
            resultado = 'bs' + resultado
        return resultado
    
    def Multiplication(self):
        self.__setOperation__('x')
        multiplicand = self.__getRealFactor__(self.__multiplicand)
        multiplier = self.__getRealFactor__(self.__multiplier)

        self.__getProcediment__(multiplicand, multiplier)
        self.__lastoperationresult = bin(int(multiplicand, 2)*int(multiplier, 2)).replace('0b', '')
        self.__lastoperationresult = self.__setsign__(self.__lastoperationresult)

    def __str__(self) -> str:
        return self.__operation + self.__operationsteps +  self.__lastoperationresult

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

    calculator = BinaryCalculator(a_str, b_str, bits)
    calculator.Multiplication()
    latex = Latex()
    latex.createFrame('Operation', calculator.getoperationtext())
    latex.createFrame('result', calculator.getoperationsteps() + calculator.getlastoperationresult())
    latex.setTitlePageContent('Multiplicacion binaria', '', ['Justin Corea', 'persona2', 'persona3'], 'Instituto tecnologico de costa rica', 'xx/marzo/2023')
    latex.createBeamer()
    #latex.CreatePDF()
    print(calculator)
