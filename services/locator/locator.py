from services.helper import helper

def coordinatesRelativeTo(relativeObj, diff_x = 0, diff_y = 0):
    x, y = relativeObj
    return helper.calculateObjCoordinates(x + diff_x, y + diff_y) 

bag = helper.calculateObjCoordinates(1314, 577) 
run = helper.calculateObjCoordinates(1328, 623)

move_1 = helper.calculateObjCoordinates(1206, 275) 
move_2 = coordinatesRelativeTo(move_1, diff_x=120)
move_3 = coordinatesRelativeTo(move_1, diff_y=60)
move_4 = coordinatesRelativeTo(move_1, diff_x=120, diff_y=60)