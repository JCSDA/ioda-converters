#!/usr/bin/env python
import argparse
import os
import sys
from multiprocessing import Pool
import glob

import conv
import radiances
import composition
import aod_dicts as aodd
import oz_dicts as od
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

def run_aod_obs(aodfile,outdir):
  print("Processing:"+str(aodfile))
  Diag = composition.AOD(aodfile)
  Diag.read()
  Diag.toIODAobs(outdir)
  return 0

def run_oz_obs(ozfile,outdir):
  print("Processing:"+str(ozfile))
  Diag = composition.Ozone(ozfile)
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

def run_aod_geo(aodfile,outdir):
  print("Processing:"+str(aodfile))
  Diag = composition.AOD(aodfile)
  Diag.read()
  Diag.toGeovals(outdir)
  return 0

def run_oz_geo(ozfile,outdir):
  print("Processing:"+str(ozfile))
  Diag = composition.Ozone(ozfile)
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

obspool = Pool(processes=nprocs)
# process obs files
if MyArgs.obs_dir:
  ObsDir=MyArgs.obs_dir
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
  # atmospheric composition observations
  # aod first
  for radfile in radfiles:
    process = False
    for p in aodd.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_aod_obs,args=(radfile,ObsDir))
  # ozone 
  for radfile in radfiles:
    process = False
    for p in od.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_oz_obs,args=(radfile,ObsDir))

# process geovals files
if MyArgs.geovals_dir:
  GeoDir=MyArgs.geovals_dir
  ### conventional obs first
  # get list of conv diag files
  convfiles = glob.glob(DiagDir+'/*conv*') 
  for convfile in convfiles:
    res = obspool.apply_async(run_conv_geo,args=(convfile,GeoDir))
  ### radiances next
  radfiles = glob.glob(DiagDir+'/diag*')
  for radfile in radfiles:
    process = False
    for p in rd.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_radiances_geo,args=(radfile,GeoDir))
  # atmospheric composition observations
  # aod first
  for radfile in radfiles:
    process = False
    for p in aodd.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_aod_geo,args=(radfile,ObsDir))
  # ozone 
  for radfile in radfiles:
    process = False
    for p in od.sensors:
      if p in radfile:
        process = True
    if process:
      res = obspool.apply_async(run_oz_geo,args=(radfile,ObsDir))

# process all in the same time, because sats with many channels are so slow...
obspool.close()
obspool.join()