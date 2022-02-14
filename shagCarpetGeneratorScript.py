# shagCarpetGenerator.py

import maya.cmds as cmds
import random
import math

from datetime import datetime
random.seed( datetime.now() )

# Delete Carpet Clusters Function
def deleteCarpet(name):
    
    if cmds.objExists( name + '*' ):
        cmds.delete( name + '*' )

# Duplicate Carpet Base Function
def duplicateBase(baseName):
    
    if cmds.objExists( baseName + '_original' ):
        cmds.showHidden( baseName + '_original' )
        if cmds.objExists( baseName ):
            cmds.delete( baseName )
        cmds.duplicate( baseName + '_original', name=baseName )
        cmds.hide( baseName + '_original' )

# Create Carpet Base Function
def createCarpetBase(shape, width, height):
    deleteCarpet('carpetCluster')
    deleteCarpet('carpetBase')
    
    if shape == 'Rectangle':
        cmds.polyPlane( sx=width*5, sy=height*5, w=width, h=height, name='carpetBase_original' )
    
    if shape == 'Circle':
        # Radius = width / 2
        size = width / 2.0
         
        if size == 0.5:
            numSides = 4
            circleSubdiv = 3
        elif size == 1:
            numSides = 4
            circleSubdiv = 3
        elif size == 1.5:
            numSides = 4
            circleSubdiv = 4
        elif size == 2:
            numSides = 4
            circleSubdiv = 4
        elif size == 2.5:
            numSides = 4
            circleSubdiv = 4
        elif size == 3:
            numSides = 3
            circleSubdiv = 5
        elif size == 3.5:
            numSides = 3
            circleSubdiv = 5
        elif size == 4:
            numSides = 4
            circleSubdiv = 6
        elif size == 4.5:
            numSides = 4
            circleSubdiv = 6
        elif size == 5:
            numSides = 4
            circleSubdiv = 6
            
        circleBase = cmds.polyDisc( sides=numSides, subdivisionMode=4, subdivisions=circleSubdiv, radius=size )
        cmds.rename( circleBase, 'carpetBase_original' )

