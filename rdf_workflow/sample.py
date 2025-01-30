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
            splitName = treeName.split('/')
            assert(len(splitName) < 3), "Sample got a tree name with more than one splitting /. This is not implemented"
            if len(splitName)==2:
                if splitName[0] not in self.chains.keys():
                    self.chains[splitName[0]] = {}
                self.chains[splitName[0]][splitName[1]] = ROOT.TChain(treeName)
            elif len(splitName)==1:
                if splitName[0] not in self.chains.keys():
                    self.chains[splitName[0]] = {}
                self.chains[splitName[0]][splitName[0]] = ROOT.TChain(treeName)

        for fileName in self.listOfFiles:
            for directoryName in self.chains:
                for treeName in self.chains[directoryName]:
                    self.chains[directoryName][treeName].Add(fileName)

    def listOfNamesToListOfChains(self, listOfTrees:list[str]):
        finalList = []
        for treeName in listOfTrees:
            # print(treeName)
            splitName = treeName.split('/')
            # print(splitName)
            assert(len(splitName) < 3), "name to tree list conversion got the wrong number of splitting /'s"
            if len(splitName)==2:
                try:
                    finalList.append(self.chains[splitName[0]][splitName[1]])
                except KeyError:
                    print(f"Didn't find tree {treeName} in local chains. Skipping.")
            elif len(splitName)==1:
                try:
                    finalList.append(self.chains[splitName[0]][splitName[0]])
                except KeyError:
                    print(f"Didn't find tree {treeName} in local chains. Skipping.")
        return finalList

    def getListOfAllChains(self):
        finalList = []
        for directoryName in self.chains:
            for treeName in self.chains[directoryName]:
                finalList.append(self.chains[directoryName][treeName])
        return finalList

    def getNewChain(self, listOfTrees:list[str]=None):
        self.generateChains()
        if listOfTrees != None:
            listOfChains = self.listOfNamesToListOfChains(listOfTrees)
        else:
            listOfChains = self.getListOfAllChains()
        theChain = listOfChains[0]
        if len(listOfChains) > 1:
            for chain in listOfChains[1:]:
                theChain.AddFriend(chain)
        return theChain

    def getNewDataframe(self, listOfTrees:list[str]=None):
        theChain = self.getNewChain(listOfTrees)
        theDataframe = ROOT.RDataFrame(theChain)
        return theDataframe

