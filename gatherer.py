# Dependencies
from collections import namedtuple
from urllib.request import urlopen
import ujson as json
import os.path
from progress.bar import Bar
import configparser
# Modules
import binarytree as bt
# Variables

config = configparser.ConfigParser()
config.read("config.ini")

url = "http://www.xeno-canto.org/api/2/recordings?query=nr:1-1000000&page="

apiJSON = config["GATHERER"]["apiJSON"]
EmptySpeciesJSON = config["GATHERER"]["emptySpeciesJSON"]
unsortedSpeciesJSON = config["GATHERER"]["unsortedSpeciesJSON"]
sortedSpeciesJSON = config["GATHERER"]["sortedSpeciesJSON"]

SpeciesToIgnore = json.loads(config["GATHERER"]["SpeciesToIgnore"])

#classes
class Species:
    speciesName= ""
    speciesRecordings = []

    speciesCount = len(speciesRecordings)

    def __init__(self,species,recordings):
        self.speciesName = species
        self.recordings = recordings

    def __str__(self):
        definition = (self.speciesName,self.recordings)
        return str(definition)

    def __repr__(self):
        return repr((self.speciesName, self.speciesCount, self.speciesRecordings))

    def GetTuple(self):
        definition = (self.speciesName,self.recordings)
        return definition

# Functions
def DownloadApiJson():
    numPages,numSpecies = GetApiInfo()
    print("Number of pages is: "+str(numPages))
    print("Number of species is: "+str(numSpecies))
    recordings = []

    # check if apiJSON exists
    if os.path.isfile(apiJSON):
        # the file does exists so we can just return that
        with open(apiJSON) as infile:
            recordings = json.load(infile)
        return recordings
    else:
        bar = Bar('IncrementalBar', max=numPages)
        for i in range(1,numPages+1):
            recordings.append(DownloadOnePage(i))
            bar.next()
        bar.finish()

        # write this to file
        with open(apiJSON,"w") as outfile:
            json.dump(recordings,outfile)

        return recordings


def DownloadOnePage(pageNum):
    response = urlopen(url+str(pageNum))
    data = json.load(response)["recordings"]
    return data

def GetApiInfo():
    response = urlopen(url+"1")
    data = json.load(response)
    numSpecies = data["numSpecies"]
    numPages = data["numPages"]
    return (numPages,numSpecies)


def SortRecordings(recordings):
    EmptySpecies = []

    if os.path.isfile(EmptySpeciesJSON):
        print("We will jump right to the second step of SortRecordings() as we can use EmptySpecies.json instead")
        print("Delete sortedRecordings.json & unsortedRecordings.json & EmptySpecies.json from the directory to redo the sorting ")
        with open(EmptySpeciesJSON) as infile:
            EmptySpecies = json.load(infile)
    else:
        EmptySpecies = FindAllSpecies(recordings)
        with open(EmptySpeciesJSON,"w") as outfile:
            json.dump(EmptySpecies,outfile)
        EmptySpecies = json.loads(json.dumps(EmptySpecies))

    unsortedSpecies = []

    if os.path.isfile(unsortedSpeciesJSON):
        print("We will jump right to the second step of SortRecordings() as we can use unsortedRecordings.json instead")
        print("Delete sortedRecordings.json & unsortedRecordings.json & EmptySpecies.json from the directory to redo the sorting ")
        # if the sortedAPIJSONPath doesnt exist there is still
        # hope for the unsorted file exists so we can skip some work
        with open(unsortedSpeciesJSON) as infile:
            unsortedSpecies = json.load(infile)
    else:
        unsortedSpecies = GatherAllRecordings(recordings, EmptySpecies)
        with open(unsortedSpeciesJSON,"w") as outfile:
            json.dump(unsortedSpecies,outfile)
        unsortedSpecies = json.loads(json.dumps(unsortedSpecies))

    sortedSpecies = []

    if os.path.isfile(sortedSpeciesJSON):
        print("We will skip the SortRecordings() and use the sortedRecordings.json instead")
        print("Delete sortedRecordings.json & unsortedRecordings.json & EmptySpecies.json from the directory to redo the sorting ")
        # if sortedAPIJSONPath exists means we have done this before
        # and we dont need to do it again
        with open(sortedSpeciesJSON) as infile:
            sortedSpecies = json.load(infile)
    else:
        sortedSpecies = SortAllSpecies(unsortedSpecies)
        with open(sortedSpeciesJSON,"w") as outfile:
            json.dump(sortedSpecies,outfile)
        sortedSpecies = json.loads(json.dumps(sortedSpecies))

    return sortedSpecies



def FindAllSpecies(recordings):
    unsortedSpecies = []

    bar = Bar('Finding All Species', max=len(recordings))

    for page in recordings:
        for recording in page:
            if( SpeciesContains(recording["en"],unsortedSpecies) != True):
                species = Species(recording["en"],[])
                unsortedSpecies.append(species)
        bar.next()

    bar.finish()

    # remove the species to ignore
    for species in unsortedSpecies:
        if(species.speciesName in SpeciesToIgnore):
            unsortedSpecies.remove(species)


    return unsortedSpecies


def GatherAllRecordings(recordings,EmptySpecies):

    # this is done to make our life easier
    allRecordings = []

    for page in recordings:
        for recording in page:
            if(recording is None):
                continue
            allRecordings.append(recording)

    bar = Bar('Filling EmptySpecies', max=len(allRecordings))

    for recording in allRecordings:
        recordingSTR = str(recording)
        recordingSpecies = ExtractSpeciesFromJSON(recordingSTR)
        # check for errors
        if(recordingSpecies != "Error"):
            for i in range(0,len(EmptySpecies)):
                if(EmptySpecies[i]["speciesName"] == recordingSpecies):
                    EmptySpecies[i]["speciesRecordings"].append(recordingSTR)
                    break

        bar.next()
    bar.finish()
    return EmptySpecies


def SortAllSpecies(unsortedSpecies):
    tree = bt.Tree()
    for species in unsortedSpecies:
        tree.addValue(len(species["speciesRecordings"]),species)
    l = tree.traverse()
    return l[:10]

def SpeciesContains(speciesName,sortedSpecies):
    for species in sortedSpecies:
        if(species.speciesName == speciesName):
            return True
    return False

def ExtractSpeciesFromJSON(recording):
    try:
        beforeEN = recording.find(", \'en\': \'")+9
        afterEN = recording.find(", \'rec\': \'")-1
        return recording[beforeEN:afterEN]
    except BaseException:
        print("error in ExtractSpeciesFromJSON")
        return "Error"


# Code

def StartGathering():
    recordings = DownloadApiJson()
    sortedRecordings = SortRecordings(recordings)
    #print(sortedRecordings)

StartGathering()
