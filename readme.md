This Neural Network uses keras tensorflow to classify bird bioacoustics.

The project is split into 5 modules.


#### 1. Gathering
Here we get the audio data from [Xeno-Canto](http://xeno-canto.org/), and we are also provided the labels for the sounds
###### Step by Step
1. Download all pages from Xeno-Canto and write it to a json file, or load the json file if we have written it before.
2. Sort the json by the number of birds in each species.
3. Pick the recordings of the n first species.
4. Download the recordings,
5. Put the file path into an array looking like this

        Bird Species Array

        [
            Little Tinamou,
            [
            path1, path2, path3, path4
            ]
            Cinereous Tinamou,
            [
            path1, path2, path3, path4
            ]
        ]
6. Now we pass our array to the Segmentation engine

#### 2. Segmentation
After we have gathered a sound we want to cut it up into five second pieces because it is a lot easier for the classifier the receive data having the same shape.




###### Step by Step
1. Use p



#### 3. Feature Extraction  
We will then extract the spectrogram from the bird calls and use that to input into the classifier.

#### 4. Classification
This is the difficult part here we take the five second spectrogram and input into the pre-trained classifier and it will give us the output

#### 5. Voting

With all the answers we get from the classifier we will figure out the correct bird species.
