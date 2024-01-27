import maya.cmds as cmds
import maya.mel as mel

anim2ShelfWindow = ""

def buildAnimScript(rangeMin, rangeMax, rememberNamespace, sText, tText):
    scriptStr = "import maya.cmds as m\n\n"
    scriptStr += "t=True\n"
    scriptStr += "f=False\n"
	
    thisSel = cmds.ls(sl=True)
    if len(thisSel) > 0:
	    #Check if all selected objects have single namespace
        singleNamespace = True
        for i in range(0, len(thisSel)):
            if i == 0 and thisSel[i].rfind(":") == -1:
                lastNamespace = ""
            elif i == 0:
                lastNamespace = thisSel[i][0:thisSel[i].rfind(":")]+":"
                
            thisNamespace = thisSel[i][0:thisSel[i].rfind(":")]+":"
            if not thisNamespace.startswith(lastNamespace) and not lastNamespace.startswith(thisNamespace):
                singleNamespace = False
                break
        
        if cmds.checkBox(rememberNamespace, q=True, value=True) == True:
            if singleNamespace:
                scriptStr += "sngNS=\""+lastNamespace+"\"\n"
                scriptStr += "useNS=m.confirmDialog(t='anim2shelf', m=\"Use first selected object's namespace?\", b=['Yes','No'], db='No', cb='No', ds='No')\n"
                scriptStr += "if len(m.ls(sl=t))==0 and useNS==\"Yes\":\n"
                scriptStr += "    m.error('No object is selected for a new namespace.')\n"
                scriptStr += "thisNS=m.ls(sl=t)[0][0:m.ls(sl=t)[0].rfind(':')]+':'\n"
                print "Single namespace selected."
            else:
                print "Multiple namespaces selected."
				
        thisSourceText = cmds.textFieldGrp(sText, q=True, text=True)
        thisTargetText = cmds.textFieldGrp(tText, q=True, text=True)
        if thisSourceText != "" and thisTargetText != "":
            scriptStr += "sT=\""+thisSourceText+"\"\n"
            scriptStr += "tT=\""+thisTargetText+"\"\n"
        
        for ctrl in thisSel:
            ctrlAttrs = cmds.listAnimatable(ctrl)
            for fullAttr in ctrlAttrs:
                attr = ctrl+"."+cmds.attributeName(fullAttr, short=True)
                scriptStr += "#Attr "+attr+"\n"
                scriptStr += "a=\""+attr+"\"\n"
                
                if singleNamespace and cmds.checkBox(rememberNamespace, q=True, value=True) == True:
                    scriptStr += "if useNS==\"Yes\":\n"
                    scriptStr += "    a=a.replace(sngNS, thisNS)\n"
                if thisSourceText != "" and thisTargetText != "":
                    scriptStr += "a=a.replace(sT, tT)\n"
            
                attrKeys = cmds.keyframe(attr, q=True, time=(rangeMin,rangeMax), timeChange=True)
                attrValues = cmds.keyframe(attr, q=True, time=(rangeMin,rangeMax), valueChange=True)
                
                if attrKeys is not None:
					for i in range(len(attrKeys)):
						attrKey_g = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), g=True)
						attrKey_itt = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), inTangentType=True)
						attrKey_ott = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), outTangentType=True)
						attrKey_ia = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), inAngle=True)
						attrKey_oa = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), outAngle=True)
						attrKey_iw = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), inWeight=True)
						attrKey_ow = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), outWeight=True)
						attrKey_l = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), lock=True)
						attrKey_wl = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), weightLock=True)
						attrKey_wt = cmds.keyTangent(attr, q=True, time=(attrKeys[i],attrKeys[i]), weightedTangents=True)
						
						scriptStr += "#Key "+str(attrKeys[i])+"\n"
						scriptStr += "try:\n"
						scriptStr += "    m.setKeyframe(a,e=t,t="+str(attrKeys[i])+",v="+str(attrValues[i])+")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),g="+str(attrKey_g[2]).title()+")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),l="+str(attrKey_l[0])+")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),wt="+str(attrKey_wt[0])+")\n"
						if attrKey_wt[0]:
							scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),wl="+str(attrKey_wl[0])+")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),a=True,ow="+str(attrKey_ow[0])+",iw="+str(attrKey_iw[0])+")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),a=True,oa="+str(attrKey_oa[0])+",ia="+str(attrKey_ia[0])+")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),itt=\""+str(attrKey_itt[0])+"\")\n"
						scriptStr += "    m.keyTangent(a,e=t,t=("+str(attrKeys[i])+","+str(attrKeys[i])+"),ott=\""+str(attrKey_ott[0])+"\")\n"
						scriptStr += "except:\n"
						scriptStr += "    pass\n"
						scriptStr += "\n"
    else:
        return False
    
    return scriptStr

