import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import time #for time.sleep()
import utility_functions as uf #import utility functions
import gcode_translator as gt

from test_movement import print_smiley, print_square

msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
msb.ActivateRobot() #same as in the webinterface: activate Robot
msb.Home() #Home the robot
msb.ClearMotion()
msb.SendCustomCommand('ResetError()')
msb.SendCustomCommand('ResumeMotion()')
msb.SendCustomCommand('SetJointVelLimit(100)')
msb.SendCustomCommand('SetCartLinVel(200)')
msb.SendCustomCommand('SetBlending(60)')

#setpayload!!!!!--------------------------------


msb.SendCustomCommand('SetTrf(0,0,160,0,0,0)') #Set tooltip reference frame to 160 in front of the end of robot arm

#initial position
msb.SendCustomCommand(f'MovePose({150},{0},{65+30},180,0,-180)')
time.sleep(2)



#------------load ---------------------
#print_smiley(50,150,2)
#uf.z_hop(1,10,msb)
print_square(90,150,1,120,0, msb)
#draw asrl am logo
# Specify the path to your .gcode file
file_path = r"C:\Users\steph\OneDrive\_Studium\_Semester 6 (FS2024)\Bachelor Thesis\CODEBASE\BachelorThesis_SonoBone\gcode\Bone2.gcode"
# Extract coordinates
coordinates = gt.extract_coordinates(file_path)

# Write the coordinates
#gt.write_coordinates(coordinates, msb)
# Print the coordinates
#for coordinate in coordinates:
 #   print(coordinate)



# ----- present print ----
msb.SendCustomCommand(f'MovePose({150},{0},{65+20},180,0,-180)')




#finish the program
msb.WaitIdle()
msb.DeactivateRobot()
msb.Disconnect()