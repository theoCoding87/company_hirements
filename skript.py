# TODO Converts given Ticket-Value of long string into usable csv.
# TODO Also sorts First- and Last name, due its different order given by HR.
#

from fpdf import FPDF 
from tabulate import tabulate
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




### neuer Ansatz:
### Class 
###     constructor (?) with given path
###     method to print to Table
###     method: assign Values Vorname, Nachname, Personalnummer, Passwort
###         display the vales to user as a printed table in command line
###         user-input from console 1,2,3,4
###     method: create PDF
class ConsolePdfBuilder:
    def __init__(self, path):
        # list which holds listElement for each given Value for an Employee in source.txt, will be the header for tabulate
        self.mlistHead = [] 
        # dict to hold demanded Values and its assignet
        self.mDictValuePairs = {"strFirstName":0, "strLastName":0, "intUsername":0}


    def PrintWelcomeScreen(self):
        print("\n   ||-------------------------------------------------------------||")
        print("   ||        PDF-Gestalter für Momox-Einstellungen Leipzig        ||")
        print("   || Quelle des Datensatzes ist source.txt                       ||")
        print("   || aktuelle Reihenfolge: Vorname, Nachname, lej_1234, Passwort ||")
        print("   ||-------------------------------------------------------------||\n")

    def EvaluatePath(self,path):
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


    # Functions set Dictionary indicees for the needed values: First Name, Last Name, PersonalID
    def SetFirstNameIndex(self, i):
        self.mDictValuePairs.update({"strFirstName": i})
    def SetLastNameIndex(self, i):
        self.mDictValuePairs.update({"strLastName": i})
    def setPersonalId(self, i):
        self.mDictValuePairs.update({"intUsername": i})
        
    ### first of two functions to create a password
    ### function to create random constellation of a font-independent distinguishable tripplet made of items out of four predefined lists
    def createStringTriplet():
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
    def createSpecialCharacterDuplet():
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
    def createPassword():
        strPassword = str(createStringTriplet()) + str(createSpecialCharacterDuplet()) + str(createStringTriplet())
        return strPassword

    # Function to concatenate the Personal Number and Prefix lej_
    def createUserName(self, MomoxPersNr):
        userName = "lej_" + str(MomoxPersNr)
        return userName

    def PrintTable(self,path):
        ### Prints out Table on Console. Table head is filled with numbers as indicees.
        ### User has to input Numbers for relevant Values:
        ### Vorname, Nachname, Personalnummer
        
        with open("source.txt","r") as f:
            listEmployee = [line.rstrip("\n") for line in f]
            # Detect count of attributes
            numOfAttributes = 0
            listFirstEmployee = listEmployee[0].split("\t")
            for i in listFirstEmployee:
                    self.mlistHead.append(numOfAttributes)
                    numOfAttributes += 1
                            
            ### create object containing given employees for body of table:
            listTableData = []
            count = 0

            #for i in listEmployee:
            currentEmployee = listEmployee[count].split("\t")
            for b in range(len(currentEmployee)):
                listTableData.append(listEmployee[count].split("\t"))
                count += 1
            count = 0
            print(tabulate(listTableData, headers=self.mlistHead, tablefmt="grid"))
        return 1








source = "source.txt"
x = ConsolePdfBuilder(source)
# x.PrintWelcomeScreen()
# x.EvaluatePath(source)
x.PrintTable(source)
i = input("Welche Spalte ist Vorname: ")
x.SetFirstNameIndex(i)

i = input("Welche Spalte ist Nachname: ")
x.SetLastNameIndex(i)

i = input("Welche Spalte ist Personalnummer: ")
x.setPersonalId(i)

print(x.mDictValuePairs)



#Todo: class momoxPDF(assignedStructure)
# needs to be 3x3 ?
pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", "B", 16)
pdf.cell(40, 10, "Momox")
pdf.image('logo.jpg', x = None, y = None, type = 'jpg',)
pdf.output("firsExample.pdf")



# password-generator

#print("---------------> convertion done.")