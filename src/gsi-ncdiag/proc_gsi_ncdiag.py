#!/usr/bin/env python
import argparse
import os
import sys
from multiprocessing import Pool
import glob

import conv
import radiances
import rad_dicts as rd

def run_conv_obs(convfile,outdir):
  print("Processing:"+str(convfile))
  Diag = conv.Conv(convfile)
  Diag.read()
  Diag.toIODAobs(outdir)
  return 0

def run_radiances_obs(radfile,outdir):
  print("Processing:"+str(radfile))
  Diag = radiances.Radiances(radfile)
  Diag.read()
  Diag.toIODAobs(outdir)
  return 0

def run_conv_geo(convfile,outdir):
  print("Processing:"+str(convfile))
  Diag = conv.Conv(convfile)
  Diag.read()
  Diag.toGeovals(outdir)
  return 0

def run_radiances_geo(radfile,outdir):
  print("Processing:"+str(radfile))
  Diag = radiances.Radiances(radfile)
  Diag.read()
  Diag.toGeovals(outdir)
  return 0

ScriptName = os.path.basename(sys.argv[0])

# Parse command line
ap = argparse.ArgumentParser()
ap.add_argument("-n","--nprocs",help="Number of tasks/processors for multiprocessing")
ap.add_argument("input_dir",help="Path to concatenated GSI diag files")
ap.add_argument("-o","--obs_dir",help="Path to directory to output observations")
ap.add_argument("-g","--geovals_dir",help="Path to directory to output observations")

MyArgs = ap.parse_args()

if MyArgs.nprocs:
  nprocs = int(MyArgs.nprocs)
else:
  nprocs = 1
  
DiagDir = MyArgs.input_dir

# process obs files
if MyArgs.obs_dir:
  ObsDir=MyArgs.obs_dir
  obspool = Pool(processes=nprocs)
  ### conventional obs first
  # get list of conv diag files
  convfiles = glob.glob(DiagDir+'/*conv*') 
  for convfile in convfiles:
    res = obspool.apply_async(run_conv_obs,args=(convfile,ObsDir))
  ### radiances next
  radfiles = glob.glob(DiagDir+'/diag*')
  for radfile in radfiles:
    process = False
    for p in rd.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_radiances_obs,args=(radfile,ObsDir))
  obspool.close()
  obspool.join()

# process geovals files
if MyArgs.geovals_dir:
  GeoDir=MyArgs.geovals_dir
  obspool = Pool(processes=nprocs)
  ### conventional obs first
  # get list of conv diag files
  convfiles = glob.glob(DiagDir+'/*conv*') 
  for convfile in convfiles:
    res = obspool.apply_async(run_conv_geo,args=(convfile,ObsDir))
  ### radiances next
  radfiles = glob.glob(DiagDir+'/diag*')
  for radfile in radfiles:
    process = False
    for p in rd.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_radiances_geo,args=(radfile,ObsDir))
  obspool.close()
  obspool.join()
