########################################################################
## sample.py                                                          ##
## Author: Andrew Loeliger                                            ##
## defines class for containing information from ROOT files           ##
########################################################################


#!/usr/bin/env python3

import ROOT

class sample:
    def __init__(self, listOfFiles:list[str], treeNames:list[str]):
        self.listOfFiles = listOfFiles
        self.treeNames = treeNames

    #We're going to move this off to be a reset of state
    #since undoing the friend process doesn't seem to be working
    def generateChains(self):
        self.chains = {}
        for treeName in self.treeNames:
            self.chains[treeName] = ROOT.TChain(treeName)

        for fileName in self.listOfFiles:
            for treeName in self.chains:
                self.chains[treeName].Add(fileName)

    def listOfNamesToListOfChains(self, listOfTrees:list[str]):
        finalList = []
        for treeName in listOfTrees:
            finalList.append(self.chains[treeName])
        return finalList

    def getListOfAllChains(self):
        finalList = []
        for treeName in self.chains:
            finalList.append(self.chains[treeName])
        return finalList

    def getNewChain(self, listOfTrees:list[str]=None):
        self.generateChains()
        print(listOfTrees)
        if listOfTrees != None:
            listOfChains = self.listOfNamesToListOfChains(listOfTrees)
        else:
            listOfChains = self.getListOfAllChains()
        print(listOfChains)
        theChain = listOfChains[0]
        if len(listOfChains) > 1:
            for chain in listOfChains[1:]:
                theChain.AddFriend(chain)
        return theChain

    def getNewDataframe(self, listOfTrees:list[str]=None):
        theChain = self.getNewChain(listOfTrees)
        theDataframe = ROOT.RDataFrame(theChain)
        return theDataframe