# Create Carpet Strands Function
def createCarpetStrands(shape, width, height, carpetStrandColor, heightVariation, coverageType, faces, applyToCarpet):
    duplicateBase('carpetBase')
    
    # Clear old strands if new carpet
    if applyToCarpet == "New Carpet":
        deleteCarpet('carpetCluster')
        
    # Import carpet strand cluster    
    cmds.file( 'carpetStrandClusterModel.ass', i=True )
    cmds.sets( 'ArnoldStandIn', fe='ArnoldStandInDefaultLightSet' )
    carpetStrandCluster = cmds.select('ArnoldStandIn')
    carpetStrandCluster = cmds.rename(carpetStrandCluster, 'carpetCluster')
    
    # Apply selected shader color to carpet strands
    currShader = cmds.duplicate(carpetStrandColor, name='carpetShader#')
    print(currShader)
    cmds.select(carpetStrandCluster)
    cmds.hyperShade(assign=currShader[0])
    
    # Variables
    currWidth = 0
    currHeight = 0
    density = 0.3
    minClusterHeight = 1 - (heightVariation * 0.1)
    maxClusterHeight = 1 + (heightVariation * 0.1)
    baseHeight = 0.05
    
    # Cover entire base plane with carpet strands
    if coverageType == 'Entire Plane':
        if shape == 'Rectangle':
           
            numVerts = int((width*5) * (height*5) + (((width+height)/2.0)*10))
            currCarpetGroup = cmds.group( empty=True, name='carpetClusterGroup#' )
    
            # Cover all base plane vertices
            for i in range(0, numVerts):
                currCarpetCluster = cmds.instance( carpetStrandCluster, name='carpetCluster#' )
                cmds.parent( currCarpetCluster, currCarpetGroup )
                
                currPos = cmds.xform('carpetBase.vtx[%s]' % (i), q=True, t=True, ws=True)
                x = currPos[0]
                y = currPos[1]
                z = currPos[2]
    
                # Transform carpet strand position
                randRotate = random.uniform(0, 360)
                randScale = random.uniform(minClusterHeight, maxClusterHeight)
                cmds.move(x, y, z, currCarpetCluster)
                cmds.rotate(0, randRotate, 0, currCarpetCluster)
                cmds.scale(1, randScale, 1, currCarpetCluster)
            
        elif shape == 'Circle':
            
            # Radius = width / 2
            size = width / 2
             
            if size == 0.5:
                numVerts = 80
            elif size == 1:
                numVerts = 80
            elif size == 1.5:
                numVerts = 288
            elif size == 2:
                numVerts = 288
            elif size == 2.5:
                numVerts = 288
            elif size == 3:
                numVerts = 816
            elif size == 3.5:
                numVerts = 816
            elif size == 4:
                numVerts = 1088
            elif size == 4.5:
                numVerts = 1088
            elif size == 5:
                numVerts = 1088
                
            currCarpetGroup = cmds.group( empty=True, name='carpetClusterGroup#' )
    
            # Cover all base plane vertices
            for i in range(0, numVerts):
                currCarpetCluster = cmds.instance( carpetStrandCluster, name='carpetCluster#' )
                cmds.parent( currCarpetCluster, currCarpetGroup )
                
                currPos = cmds.xform('carpetBase.vtx[%s]' % (i), q=True, t=True, ws=True)
                x = currPos[0]
                y = currPos[1]
                z = currPos[2]
    
                # Transform carpet strand position
                randRotate = random.uniform(0, 360)
                randScale = random.uniform(minClusterHeight, maxClusterHeight)
                cmds.move(x, y, z, currCarpetCluster)
                cmds.rotate(0, randRotate, 0, currCarpetCluster)
                cmds.scale(1, randScale, 1, currCarpetCluster)
                
        # Extrude carpet base
        cmds.select( 'carpetBase' )
        cmds.polyExtrudeFacet( localTranslateZ=baseHeight )
        cmds.select( 'carpetBase' )
        cmds.scale(1.1, 1, 1.1)    
    
    # Cover only selected faces with carpet strands        
    elif coverageType == 'Selected Faces':
        # Convert faces to vertices
        selectedVertices = cmds.polyListComponentConversion( faces, tv=True )
        print(selectedVertices)
        
        # Change name of selected components to new carpet base name
        length = len(selectedVertices)
        for i in range (0, length):
            selectedVertices[i] = selectedVertices[i].replace("_original", "")
            print(selectedVertices[i])
        print(selectedVertices)
        
        # Select vertices
        cmds.select(selectedVertices)
        
        # Determine number of vertices based on base plane size and shape
        if shape == 'Rectangle':
            print('Rectangle true')
            numVerts = int((width*5) * (height*5) + (((width+height)/2.0)*10))
        elif shape == 'Circle':
            print('Circle true')
            # Radius = width / 2
            size = width / 2
             
            if size == 0.5:
                numVerts = 80
            elif size == 1:
                numVerts = 80
            elif size == 1.5:
                numVerts = 288
            elif size == 2:
                numVerts = 288
            elif size == 2.5:
                numVerts = 288
            elif size == 3:
                numVerts = 816
            elif size == 3.5:
                numVerts = 816
            elif size == 4:
                numVerts = 1088
            elif size == 4.5:
                numVerts = 1088
            elif size == 5:
                numVerts = 1088
        
        currCarpetGroup = cmds.group( empty=True, name='carpetClusterGroup#' )
    
        # Loop through all base plane vertices
        for i in range(0, numVerts):
            # Cover only vertices of selected faces
            if cmds.ls('carpetBase.vtx[%s]' % (i), sl=True): 
                print('carpetBase.vtx[%s] Selected' % (i))
                currCarpetCluster = cmds.instance( carpetStrandCluster, name='carpetCluster#' )
                cmds.parent( currCarpetCluster, currCarpetGroup )
                
                currPos = cmds.xform('carpetBase.vtx[%s]' % (i), q=True, t=True, ws=True)
                x = currPos[0]
                y = currPos[1]
                z = currPos[2]
    
                # Transform carpet strand position
                randRotate = random.uniform(0, 360)
                randScale = random.uniform(minClusterHeight, maxClusterHeight)
                cmds.move(x, y, z, currCarpetCluster)
                cmds.rotate(0, randRotate, 0, currCarpetCluster)
                cmds.scale(1, randScale, 1, currCarpetCluster)
                
            cmds.select(selectedVertices)
    
    cmds.hide( carpetStrandCluster )

