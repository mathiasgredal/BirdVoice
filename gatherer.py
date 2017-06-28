# Dependencies
from collections import namedtuple
import urllib2
import json
import os.path

# Modules

#classes
class Species:
    speciesName= ""
    speciesRecordings = []

    def speciesCount(self):
        return len(self.speciesRecordings)

    def __init__(self,species,recordings):
        self.speciesName = species
        self.recordings = recordings

    def __str__(self):
        definition = (self.speciesName,self.recordings)
        return str(definition)

# Functions
def DownloadApiJson():
    numPages,numSpecies = GetApiInfo()
    recordings = []

    # check if apiJSON exists
    if os.path.isfile(apiJSONPath):
        # the file does exists so we can just return that
        with open(apiJSONPath) as infile:
            recordings = json.load(infile)
        return recordings
    else:
        for(i in numPages):
            recordings.append(DownloadOnePage(i))

        # write this to file
        with open(apiJSONPath,"w") as outfile:
            json.dump(recordings,outfile)

        return recordings


def DownloadOnePage(pageNum):
    response = urllib2.urlopen(url+pageNum)
    data = json.load(response).recordings
    return data

def GetApiInfo():

    response = urllib2.urlopen(url+"1")
    data = json.load(response)
    numSpecies = data.numSpecies
    numPages = data.numPages
    return (numPages,numSpecies)


def SortRecordings(recordings):
    sortedSpecies = []
    # here we set all the species
    for (recording in recordings):
        if(!SpeciesContains(recording.en,sortedSpecies)):
            species = Species(recording.en,[recording])
            sortedSpecies.append(species)
    # now every single species is inside our sorted species
    # we can now fill up our species recordings

    for(recording in recordings):
        for (species in sortedSpecies):
            if(species.speciesName == recording.en):
                species.speciesRecordings.append(recording)
                break


def SpeciesContains(speciesName,sortedSpecies):
    for (species in sortedSpecies):
        if(species.speciesName == speciesName)
            return True
    return False

# Code

url = "http://www.xeno-canto.org/api/2/recordings?query=nr:1-1000000&page="

apiJSONPath = "recordings.json"

def StartGathering():
