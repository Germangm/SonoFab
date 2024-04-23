import math
import time #for time.sleep()
import utility_functions as uf #import utility functions
import stepper_control as sc
from globals import GlobalState
from globals import RobotStats


#---extract the coordinates from the gcode file---------------------------------------------------------
def extract_coordinates(file_path):
    coordinates = []

    
    with open(file_path, 'r') as file:
        i = 0
        
        for line in file:
            if i <44:
                i+=1
                continue
            if line.startswith(';TIME_ELAPSED'):
                break
            if line.startswith('G0') or line.startswith('G1'):
                x = None
                y = None
                z = None
                alpha = None
                beta = None
                gamma = None
                e = None
                er = False
                for command in line.split():
                    if command.startswith('X'):
                        x = float(command[1:])
                    elif command.startswith('Y'):
                        y = float(command[1:])
                    elif command.startswith('Z'):
                        try:
                            z = float(command[1:])
                        except:
                            er = True
                    elif command.startswith('E'):
                        e = float(command[1:])
                coordinates.append([x, y, z, e, er])
                
    return coordinates

#---write the coordinates (2D print) to the robot ---------------------------------------------------------
def write_coordinates(coordinates, self, x_offset, y_offset):
    
    #set printing speed
    #self.SendCustomCommand(f'SetJointVelLimit({RobotStats().joint_vel_limit})')
    #self.SendCustomCommand(f'SetCartLinVel({RobotStats().max_linvel})')

    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().joint_vel_limit})')

    #coordinates consist of [x, y, z, e, er]        
    z_0 = RobotStats().min_z 

    #offset from modify placement
    
    non_none_z = 0
    non_none_x = 0
    non_none_y = 0
    previous_percent = 0
    
    non_none_e = 0
    last_e = 0
    i = 0

    length = len(coordinates)
    for x, y, z, e, er in coordinates:
        
        print(f'--{i}--')

        #wait in this position when the print is paused
        while(GlobalState().printing_state != 2): #print paused 
            if GlobalState().printing_state == 5:
                print("exit path 1")
                print(GlobalState().printing_state)
                return
            time.sleep(0.1)
        
        # Check printing_state if the print is stoppedc
            if GlobalState().printing_state == 5:  
                print("exit path 2")
                print(GlobalState().printing_state)
                return

        i += 1 #index
        GlobalState().current_line = i
        
        GlobalState().current_progress = round(float(i)/float(length) * 100, 1)
        
        
        

        #GlobalState().terminal_text += f'{i} / {length}'

        #blank line -> skip
        if(x == None and y == None and z == None):
            continue
        #reference so that constant z is managed if z is not specified
        if(z != None):
            non_none_z = z
        if(x != None):
            non_none_x = x
        if(y != None):
            non_none_y = y  
        if(e != None):
            non_none_e = e

        ''' waiting for future implementation
        #if er = True, continue with the next line
        if(er == True):
            print('Error was TRUE -> continued')
            continue

        #extrusion information
        if(e != None):
            print(f'extrusion: {e}')
            #time.sleep(1)
        '''

        '''
        #wait for the last position to be nearly reached
        while(GlobalState().semaphore != 0): 
            if GlobalState().printing_state == 5:
                print("exit path 3")
                print(GlobalState().printing_state)
                return
            time.sleep(0.1)
        '''
        
        #if x and y are not specified, move to current position with z offset
        if (x == None or y == None):
            
            #print(f'{non_none_x+x_offset}, {non_none_y + y_offset}, {z+z_0+10}')
            uf.commandPose(non_none_x+x_offset, non_none_y + y_offset, z + z_0 + 10 + GlobalState().user_z_offset, 180, 0, -180, self)
            GlobalState().last_pose = [non_none_x+x_offset, non_none_y + y_offset, z + z_0 + 10 + GlobalState().user_z_offset, 180, 0, -180]
            if(e != None):
                sc.send_position(e - last_e)
                last_e = e
            
            #wait for position to be almost reached
            uf.WaitReachedPose([non_none_x+x_offset, non_none_y + y_offset, z + z_0 + 10 + GlobalState().user_z_offset, 180, 0, -180])
            
            
            #sc.send_speed(0)
            GlobalState().semaphore += 1
            #uf.add_target_pose([non_none_x+x_offset, non_none_y + y_offset, z + z_0 + 10 + GlobalState().user_z_offset, 180, 0, -180])
            
        elif z == None:
            
            uf.commandPose(x+x_offset, y+y_offset, non_none_z + z_0 + GlobalState().user_z_offset, 180, 0, -180, self)
            GlobalState().last_pose = [x+x_offset, y+y_offset, non_none_z + z_0 + GlobalState().user_z_offset, 180, 0, -180]
            if(e != None ):
                #sc.send_position(e - last_e)
                last_e = e

            #wait for position to be almost reached
            uf.WaitReachedPose([x+x_offset, y + y_offset, non_none_z + z_0 + 10 + GlobalState().user_z_offset, 180, 0, -180])
            GlobalState().semaphore += 1
            #sc.send_speed(0)
            ''' removed in command pose to wait'''
            #uf.add_target_pose([x+x_offset, y+y_offset, non_none_z + z_0 + GlobalState().user_z_offset, 180, 0, -180])
            
        #throw exception
        else:
            print("!-!-!-!-!Line skip error!-!-!-!-!")
            #GlobalState().terminal_text += "Line skip error"

        time.sleep(0.01)
        
        #-------------------finished print -----------------------------
    
    sc.send_speed(0)
    #set speed higher again
    GlobalState().msb.SendCustomCommand(f'SetJointVelLimit({RobotStats().start_joint_vel_limit})')
    uf.endpose(self)
    #print finished
    GlobalState().printing_state = 4
    return

