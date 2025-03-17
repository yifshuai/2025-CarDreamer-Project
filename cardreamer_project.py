import carla
import matplotlib.pyplot as plt
import subprocess
import math as m
import time
import psutil

#Global Parameters:
forward_classification_boundries=[-5,5]

#calculate theta helper function
def theta(deltax,deltay):
  theta=m.degrees(m.atan2(deltay,deltax))
  if theta<0:
    theta+=360
  return theta

#gets yaw of each segment, assumes yaw_segment0 = 0, yaw_segmentn = 0
def get_yaws(waypoint_list,num_segments):
  if(len(waypoint_list)<num_segments):
    num_segments=len(waypoint_list)
  l=(int)(len(waypoint_list)/num_segments)
  waypoint_list_segments=waypoint_list[0::l]
  thetas=[]
  deltax=[]
  deltay=[]
  for i in range(len(waypoint_list_segments)-1):
    deltax.append(waypoint_list_segments[i+1][0]-waypoint_list_segments[i][0])
    deltay.append(waypoint_list_segments[i+1][1]-waypoint_list_segments[i][1])

  for i in range(len(deltax)):
    thetas.append(theta(deltax[i],deltay[i]))

  yaws=[0.0]
  for i in range(len(thetas)):
    if i>0:
      yaws.append(thetas[i]-thetas[i-1])

  yaws.append(0.0)
  return yaws, waypoint_list_segments

def label_moves(yaws,waypoint_list_segments):
  moves=[]
  for yaw in yaws:
    if yaw>forward_classification_boundries[1]:
      moves.append('carla_left_turn_simple')
    elif yaw<forward_classification_boundries[0]:
      moves.append('carla_right_turn_simple')
    else:
      moves.append('carla_overtake')
  moves.pop()

  waypoints_moves=[]
  for i in range(len(waypoint_list_segments)-1):
    start=waypoint_list_segments[i]
    end=waypoint_list_segments[i+1]
    waypoints_moves.append([start,end])


  return moves, waypoints_moves

def concentrate_moves(moves,waypoint_moves):
  assert len(moves)==len(waypoint_moves), "number of moves != number of waypoint intervals"
  returnMoves=[]
  returnWaypoints=[]
  start_ptr=waypoint_moves[0][0]
  prev_move=moves[0]
  n=len(moves)
  for i in range(n):
    if i==0:
      returnMoves.append(prev_move)
    else:
      if moves[i]!=prev_move:
        returnMoves.append(moves[i])
        returnWaypoints.append([start_ptr,waypoint_moves[i-1][1]])
        start_ptr=waypoint_moves[i][0]
        prev_move=moves[i]
  returnWaypoints.append([start_ptr,waypoint_moves[-1][1]])
  


  '''
  for i in range(len(moves)-1):
    if(i<len(moves)):
      print("here ", i) #
      if(moves[i]!=moves[i+1]):
        returnMoves.append(moves[i+1])
        end_ptr=waypoint_moves[i+1][1]
        returnWaypoints.append([start_ptr,end_ptr])
        start_ptr=end_ptr
    else:
      print("here2 ", i) #
      if returnMoves[-1]!=moves[i]:
        returnMoves.append(moves[i])
        end_ptr=waypoint_moves[i][1]
        returnWaypoints.append([start_ptr,end_ptr])

'''


  assert len(returnMoves)==len(returnWaypoints), "num concentrated moves != num concentrated waypoints"
  return returnMoves,returnWaypoints


'''
  Note: by default, num_segments=14.
  Since our waypoints have len = 98, we account for all waypoints
  98%14=0
'''
def waypoint_to_move_segmenter(waypoint_list,num_segments=16):
  yaws, waypoint_list_segments=get_yaws(waypoint_list,num_segments)
  moves, waypoint_moves=label_moves(yaws,waypoint_list_segments)
  return concentrate_moves(moves,waypoint_moves)



