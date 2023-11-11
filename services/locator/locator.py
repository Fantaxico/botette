from services.helper import helper

def coordinatesRelativeTo(relativeObj, diff_x = 0, diff_y = 0):
    x, y, w, h = relativeObj
    return helper.calculateObjCoordinates(x + diff_x, y + diff_y) 

bag = helper.calculateObjCoordinates(1314, 577) 
run = helper.calculateObjCoordinates(1328, 623) 