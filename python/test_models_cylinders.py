#!/usr/bin/env python
'''Generates mesh files and point clouds for randomly generated rectangular blocks.'''

# python
import time
# scipy
from scipy.io import savemat
from numpy import array, mean
# self
import point_cloud
from rl_agent import RlAgent
from rl_environment import RlEnvironment

def main():
  '''Entrypoint to the program.'''

  # PARAMETERS =====================================================================================

  # system
  gpuId = 0

  # objects
  objectHeight = [0.007, 0.013]
  objectRadius = [0.030, 0.045]
  nObjects = 1000

  # view
  viewCenter = array([0,0,0])
  viewKeepout = 0.60
  viewWorkspace = [(-1.0,1.0),(-1.0,1.0),(-1.0,1.0)]

  # visualization/saving
  showViewer = False
  showSteps = False
  plotImages = False

  # INITIALIZATION =================================================================================

  rlEnv = RlEnvironment(showViewer, removeTable=True)
  rlAgent = RlAgent(rlEnv, gpuId)

  # RUN TEST =======================================================================================

  for objIdx in xrange(nObjects):

    obj = rlEnv.PlaceCylinderAtOrigin(objectHeight, objectRadius, "cylinder-{}".format(objIdx), True)
    cloud, normals = rlAgent.GetFullCloudAndNormals(viewCenter, viewKeepout, viewWorkspace)
    point_cloud.SaveMat("cylinder-{}.mat".format(objIdx), cloud, normals)

    rlAgent.PlotCloud(cloud)
    if plotImages:
      point_cloud.Plot(cloud, normals, 2)

    if showSteps:
      raw_input("Placed cylinder-{}.".format(objIdx))

    rlEnv.RemoveObjectSet([obj])

if __name__ == "__main__":
  main()
  exit()