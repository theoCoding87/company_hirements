# TODO Converts given Ticket-Value of long string into usable csv.
# TODO Also sorts First- and Last name, due its different order given by HR.
#

from fpdf import FPDF 
from tabulate import tabulate
from datetime import datetime
import csv
import random




####Evaluate the Source File / given Path
def testObjectValues(path):
    if type(path) != str:
        print("Function Error: Function expects Datatype of String.")
    #Todo: Exception for wrong string of path
    #except OSError as e:
        #print("Functin Error: No such File.")
    else:
        with open(path, "r") as f:
            listEmployee = [line.rstrip("\n") for line in f]
            print("\n#### Check Object and its Values #### (You can expect 6 Lines)")
            print(" >   Object Type     : " + str(type(listEmployee)))
            count = 0
            for i in listEmployee:
                count += 1
            print(" >   Number of items :", count)
            ValueFirstItem= listEmployee[0].split("\t")     #Todo: changed firrst value to index of 0 -> still working?
            arrWrittenNumber = ["1st","2nd","3rd","4th"]
            countNum = 0
            for i in ValueFirstItem:
                print(" >  ", arrWrittenNumber[countNum], "value is ", ValueFirstItem[countNum])
                countNum += 1
            #print("First Item is ", ValueFirstItem[0], " | ", ValueFirstItem[1])
            print("#### EndOfCheck ####\n")


