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