def generate_road_waypoints(world, start_location, end_location, max_waypoints=200):
    # Get the map
    carla_map = world.get_map()
    
    # Find nearest waypoints on the road
    start_waypoint = carla_map.get_waypoint(start_location, 
                                            project_to_road=True, 
                                            lane_type=carla.LaneType.Driving)
    end_waypoint = carla_map.get_waypoint(end_location, 
                                          project_to_road=True, 
                                          lane_type=carla.LaneType.Driving)
    
    if not start_waypoint or not end_waypoint:
        raise ValueError("Could not find valid road waypoints for start or end location")
    
    # Collect waypoints by walking through connected waypoints
    current_waypoint = start_waypoint
    road_waypoints = [start_location]
    
    while current_waypoint and current_waypoint != end_waypoint:
        # Find next waypoints
        next_waypoints = current_waypoint.next(1.0)  # 1-meter steps
        
        if not next_waypoints:
            break
        
        # Choose the waypoint closest to the end destination
        next_waypoint = min(next_waypoints, 
                            key=lambda wp: _distance(wp.transform.location, end_location))
        
        road_waypoints.append(next_waypoint.transform.location)
        current_waypoint = next_waypoint
        
        # Prevent infinite loop and limit waypoints
        if len(road_waypoints) >= max_waypoints:
            break
    
    # Ensure end point is included
    if road_waypoints[-1] != end_location:
        road_waypoints.append(end_location)
    
    return road_waypoints

def _distance(loc1, loc2):
    return m.sqrt(
        (loc1.x - loc2.x)**2 + 
        (loc1.y - loc2.y)**2 + 
        (loc1.z - loc2.z)**2
    )


town = 'Town03'

def get_waypoints():
    try:
        client = carla.Client('localhost', 2000)
        world = client.load_world(town)
        world = client.get_world()
        sx,sy=start_coord[0],start_coord[1]
        ex,ey=end_coord[0],end_coord[1]
        start = carla.Location(x=sx, y=sy, z=0)
        end = carla.Location(x=ex, y=ey, z=0)
            
        road_waypoints = generate_road_waypoints(world, start, end)
        waypoints=[]
            
        for wp in road_waypoints:
            waypoints.append([wp.x,wp.y,wp.z])
 
        #chop off first,last value
        waypoints.pop(0)
        waypoints.pop()
        return waypoints

        
        
    except:
        print("error")    
        

def visualize_waypoints(waypoints):
    x = [x[0] for x in waypoints]
    y = [x[1] for x in waypoints]
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.plot(x, y, '-')  # Base line
    for i in range(len(x) - 1):
        if i%20==0:
            mid_x=(x[i]+x[i+1])/2
            mid_y=(y[i]+y[i+1])/2
            dx = x[i+1]-x[i]
            dy = y[i+1]-y[i]
            ax.annotate('', xy=(x[i+1], y[i+1]),xytext=(mid_x,mid_y),arrowprops=dict(arrowstyle='->',color='red',lw=1.5))
    plt.show()        



import subprocess
import time

def run_command_with_timeout(command, timeout=200):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
    
    start_time = time.time()  # Record start time
    try:
        for line in iter(process.stdout.readline, ''):  # Read output live
            print(line, end="")  
            
            # Check if timeout has been reached
            if time.time() - start_time >= timeout:
                print(f"\nStopping after {timeout} seconds.")
                process.terminate()  # Gracefully stop
                break

        process.wait(timeout=5)  # Ensure cleanup
    except subprocess.TimeoutExpired:
        process.kill()  # Force kill if needed
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Error: {stderr_output}")

# Example Usage:
# run_command_with_timeout("./eval_dm3.sh 2000 0 ./logdir/new_four_lane/checkpoint.ckpt --task carla_four_lane --dreamerv3.logdir ./logdir/new_four_lane", timeout=80)



