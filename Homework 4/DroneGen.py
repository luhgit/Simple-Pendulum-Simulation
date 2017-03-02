#!/usr/bin/python
from scipy import *
import numpy as np
import threading, Queue
import time, random
import names

# Specifying the requirements of drone delivery system
parcels = 200               # No. of Parcels need to be delivered
drone_population = 20       # No. of Drones available for Delivery
drone_capacity = 5.0        # Drone weight carrying capacity (KG)
radius = 35.0               # Delivery Radius in (KM)


exitFlag = 0       

class DroneGenerator(threading.Thread):
    def __init__(self, droneID, name, taskQ):
        threading.Thread.__init__(self)
        self.droneID = droneID
        self.name = name
        self.taskQ = taskQ
        self.speed = 5

    def run(self):
        print('Starting Drone with ID: ' + self.name + '\n')
        self.deliver(self.name, self.taskQ)
        print('Stopping Drone with ID:' + self.name + '\n')

    def deliver(self, droneName, task_queue):
        while not exitFlag:
            time_needed = 1
            queueLock.acquire()
            if not workQueue.empty():
                task = task_queue.get()
                weight = task[1]
                distance = task[2]
                time_needed = distance/self.speed
                queueLock.release()
                print('{} is delivering the parcel {} from {} to {} having weight {} KG and distance {} KM from Delivery Terminal. \n').format(droneName, task[0], task[3], task[4], str(weight), str(distance))
            else:
                queueLock.release()
            time.sleep(time_needed)

# Generates the Drone population
def createDrones(population):
    for i in range(population):
        droneList.append('Drone-' + str(i+1))

# Generates the Random Tasks which represent each Parcel with Parcel ID, Weight, Distance
def genTaskList():
    for id, packet in enumerate(range(parcels)):
        size = np.random.uniform(0.5, drone_capacity)                           # Random weight between 0.5 KG and 5 KG (drone capacity)
        dist = np.random.uniform(0.5, radius)                                   # Random distance between 0.5 KM and 35 KM (Delievery Radius)
        sender = names.get_full_name()                                          # Generates the Random name for Sender
        receiver = names.get_full_name()                                        # Generates the Random name for Reciever
        taskList.append(['Parcel-'+str(id), round(size, 3), round(dist, 2), sender, receiver])    # Appends each task in the Task Queue with ParcelID, Weight & Delivery Distance


if __name__ == '__main__':
    droneList = []                                                      # List of available drones
    taskList = []                                                       # List of Tasks
    queueLock = threading.Lock()                                        # Acquiring Thread Lock
    workQueue = Queue.Queue(parcels)                                    # Creating a Queue to store Tasks
    drones = []
    droneID = 1

    createDrones(drone_population)                                      # Generating 20 Drones
    genTaskList()                                                       # Generating the 500 random parcels (Tasks)


    print('\nStarting simulation of Delivery Drones...\n')
    time.sleep(2)
    print('Fetching list of Tasks (Parcels)...\n')
    time.sleep(2)
    print('Task Queue acquired with a total of {} Tasks.\n').format(len(taskList))
    time.sleep(2)
    print('Fetching the available Drones List...\n')
    time.sleep(2)
    print('Drones List is acquired with a total of {} drones.\n').format(len(droneList))
    time.sleep(2)
    print('Starting Delivery Process...\n')
    time.sleep(2)

    # Create new drones
    for droneName in droneList:
        drone = DroneGenerator(droneID, droneName, workQueue)
        drone.start()
        drones.append(drone)
        droneID += 1

    # Fill the queue
    queueLock.acquire()
    for task in taskList:
        workQueue.put(task)
    queueLock.release()


    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all the threads to complete
    for drone in drones:
        drone.join()

    print('All {} Parcels Successfully Delivered and All {} drones are available again!!').format(len(taskList), len(droneList))