def createShelfButton(animRangeField, iconTextField, annotationField, rememberNamespace, sText, tText):
    rangeMin = cmds.floatFieldGrp(animRangeField, q=True, value1=True)
    rangeMax = cmds.floatFieldGrp(animRangeField, q=True, value2=True)
    thisAnim = buildAnimScript(rangeMin, rangeMax, rememberNamespace, sText, tText)
    
    if(thisAnim):
        animIconLabelVal = cmds.textFieldGrp(iconTextField, q=True, text=True)
        animNoteVal = cmds.textFieldGrp(annotationField, q=True, text=True)
        
        gShelfTopLevel = mel.eval("global string $gShelfTopLevel; $tempMelVar=$gShelfTopLevel;")
        currentShelf = cmds.tabLayout(gShelfTopLevel, q=True, selectTab=True)
        cmds.shelfButton(p=currentShelf, annotation=animNoteVal, iol=animIconLabelVal, stp="python", image1="anim2shelf.png", command=thisAnim)

def setAnimRange(rangeField):
    cmds.floatFieldGrp(rangeField, e=True, value1=cmds.playbackOptions(q=True, min=True), value2=cmds.playbackOptions(q=True, max=True))
    
def closeAnim2Shelf(win):
    cmds.deleteUI(win, window=True)

def anim2Shelf():
    global anim2ShelfWindow
    if (cmds.window(anim2ShelfWindow, exists=True)):
        cmds.deleteUI(anim2ShelfWindow)
    anim2ShelfWindow = cmds.window(t="Anim2Shelf", s=False, mxb=False, width=400)
    
    cmds.columnLayout()
    
    animIconLabel = cmds.textFieldGrp(label='Icon Label', text='anm1')
    animNote = cmds.textFieldGrp(label='Tooltip', text='Import animation from Anim2Shelf.')
    animRangeField = cmds.floatFieldGrp(numberOfFields=2, label='Frame range', value1=cmds.playbackOptions(q=True, min=True), value2=cmds.playbackOptions(q=True, max=True))

    sourceTextReplace = cmds.textFieldGrp(label='Replace text', text='')
    targetTextReplace = cmds.textFieldGrp(label='with text', text='')

    rememberNamespace = cmds.checkBox(label='Another Namespace (If single)', ann="Check if you want the ability to paste animation onto another rig instance.\nUncheck if the destination is same as the source.", value=True)
	
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(133, 133, 133), columnAlign=(1, 'right'))
    cmds.button(width=133, label="Create Button", ann="Create button in the current shelf for selected objects.", command="anim2shelf.createShelfButton(\""+animRangeField+"\", \""+animIconLabel+"\", \""+animNote+"\", \""+rememberNamespace+"\", \""+sourceTextReplace+"\", \""+targetTextReplace+"\")")
    cmds.button(width=133, label="Grab Range", ann="Copy frame range from timeslider.", command="anim2shelf.setAnimRange(\""+animRangeField+"\")")
    cmds.button(width=133, label="Close", ann="Close anim2Shelf.", command="anim2shelf.closeAnim2Shelf(\""+anim2ShelfWindow+"\")")
    
    cmds.showWindow(anim2ShelfWindow)