def terminateCarla():
  for proc in psutil.process_iter(["pid", "name"]):
    if "CarlaUE4" in proc.info["name"]:
        print(f"Terminating CARLA process {proc.info['pid']}")
        psutil.Process(proc.info["pid"]).terminate()
  time.sleep(10)

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("Hello! Welcome to our senior design project demonstration!")
start_coord_string = input("Enter a start coordinate [x,y]: ")
start_coord=eval(start_coord_string)
assert len(start_coord)==2, "Incorrect start coordinate length"

end_coord_string = input("Enter an end coordinate [x,y]: ")
end_coord=eval(end_coord_string)
assert len(end_coord)==2, "Incorrect end coordinate length"

print("Generating waypoints...")
waypoints = get_waypoints()
#print(waypoints)
print("Done")
print("\n")
print("Getting moves...\n")
#visualize_waypoints(waypoints=waypoints)
moves,coords = waypoint_to_move_segmenter(waypoints)
print("Moves list: ",moves)
print("Coordinates list: ",coords)
#print(moves)
#print(coords)


import yaml

###
yaml_dir = "/home/eec174/cardreamer/CarDreamer/car_dreamer/configs/tasks.yaml"
###

def write_coord_to_yaml(move, idx):
  with open(yaml_dir, 'r') as yaml_file:
    yaml_data=yaml.load(yaml_file, Loader=yaml.SafeLoader)
  
  match move:
    case 'carla_overtake':
        yaml_data["carla_overtake"]["env"]["lane_start_points"]= coords[idx][0]
        yaml_data["carla_overtake"]["env"]["lane_end_points"]=coords[idx][0]
        print(coords[idx])

    case 'carla_right_turn_simple':
        start_point = coords[idx][0]
        lane_start_point = start_point.append(0)
        print(coords[idx])
        yaml_data["carla_right_turn_simple"]["env"]["world"]["town"]=town
        yaml_data["carla_right_turn_simple"]["env"]["lane_start_point"]=lane_start_point
        yaml_data["carla_right_turn_simple"]["env"]["ego_path"] = coords[idx]
        print(coords[idx])

    case 'carla_left_turn_simple': 
        start_point = coords[idx][0]
        lane_start_point = start_point.append(0)
        yaml_data["carla_left_turn_simple"]["env"]["world"]["town"]=town
        yaml_data["carla_left_turn_simple"]["env"]["lane_start_point"]=lane_start_point
        yaml_data["carla_left_turn_simple"]["env"]["ego_path"] = coords[idx]
        #print(coords[idx])

  with open(yaml_dir,'w') as yaml_file:
      yaml.dump(yaml_data,yaml_file,default_flow_style=False)

time.sleep(5)      
terminateCarla()

index = 0
for idx, move in enumerate(moves):
  #write_coord_to_yaml(move,idx)
  match move:
      case 'carla_overtake':
        ##Change checkpoint location below
        command = f"./eval_dm3.sh 2000 0 ./logdir/new_four_lane/checkpoint.ckpt --task carla_overtake --dreamerv3.logdir ./logdir/new_four_lane{index}"
        

        run_command_with_timeout(command,80)
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
      case 'carla_right_turn_simple':

        ##Change checkpoint location below
        command = f"./eval_dm3.sh 2001 0 ./logdir/new_right_turn_hard/checkpoint.ckpt --task carla_right_turn_simple --dreamerv3.logdir ./logdir/new_right_turn_hard{index}"

        run_command_with_timeout(command,80)
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
      case 'carla_left_turn_simple':


        #Change checkpoint location below
        command = f"./eval_dm3.sh 2002 0 ./logdir/new_left_turn_hard/checkpoint.ckpt --task carla_left_turn_simple --dreamerv3.logdir ./logdir/new_left_turn_hard{index}"


        run_command_with_timeout(command,200)
        #result = subprocess.run(command, shell=True, capture_output=True, text=True) 
      case _:
        print("Done")

  index+=1
  time.sleep(8)
  #pause = input("Press enter to continue") #Pause after each move for analysis