# UI Window
class shagCarpetGeneratorUI():
    
    # Constructor
    def __init__(self):
        
        self.windowID = 'shagCarpetGeneratorWindow'
    
        # Check if window already open & close it
        if cmds.window( self.windowID, exists=True ):
            cmds.deleteUI( self.windowID )
        
        # Create new window
        self.window = cmds.window( self.windowID, title='Shag Carpet Generator', resizeToFitChildren=True)
        cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,150), (2,150), (3,125) ], columnAlign=[ (1,'right') ], columnSpacing=[ (2,15), (3,15)] )
        
        # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Formatting - Blank row
        cmds.text( label='Carpet Base Settings' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Pattern type
        cmds.text( label='Carpet Shape' )
        self.carpetShapeOptionMenu = cmds.optionMenu( 'carpetShapeOptionMenu', changeCommand=self.carpetLengthButton )
        cmds.menuItem( label='Rectangle' )
        cmds.menuItem( label='Circle' )
        cmds.separator( h=15, style='none' )
        
         # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Building foundation dimensions
        cmds.text( label='Carpet Width' )
        self.carpetWidth = cmds.intField( minValue=1, maxValue=10, value=5 )
        cmds.separator( h=10, style='none' )
        
        cmds.text( label='Carpet Length' )
        self.carpetHeight = cmds.intField( 'length', minValue=1, maxValue=10, value=5 )
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Generate carpet base plane button
        cmds.separator( h=15, style='none' )
        cmds.button( label = "Generate Base", command=self.carpetBaseSpecs )
        cmds.separator( h=15, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.text( label='Carpet Strand Settings' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Populate area buttons
        cmds.text( label='Strand Coverage' )
        self.coverageType = cmds.radioCollection()
        cmds.radioButton( label='Entire Plane', sl=True )
        cmds.radioButton( label='Selected Faces' )
        
        # Formatting - Blank row
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        cmds.separator( h=15, style='none' )
        
        # Color
        cmds.text( label='Color' )
        self.colorNode = cmds.createNode('aiStandardSurface', n='CarpetColor')
        cmds.attrColorSliderGrp( l='', at='%s.baseColor' % (self.colorNode), cw=[1, 0] )
        cmds.separator( h=15, style='none' )
        
         # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Strand Height Variation Intensity
        cmds.text( label='Strand Height Variation' )
        self.heightVariationIntensity = cmds.intSlider( minValue=1, maxValue=5, value=3, step=1)
        cmds.separator( h=10, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Generate carpet strands button
        cmds.separator( h=15, style='none' )
        cmds.button( label = "Generate Strands", command=self.carpetStrandSpecs )
        cmds.separator( h=15, style='none' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Populate area buttons
        cmds.text( label='Apply To:' )
        self.preserveStrands = cmds.radioCollection()
        cmds.radioButton( label='Same Carpet', sl=True )
        cmds.radioButton( label='New Carpet' )
        
        # Formatting - Blank row
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        cmds.separator( h=10, style='none' )
        
        # Display window   
        cmds.showWindow()
        
    def carpetLengthButton(self, *args):
        # Carpet shape
        carpetShape = cmds.optionMenu( self.carpetShapeOptionMenu, query=True, value=True )
        
        if(carpetShape == "Circle"):
            cmds.disable('length')
        else:
            cmds.disable('length', v=False)
        
    def carpetBaseSpecs(self, *args):
        
        # Carpet shape
        carpetShape = cmds.optionMenu( self.carpetShapeOptionMenu, query=True, value=True )
        
        # Base plane dimensions
        carpetWidth = cmds.intField( self.carpetWidth, query=True, value=True)
        carpetHeight = cmds.intField( self.carpetHeight, query=True, value=True)
        
        # Function call
        createCarpetBase(carpetShape, carpetWidth, carpetHeight)
    
    def carpetStrandSpecs(self, *args):
        # Carpet shape
        carpetShape = cmds.optionMenu( self.carpetShapeOptionMenu, query=True, value=True )
        
        # Base plane dimensions
        carpetWidth = cmds.intField( self.carpetWidth, query=True, value=True)
        carpetHeight = cmds.intField( self.carpetHeight, query=True, value=True)
        
        # Carpet color
        carpetColor = self.colorNode
        print(carpetColor)
        
        # Strand height 
        heightVariationIntensity = cmds.intSlider( self.heightVariationIntensity, query=True, value=True)
        
        # Strand coverage
        coverageType = cmds.radioCollection(self.coverageType, query=True, sl=True)
        strandCoverageSelected = cmds.radioButton(coverageType, query=True, label=True)        
        print(strandCoverageSelected)
        
        selectedFaces = cmds.ls(sl=True)
        print(selectedFaces)
        
        # Apply to new or same carpet
        carpetIteration = cmds.radioCollection(self.preserveStrands, query=True, sl=True)
        chosenCarpetIteration = cmds.radioButton(carpetIteration, query=True, label=True)        
        print(chosenCarpetIteration)
                
        # Function call
        createCarpetStrands(carpetShape, carpetWidth, carpetHeight, carpetColor, heightVariationIntensity, strandCoverageSelected, selectedFaces, chosenCarpetIteration)
        
# UI instantiation  
window = shagCarpetGeneratorUI()