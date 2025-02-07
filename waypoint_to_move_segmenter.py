# -*- coding: utf-8 -*-
"""waypoint_to_move_segmenter

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kjpVLp7_LH4rAR7jXlHVMGbQTXSyeVWO
"""

#Complex path segmenter
import math as m


#Global Parameters:
left_classification_boundries=[-90,-15] #Left min angle, max angle
right_classification_boundries=[15,90] #Right min angle, max angle
forward_classification_boundries=[-15,15] #Forward min angle, max angle

num_clusters=10 #Less clusters -> Wider consideration of moves during concentration; More clusters -> Narrower consideration -> Less moves ignored

#Example waypoint list
#waypoint_list=[(0,0,30),(1,1,32),(2,2,35),(3,3,45),(4,4,45),(5,5,20),(6,6,0),(7,7,-20),(8,8,-40),(9,9,-60),(10,10,-40),(11,11,-20),(12,12,-20),(13,13,0),(14,14,20),(15,15,40),(16,16,60),(17,17,80),(18,18,85),(19,19,85),(20,20,-10),(21,21,-110),(22,22,0),(23,23,-180)]


#Note: this might not be exactly how theta is formatted, can be retroactively changed
def get_thetas(waypoint_list):
  n=len(waypoint_list)
  thetas=[]
  thetas.append(0)
  for i in range(n-1):
    thetas.append(waypoint_list[i+1][2]-waypoint_list[i][2])
  return thetas

def distinguish_moves(thetas):
  move_list=[]
  for i in range(len(thetas)):
    if (thetas[i]<left_classification_boundries[1])and(thetas[i]>left_classification_boundries[0]):
      move_list.append('l')
    elif (thetas[i]>right_classification_boundries[0])and(thetas[i]<right_classification_boundries[1]):
      move_list.append('r')
    elif (thetas[i]<=forward_classification_boundries[1])and(thetas[i]>=forward_classification_boundries[0]):
      move_list.append('f')
    else:
      move_list.append('b')
  return move_list


def most_common(input_list,classes):
  classes_count=[0]*len(classes)
  for i in range(len(input_list)):
    if input_list[i] in classes:
      idx=classes.index(input_list[i])
      classes_count[idx]+=1
  return classes[classes_count.index(max(classes_count))]


def concentrate_moves(move_list,num_clusters=10,classes=['f','b','l','r']):
  new_move_list=[]
  coord_list=[]
  cluster_size=len(move_list)/num_clusters
  for i in range(num_clusters):
    if i==num_clusters:
      most_common_move=most_common(move_list[m.ceil(i*cluster_size):],classes)
      new_move_list.append(most_common_move)
      coord_list.append([m.ceil(i*cluster_size),len(move_list)])
    else:
      most_common_move=most_common(move_list[m.ceil(i*cluster_size):m.ceil((i+1)*cluster_size)],classes)
      new_move_list.append(most_common_move)
      coord_list.append([m.ceil(i*cluster_size),m.ceil((i+1)*cluster_size-1)])
  return new_move_list,coord_list

def get_final_move_list(concentrated_move_list,coord_list):
  final_move_list=[]
  final_coord_list=[]
  final_coord_list.append([0,0])
  final_move_list.append(concentrated_move_list[0])
  prevMove=concentrated_move_list[0]
  for i in range(len(concentrated_move_list)):
    if concentrated_move_list[i]==prevMove:
      final_coord_list[-1][1]=coord_list[i][1]
    else:
      final_coord_list.append([coord_list[i][0],coord_list[i][1]])
      final_move_list.append(concentrated_move_list[i])
      prevMove=concentrated_move_list[i]
  return final_move_list,final_coord_list


def waypoint_to_move_segmenter(waypoint_list):
  thetas=get_thetas(waypoint_list)
  final_coord_list=[]
  move_list=distinguish_moves(thetas)
  concentrated_move_list,coord_list=concentrate_moves(move_list,num_clusters)
  final_move_list,final_coord_idx_list=get_final_move_list(concentrated_move_list,coord_list)
  for idx_group in final_coord_idx_list:
    final_coord_list.append([waypoint_list[idx_group[0]],waypoint_list[idx_group[1]]])
  print(final_coord_idx_list)
  return final_move_list,final_coord_list


#final_move_list,final_coord_list=waypoint_to_move_segmenter(waypoint_list)
#print(final_move_list)
#print(final_coord_list)

