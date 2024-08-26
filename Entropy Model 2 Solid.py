from vpython import *
from math import *
import time

#units J/K
k_B = 1.380649 * 10**-23

#setting number of atoms
n_atoms1 = 100
n_atoms2 = 100

#when making the boxes relative we need a side-length
side1 = n_atoms1**(1/3)
side2 = n_atoms2**(1/3)

#setting number of oscillators
N1 = 3*n_atoms1
N2 = 3*n_atoms2

#setting total quanta of energy
qTot = 10

quantaChoices = ["10","20","30","40","50","60","70","80","90","100","110","120","130","140","150"]

atomsChoices = ["100","200","300","400","500"]

flag = False

#creating a canvas in vpython for visualisations
scene = canvas(width = 610, height = 200,background = color.black,align="left")
#title in bold with two spaces
scene.title = "<b>Entropy in Blocks in Contact<b>\n\n"
scene.userspin = True
scene.userpan = False
#scene.userzoom = False

box1 = box(pos=vec(-side1/2, 0, 0), length=side1, height=side1, width=side1, color=color.cyan)
box2 = box(pos=vec(side2/2, 0, 0), length=side2, height=side2, width=side2, color=color.red)

box1Label = label(pos=vec(-side1/2, 0, 0),line = False,text="Box 1",background = color.cyan,color=color.black)
box2Label = label(pos=vec(side2/2, 0, 0),line = False,text="Box 2",background = color.red,color=color.black)

#if side2>side1:
#    box1.pos = vec(-side1/2, (side1-side2)/2, 0)
#else:
#    box2.pos = vec(side2/2, (side2-side1)/2, 0)


def changeQuanta():
    global qTot
    global flag
    global quantaMenu
    global numWaysGraph
    global entropyGraph
    global peakCurve
    global entropy1Curve
    global entropy2Curve
    global entropyTotCurve
#breaking the previous while loop
    flag = True
#    time.sleep(0.5)
    qTot = int(quantaMenu.selected)
    
    numWaysGraph.delete()
    entropyGraph.delete()
    peakCurve.delete()
    entropy1Curve.delete()
    entropy2Curve.delete()
    entropyTotCurve.delete()
    
    recalculate()

def changeAtoms1():
    global n_atoms1
    global N1
    global side1
    global flag
    global n_atoms1Menu
    global numWaysGraph
    global entropyGraph
    global peakCurve
    global entropy1Curve
    global entropy2Curve
    global entropyTotCurve
#breaking the previous while loop
    flag = True
#    time.sleep(0.5)
#resetting number of atoms
    n_atoms1 = int(n_atoms1Menu.selected)
    side1 = n_atoms1**(1/3)

#resetting number of oscillators
    N1 = 3*n_atoms1
    N1Display.text = N1

    numWaysGraph.delete()
    entropyGraph.delete()
    peakCurve.delete()
    entropy1Curve.delete()
    entropy2Curve.delete()
    entropyTotCurve.delete()

    recalculate()

def changeAtoms2():
    global n_atoms2
    global N2
    global side2
    global flag
    global n_atoms2Menu
    global numWaysGraph
    global entropyGraph
    global peakCurve
    global entropy1Curve
    global entropy2Curve
    global entropyTotCurve
#breaking the previous while loop
    flag = True
#    time.sleep(0.5)
#resetting number of atoms
    n_atoms2 = int(n_atoms2Menu.selected)
    side2 = n_atoms2**(1/3)

#resetting number of oscillators
    N2 = 3*n_atoms2
    N2Display.text = N2

    numWaysGraph.delete()
    entropyGraph.delete()
    peakCurve.delete()
    entropy1Curve.delete()
    entropy2Curve.delete()
    entropyTotCurve.delete()

    recalculate()
        
scene.append_to_caption("    ")
scene.append_to_caption("Number of atoms in block 1 = ")
n_atoms1Menu = menu(bind = changeAtoms1, choices=atomsChoices)
scene.append_to_caption("\n\n")
scene.append_to_caption("    ")
scene.append_to_caption("Number of one dimensional oscillators in block 1 = ")
N1Display = wtext(pos=scene.caption_anchor, text = N1)
scene.append_to_caption("\n\n")
scene.append_to_caption("    ")
scene.append_to_caption("Number of atoms in block 2 = ")
n_atoms2Menu = menu(bind = changeAtoms2, choices=atomsChoices)
scene.append_to_caption("\n\n")
scene.append_to_caption("    ")
scene.append_to_caption("Number of one dimensional oscillators in block 2 = ")
N2Display = wtext(pos=scene.caption_anchor, text = N2)
scene.append_to_caption("\n\n")
scene.append_to_caption("    ")
scene.append_to_caption("Total number of quanta of energy = ")
quantaMenu = menu(bind = changeQuanta, choices=quantaChoices)
scene.append_to_caption("\n\n\n\n")

