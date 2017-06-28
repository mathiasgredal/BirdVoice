# Dependencies
from collections import namedtuple
from urllib.request import urlopen
import ujson as json
import os.path
from progress.bar import Bar
# Modules

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

# Functions
def DownloadApiJson():
    numPages,numSpecies = GetApiInfo()
    print("Number of pages is: "+str(numPages))
    print("Number of species is: "+str(numSpecies))
    recordings = []

    # check if apiJSON exists
    if os.path.isfile(apiJSONPath):
        # the file does exists so we can just return that
        with open(apiJSONPath) as infile:
            recordings = json.load(infile)
        return recordings
    else:
        bar = Bar('IncrementalBar', max=numPages)
        for i in range(1,numPages+1):
            recordings.append(DownloadOnePage(i))
            bar.next()
        bar.finish()

        # write this to file
        with open(apiJSONPath,"w") as outfile:
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
    unsortedSpecies = []
    # here we set all the species
    bar = Bar('IncrementalBar', max=len(recordings))
    for page in recordings:
        for recording in page:
            if( SpeciesContains(recording["en"],unsortedSpecies) != True):
                species = Species(recording["en"],[])
                unsortedSpecies.append(species)
        bar.next()
    bar.finish()
    # now every single species is inside our sorted species
    # we can now fill up our species recordings
    bar1 = Bar('IncrementalBar', max=len(recordings))
    for page in recordings:
        for recording in page:
            for species in unsortedSpecies:
                if(species.speciesName == recording["en"]):
                    species.speciesRecordings.append(recording)
                    break
        bar1.next()
    bar1.finish()

    with open(sortedAPIJSONPath,"w") as outfile:
        json.dump(unsortedSpecies,outfile)

    # We can now begin the real sorting
    sortedSpecies = sorted(unsortedSpecies, key=lambda species: species.speciesCount)
    with open(sortedAPIJSONPath,"w") as outfile:
        json.dump(sortedSpecies,outfile)




def SpeciesContains(speciesName,sortedSpecies):
    for species in sortedSpecies:
        if(species.speciesName == speciesName):
            return True
    return False

# Code

url = "http://www.xeno-canto.org/api/2/recordings?query=nr:1-1000000&page="

apiJSONPath = "recordings.json"
sortedAPIJSONPath = "sortedRecordings.json"


def StartGathering():
    recordings = DownloadApiJson()
    sortedRecordings = SortRecordings(recordings)
    print(sortedRecordings)

StartGathering()