class ConsolePdfBuilder:
    def __init__(self, path):
        # list which holds listElement for each given Value for an Employee in source.txt, will be the header for tabulate
        self.mListHead = [] 
        # dict to hold demanded Values and its assigmets, initiated with the values 0
        self.mDictValuePairs = {"strFirstName":0, "strLastName":0, "intUsername":0}
        self.listTableData = []

    def PrintWelcomeScreen(self):
        print("\n   ||-------------------------------------------------------------||")
        print("   ||        PDF-Gestalter für Momox-Einstellungen Leipzig        ||")
        print("   ||            Quelle des Datensatzes ist source.txt            ||")
        print("   ||    Ausgegeben wird der Datensatz mit einem Tabellenkopf.    ||")
        print("   ||    Verwertbare Trennzeichen sind Tabulatur und Eingabe.     ||")
        print("   ||-------------------------------------------------------------||\n")

    # Functions set Dictionary indicees for the needed values: First Name, Last Name, PersonalID
    def SetFirstNameIndex(self, i):
        self.mDictValuePairs.update({"strFirstName": i})
    def SetLastNameIndex(self, i):
        self.mDictValuePairs.update({"strLastName": i})
    def setPersonalId(self, i):
        self.mDictValuePairs.update({"intUsername": i})
        
    ### first of two functions to create a password
    ### function to create random constellation of a font-independent distinguishable tripplet made of items out of four predefined lists
    def createStringTriplet(self):
        listConsonant = [] 
        # first list of the list / array -> fine-print consonants
        listConsonant.append(["b", "c", "d", "f", "g", "h", "k", "m", "n", "p", "q", "r", "u", "v", "w", "x", "y", "z"])
        # second list of the list / array of capital consonants
        listConsonant.append([ "B", "C", "D", "F", "G", "H", "K", "L", "M", "N", "P", "Q", "R", "T", "U", "V", "W", "X", "Y", "Z"])
        listVowel = []
        # third list of list / array  -> fine-print vowels
        listVowel.append(["a", "e","i","u"])
        # fourth list of list / array -> capital vowels
        listVowel.append(["A", "E", "U"])
        # create randomly chosen digits of the given lists above
        strTripplet = ""
        # first digit
        varBoolean = random.choice([True, False])
        strTripplet += listConsonant[int(varBoolean)][random.randint(0,len(listConsonant[int(varBoolean)])-1)]
        # second digit
        varBoolean = random.choice([True, False])
        strTripplet += listVowel[int(varBoolean)][random.randint(0,len(listVowel[int(varBoolean)])-1)]
        # third digit
        varBoolean = random.choice([True, False])
        strTripplet += listConsonant[int(varBoolean)][random.randint(0,len(listConsonant[int(varBoolean)])-1)]
        return strTripplet

    ### second function to create a password
    ### function to create random constellation of a duplet from a predefined list
    ### it is possible that the duplet has two numbers and no special character, or the other way around
    def createSpecialCharacterDuplet(self):
        listSymbolAndNumber = []
        # no 7 due to its similar appearance to t and so on. no tilde, no accents, no square brackets.
        listSymbolAndNumber.append(["!", "$", "%", "&", "/", "(", ")", "?", "#", ":", ";", "=", "2","3","4","5","6","8","9"])
        #create randomly chosen digits of the given lists above
        #strDuplet = ""
        # first digit
        strDuplet = listSymbolAndNumber[0][random.randint(0,len(listSymbolAndNumber[0])-1)]
        strDuplet += listSymbolAndNumber[0][random.randint(0,len(listSymbolAndNumber[0])-1)]
        #strDuplet += str(random.choice(listSymbolAndNumber))
        return strDuplet

    ### main function to create the actual password
    ### characteristics: holds 8 digits, two of them are a combination of special characters and / or numbers
    def createPassword(self):
        strPassword = str(self.createStringTriplet()) + str(self.createSpecialCharacterDuplet()) + str(self.createStringTriplet())
        return strPassword


    def PrintTable(self,listTableData):
        ### Prints out Table on Console. Table head is filled with numbers as indicees.
        ### User has to input Numbers for relevant Values:
        ### Vorname, Nachname, Personalnummer
        
        with open("source.txt","r") as f:
            listEmployee = [line.rstrip("\n") for line in f]
            
            
            # get mListHead as List of Indicees for Table Head
            numOfAttributes = 0 # as first Index of Table Head
            listFirstEmployee = listEmployee[0].split("\t")
            for i in listFirstEmployee:
                    self.mListHead.append(numOfAttributes)
                    numOfAttributes += 1
                            
            
            ### create object containing given employees for body of table:
            index = 0
            currentEmployee = listEmployee[index].split("\t")
            for b in range(len(listEmployee)):
                self.listTableData.append(listEmployee[index].split("\t"))
                index += 1
            print(tabulate(self.listTableData, headers=self.mListHead, tablefmt="grid"))
        return 1

    
    def buildPdf(self, listTableData, mDictValuePairs):
        pdf = FPDF()
        a = 0
        for i in listTableData:
            pdf.add_page()
            pdf.set_left_margin(25)
            pdf.set_font("Helvetica", style = "", size = 22)
            # create a dummy cell to get the position for the second cell under the momox-logo
            pdf.cell(w=10, h=44, ln=1)
            pdf.set_font("Helvetica", style="", size=22)
            # for creating the visual design, it is very usefull to make the borders visible.
            # pdf.cell(w=180, h=18, txt="Vorname", border=1, ln=1)
            pdf.cell(w=180, h=16, txt=listTableData[a][int(x.mDictValuePairs["strFirstName"])], ln=1)
            pdf.cell(w=180, h=16, txt=listTableData[a][int(x.mDictValuePairs["strLastName"])], ln=1)
            # create a dummy cell to get the position for the next cell 
            pdf.cell(w=10, h=44, ln=1)
            pdf.set_font("Helvetica", style="", size=28)
            pdf.cell(w=55, h=18, txt="Username: ")
            pdf.set_font("Helvetica", style="B", size=28)
            pdf.cell(w=60, h=18, txt="lej_" + listTableData[a][int(x.mDictValuePairs["intUsername"])],ln=1)   
            pdf.set_font("Helvetica", style="", size=28)
            pdf.cell(w=55, h=18, txt="Passwort: ")
            pdf.set_font("Helvetica", style="B", size=28)
            pdf.cell(w=60, h=18, txt=x.createPassword())
            pdf.image('momox_logo.png', 130, 15,48)
            a += 1
        # Todo: parse Datetime into Filename
        pdf.output("/export/einstellungen_" + datetime.today().strftime('%Y-%m-%d') + "output.pdf")
        return 1




source = "source.txt"
x = ConsolePdfBuilder(source)
x.PrintWelcomeScreen()
# Display the given Data in a human-readable Table
x.PrintTable(x.listTableData)
# Getting Assignment-Indicees for the relevant Data
x.SetFirstNameIndex(input("\nIn welcher Spalte steht der Vorname? "))
x.SetLastNameIndex(input("In welcher Spalte steht der Nachname? "))
x.setPersonalId(input("in welcher Spalte steht die Personalnummer? "))
print("\n-> Das PDF wird erstellt ... siehe Verzeichnis [Export]")
print("-> Danach werden die Container und Images gelöscht ...\n")


x.buildPdf(x.listTableData, x.mDictValuePairs)