def recalculate():
    global box1
    global box2
    global box1Label
    global box2Label
    global flag
    global side1
    global side2
    global qTot
    global numWaysGraph
    global entropyGraph
    global peakCurve
    global entropy1Curve
    global entropy2Curve
    global entropyTotCurve

    
    box1.length = side1
    box1.height = side1
    box1.width = side1

    box2.length = side2
    box2.height = side2
    box2.width = side2

    box1.pos = vec(-side1/2, 0, 0)
    box2.pos = vec(side2/2,0,0)

    box1Label.pos = vec(-side1/2, 0, 0)
    box2Label.pos = vec(side2/2,0,0)

#    if side2>side1:
#        box1.pos = vec(-side1/2,(side1-side2)/2, 0)
#        box2.pos = vec(side2/2, 0, 0)
#    else:
#        box1.pos = vec(-side1/2, 0, 0)
#        box2.pos = vec(side2/2, (side2-side1)/2, 0)
    
    #creating a list that will contain all data points for number of ways
    graphNumWays = []

    #similar lists for entropy curves
    graphEntropy1 = []
    graphEntropy2 = []
    graphEntropyTot =[]
    
    peakPoint = [0,0]
    zeroGradPoint = [0,0]
    
    #cycling through 0 quanta in the first block to all quanta in the first block
    for i in range(0,qTot+1,1):
        #number of quanta in the first block
        q1 = i
        #number of quanta in the second block
        q2 = qTot-q1
        
        #number of ways of arranging q1 quanta within the first block
        numWays1 = int(combin(q1 + N1-1,q1))
        
        #calculating entropy from number of ways
        entropy1 = k_B*log(numWays1)
        
        #same for second block
        numWays2 = int(combin(q2 + N2-1,q2))
        entropy2 = k_B*log(numWays2)
        
        #multiply to find the total number of ways of arranging the quanta in that split
        numWaysTot = numWays1*numWays2
        #again calculate the entropy
        entropyTot = k_B*log(numWaysTot)
        
        if numWaysTot > peakPoint[1]:
            peakPoint = [i,numWaysTot]
            zeroGradPoint = [i,entropyTot]
        
        #creating an [x,y] list for the data point of each curve
        dataPointNumWays = [q1, numWaysTot]
        dataPointEntropy1 = [q1,entropy1]
        dataPointEntropy2 = [q1,entropy2]
        dataPointEntropyTot = [q1,entropyTot]
                               
        #appending the data point to the total graph lists
        graphNumWays.append(dataPointNumWays)
        graphEntropy1.append(dataPointEntropy1)
        graphEntropy2.append(dataPointEntropy2)
        graphEntropyTot.append(dataPointEntropyTot)

    gradientList = [[0,zeroGradPoint[1]],[qTot,zeroGradPoint[1]]]
    
    #creating the graphs and then plotting the curves to the corresponding graph from the datapoints list created
    numWaysGraph = graph(title='Blocks in contact (number of ways)', xtitle='q1', ytitle='Number of ways',fast=False, align="left",height=290,width=610)
    entropyGraph = graph(title='Blocks in contact (entropy)', xtitle='q1', ytitle='Entropy, S/(J/K)',fast=False,align="right",height=290,width=610)

    time.sleep(0.2)
    
    peakCurve = gcurve(color=color.red,data=graphNumWays, graph = numWaysGraph)
    entropy1Curve = gcurve(color = color.blue,data = graphEntropy1, graph = entropyGraph)
    entropy2Curve = gcurve(color = color.cyan,data = graphEntropy2, graph = entropyGraph)
    entropyTotCurve = gcurve(color = color.red,data = graphEntropyTot, graph = entropyGraph)

    peakPointPlot = gdots(color=color.black,graph = numWaysGraph,data=peakPoint,radius=4)
    gradient = gcurve(color=color.black,data = gradientList,graph = entropyGraph,width=1)

    while True:
        rate(2)
        if flag == True:
            flag = False
            break

recalculate()
