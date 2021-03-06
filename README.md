# shagCarpetGenerator
### Shag Carpet Generator tool for Maya, Python script

## Overview
Used to create various shag carpets with settings controlled by a UI, this tool was developed as an alternative to Maya XGen, due to repeated problems of Maya crashing on my personal computer when XGen was being used.

## Implementation Instructions
To use this tool, copy and paste the python script into a new Python tab inside the Maya Script Editor window. The script can be directly used as a tool by saving the script to the shelf. 

Download "carpetStrandClusterModel.fbx" and import the model into your Maya scene. This tool relies on Arnold Stand-Ins to create the procedural carpets. Convert the model to an Arnold Stand-In.

In order for this script to run, the Arnold stand-in **must** be named as follows: 
```
carpetStrandClusterModel.ass
```
Additionally, the stand-in **must** be located inside of your Maya project folder.

## Usage Instructions
The UI enables users to choose the starting carpet shape, either rectangle or circle. The base shape can be further modified after being generated by selected vertices with soft selection and moving them as desired. Modification should be done within reason to keep consistent topology for the base plane, in order to ensure the base will be solidly covered by the carpet strands.

To modifiy the appearance of the carpet strands, strand height variation and color can be changed. Strand height variation intensity and color can be adjusted by using the provided selector and slider.

Patterns within the carpets themself can be created by using the face selection option, selecting sections of the base plane and differing colors when creating the same carpet.