def modify_placement(coordinates):

    min_x = coordinates[0][0]
    max_x = coordinates[0][0]
    max_y = coordinates[0][1]
    min_y = coordinates[0][1]

    #get max and min x and y
    for x, y, z, e, er in coordinates:
        if x != None:
            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x
        if y != None:
            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y
    print(max_x, min_x, max_y, min_y)

    #check if dimensions are feasible
    if (max_x - min_x) > (RobotStats().max_x - RobotStats().min_x):
        print("X-dimension too large")
        GlobalState().terminal_text += "\nX-dimensions are too large for the printebed for Δx = " + str(max_x-min_x)+ " \n" + "It must be within Δx = " + str(RobotStats().max_x - RobotStats().min_x)
        time.sleep(2)
        return None, None
    if (max_y - min_y) > (RobotStats().max_y - RobotStats().min_y):
        print("Y-dimension too large")
        GlobalState().terminal_text += "\nY-dimension are too large for the printebed for Δy = " + str(max_y-min_y)+ " \n" + "It must be within Δy = " + str(RobotStats().max_y - RobotStats().min_y) 
        time.sleep(2)
        return None, None
        
    
    
    #calculate offset so that the print is centered
    '''         (align to the lower edge)      + (half the distance left if evenly spaced)     '''
    x_offset = (-min_x + RobotStats().min_x) + ((RobotStats().max_x - RobotStats().min_x) - (max_x - min_x)) /2
    '''         (align to the left edge)      + (half the distance left if evenly spaced)      '''
    y_offset = (-min_y + RobotStats().min_y) + ((RobotStats().max_y - RobotStats().min_y) - (max_y - min_y )) /2


    return x_offset, y_offset


def start_print():

    x_offset = 0
    y_offset = 0
    
    #Extract coordinates
    GlobalState().terminal_text += "Extracting coordinates from file..."
    coordinates = extract_coordinates(GlobalState().filepath)

    x_offset, y_offset = modify_placement(coordinates)
    
    if x_offset == None or y_offset == None:
        GlobalState().terminal_text += "Select a different File that fits"
        GlobalState().confirmed = True
        GlobalState().printing_state = 5
        return
        
    
    time.sleep(2)
    GlobalState().terminal_text += " --done! - Starting print--"
    
    #wait for msb != None with timeout
    start_time = time.time() #reset timer
    timeout = False
    while (GlobalState().msb == None and timeout):
        if(time.time() - start_time > 10):
            timeout = True
            break
        time.sleep(0.1)

    if timeout == True:
        GlobalState().terminal_text += "Robot not connected"
        GlobalState().confirmed = True
        GlobalState().printing_state = 5
        return

    time.sleep(1)
    
    #set starting position
    uf.startpose(GlobalState().msb)
   
    
    GlobalState().msb.WaitIdle()

    GlobalState().printing_state = 2
    #start printing
    write_coordinates(coordinates,GlobalState().msb, x_offset, y_offset)

    return



    