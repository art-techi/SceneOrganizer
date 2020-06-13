''' Scene organizer
    Author: Meg Coleman
    Updated: June 13, 2020

    A simple script to organize objects in a maya scene.
    - rename: renames all of the items of a certain object type with a suffix identifying the given type
    - *reorder: (Idea) to reorder all the objects in the outliner of a scene given the type
    - groupItems: (WIP) combines all objects of the same type into their own group in the outliner

    Other ideas:
    - *reorder: reorder all the objects in the outliner of a scene given the type
    - rename the materials based on the model they are applied to
    - selects all textures in a scene and organizes them into folders depending on the mesh
    - merge textures with UDIMs into one single image and reorganize UVs to make use of the texture


'''

from maya import cmds

class CreateWindow(object):

    windowName = "Scene Organizer"

    def show(self):
        # check if window exists
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        # create window using custom name
        cmds.window(self.windowName)

        # build UI elements
        self.buildUI()
        if not cmds.window(self.windowName, query=True, exists=True):
            cmds.showWindow()

    def buildUI(self):
        column = cmds.columnLayout(rowSpacing=10)

        cmds.text(label="Rename: adds object type to end of name. (ie. sphere -> sphere_geo")
        cmds.text(label="Select an object in the outliner to rename. If nothing is selected, it will rename all objects.")
        cmds.text(label="Organize: reorders outliner by object type")
        cmds.text(label="Group: groups objects of the same type")
        # set space to put buttons on the same row
        cmds.rowLayout(numberOfColumns=3)
        # create buttons for UI
        cmds.button(label="RENAME", command=self.rename)
        cmds.button(label="ORGANIZE", command=self.reorderItems)
        cmds.button(label="GROUP", command=self.groupItems)
        cmds.setParent(column)

    def close(self, *args):
        cmds.deleteUI(self.windowName)

    def rename(self, *args):
        print "Starting rename."

        # use selection, fall back to all scene objects
        getObj = cmds.ls(selection=True, long=True, objectsOnly=True)
        if not len(getObj):
            getObj = cmds.ls(long=True, dag=True, objectsOnly=True)

        # check if selection made
        if len(getObj) == 0:
            print "Error. Nothing selected."
            return

        #print "objects: ", getObj

        # need to set order to shortest name last otherwise it will rename the object's shape before
        # the object itself
        getObj.sort(key=len, reverse=True)

        #print "objects ordered: ", getObj

        # run through selections
        for obj in getObj:
            children = cmds.listRelatives(obj, children=True) or []
            if len(children):
                child = children[0]
                objType = cmds.objectType(child)
            else:
                objType = cmds.objectType(obj)

            if objType == 'mesh':
                suffix = '_geo'
            elif objType == 'camera':
                suffix = '_cam'
            elif 'light' in objType.lower():
                suffix = '_light'
            else:
                continue

            # set new name
            shortName = obj.split('|')[-1]
            newName = shortName + suffix
            print shortName, '->', newName
            try:
                cmds.rename(obj, newName)
            except RuntimeError:
                print 'Renaming ' + obj + " failed."

    def reorderItems(self, *args):
        pass

    def groupItems(self, *args):
        print "Start group items."
        getObj = cmds.ls(objectsOnly=True)
        if not len(getObj):
            getObj = cmds.ls(objectsOnly=True, dag=True)

        if len(getObj) == 0:
            print "Error. No objects in the outliner."
            return

        '''nGeo = "Geo"
        nCam = "Cameras"
        nLight = "Lights"
        listMesh = cmds.group(empty=True, name=nGeo)
        listCams = cmds.group(empty=True, name=nCam)
        listLights = cmds.group(empty=True, name=nLight)'''
        listMesh = []
        listCams = []
        listLights = []

        for obj in getObj:
            children = cmds.listRelatives(obj, children=True) or []
            if len(children):
                child = children[0]
                objType = cmds.objectType(child)
            else:
                objType = cmds.objectType(obj)
            print objType
            if objType == 'mesh':
                listMesh.append(obj)
                #cmds.addAttr(nGeo, longName = obj, dataType = 'mesh')
            elif objType == 'camera':
                listCams.append(obj)
                #cmds.addAttr(nCam, longName = obj, dataType = 'mesh')
            elif objType.find('Light') != 0 or objType.find('light') != 0:
                listLights.append(obj)
                #cmds.addAttr(nLight, longName = obj)
            else:
                continue

        #print listMesh
        #emptyGroup = cmds.group(empty=True, name="Geo")
        if listMesh == [] or listCams == [] or listLights == []:
            print "Some groups might not have been created."
        # dictionary of lists, loop over list and check length
        cmds.group(listMesh, name="Geo")
        cmds.group(listCams, name="Cameras")
        cmds.group(listLights, name="Lights")

        # put objects of the same type into their own group
        # group(name="myGroup", empty=True)

if __name__ == '__main__':
    window = CreateWindow()
    window.show()