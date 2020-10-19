'''
About:  -Recieve family data in CSV format, save data about each family member and output a print version of the family tree
        -Names can be added individually as well

Family Tree Print Output:
Parent
    Child (Parent to Sub-Child)
        Sub-Child
    Child

Note: doesn't handle duplicate names, could generate unique ID's for this
'''

import datetime
import pandas as pd

#########################
#Get family data from csv file
#########################
def getFamilyData(famTree, path = r'Family_Members.csv'):
    df = pd.read_csv(path, sep=',', skiprows=1) #Read CSV file, account for first row of headers
    for index, row in df.iterrows():
        name = row["Name"].split()
        dateOfBirth = list(map(int, row["Date of Birth"].split("/")))

        if not pd.isna(row["Date of Death"]):
            dateOfDeath = list(map(int, row["Date of Birth"].split("/")))
        else:
            dateOfDeath = [0,0,0]

        famTree.addMember(Person(name[0], name[1],dateOfBirth,dateOfDeath))

        if row["Relation"].lower() == "parent":
            famTree.addParent(famTree.getMemeber(row["Name"]))

        if row["Relation"].lower() == "children":
            famTree.addChild(famTree.getMemeber(row["Name"]), famTree.getMemeber(row["Parent Name"]))



class FamilyTree:
    tree = dict() #Dictionary holding relations
    treeList = [] #List holding all members
    indexOldest = 0
    headPerson = "" #Oldest person at the top of the tree

    def addMember(self, newMember):
        self.treeList.append(newMember)

    def getMemeber(self, findName):
        for person in self.treeList:
            if findName == str(person):
                return person
        return None

    def addChild(self, child, parent):
        if parent in self.tree:
            self.tree[parent].append(child)
        else:
            self.tree[parent] = [child]

    def addParent(self, parent):
        self.headPerson = parent
        self.tree[parent] = []

    def printSubTree(self, parent, tabs=""):
        print(tabs + str(parent))
        for child in self.tree[parent]:
            if child in self.tree:
                self.printSubTree(child, tabs + "   ")
            else:
                print(tabs+"   "+ str(child))

    def printFullTree(self):
        self.printSubTree(self.headPerson)

class Person:
    def __init__(self, fname, lname, dateofbirth, dateofdeath =[0,0,0]):
        self.fname = fname;
        self.lname = lname;
        self.birthDay, self.birthMonth, self.birthYear = dateofbirth;
        self.deathDay, self.deathMonth, self.deathYear = dateofdeath;

    def __str__(self):
        return " ".join([self.fname, self.lname]);

    def getID(self):
        return self.ID

    def dateOfBirth(self):
        return '/'.join(str(i) for i in [self.birthDay, self.birthMonth, self.birthYear])

    def dateOfDeath(self):
        if self.deathDay != 0:
            return '/'.join(str(i) for i in [self.deathDay, self.deathMonth, self.deathYear])
        else:
            return  self.__str__() + " is not dead"

    def addDeathDate(self, day, month ,year):
        self.deathDay, self.deathMonth, self.deathYear = day, month, year

    def checkIfDead(self):
        d1 = datetime.datetime(self.deathYear, self.deathMonth, self.deathDay)
        return d1 < datetime.datetime.today()


if __name__ == "__main__":

    famTree = FamilyTree()
    getFamilyData(famTree)
    famTree.printSubTree(famTree.getMemeber("Ted Bing"))  #Print sub tree
    print("\n \n")
    famTree.printFullTree()


