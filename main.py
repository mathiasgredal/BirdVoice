# Dependencies
import sys
# Modules
import gatherer

# Functions
def GetArguments():
    arg = input("Pick Action [Create Dataset, Train Classifier, Make Prediction]")
    # validate input aka. check if it macthes our options
    if (arg == "Create Dataset"):
        return arg
    elif(arg == "Train Classifier"):
        return arg
    elif(arg == "Make Prediction"):
        return arg
    print("I don't understand you")
    sys.exit()

# Code
arg = GetArguments()
if(arg=="Create Dataset"):
    gatherer.StartGathering()
