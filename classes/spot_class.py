#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Purpose of this class is to hold data about detected maser spots
Input files required columns:

Channel | Velocity (km/s) | FLux Density (Jy/beam) | Flux error | dRA (mas) | dRA error (mas) | dDEC (mas) | dDEC error (mas)

note, that "|" signs should be not present in file. They are listed to help you with understanding what the file structure should be

Additionally, there should be following informations in header:

# ----------------------------
# TIME:         2021-07-18
# BEAM-SIZE:    4.5 x 4.5 (mas)
# ORIGIN:       22:56:17.90 62:01:49.65
# PROJECT_CODE: ED048B
# PI:           Michał Durjasz
# ----------------------------

feel free to copy-paste and fill with your parameters
there is example file in the "examples" directory:
"spots/example_spot_file.dat"
'''

# --- importing important libraries ---
from numpy import loadtxt, cos, radians
from astropy.time import Time

class maser_spots:

    def __init__(self, filename):

        # -- Reading the spots file --
        self.__read_spots_file(filename)

    # -- private --
    def __read_spots_file(self, filename): # __ means it is PRIVATE
        # -- reading the spots file --
        tmp = loadtxt(filename) # not "SELF" 'cause it is not needed afterwards
        self.flnme = filename # saving filename, it will be useful later
        # -- assinging the file structure to proper tables --
        self.channel = tmp[:,0]
        self.velocity = tmp[:,1]
        self.flux_density = tmp[:,2]
        self.flux_density_error = tmp[:,3]
        self.dRA = tmp[:,4]
        self.dRA_error = tmp[:,5]
        self.dDEC = tmp[:,6]
        self.dDEC_error = tmp[:,7]
        # -- reading header --
        tmp2 = open(filename, "r+") # opening in "read mode"
        # - reading lines -
        a = tmp2.readlines()
        # - closing file -
        tmp2.close()
        # - extracting proper informations from file -
        # TIME
        tmp = a[1].split()
        if tmp[1].upper() == "TIME:":
            self.time_string = tmp[2]
        else:
            self.time_string = "00000"
            print("NO TIME INFORMATION IN HEADER")

        # BEAM-SIZE
        tmp = a[2].split()
        if tmp[1].upper() == "BEAM-SIZE:":
            self.beam_size_ra = float(tmp[2])
            self.beam_size_dec = float(tmp[4])
        else:
            self.beam_size_ra = 0.0
            self.beam_size_dec = 0.0
            print("NO BEAM INFORMATION IN HEADER")

        # ORIGIN
        tmp = a[3].split()
        if tmp[1].upper() == "ORIGIN:":
            tmpra = tmp[2].split(":")
            self.RA = float(tmpra[0]) + float(tmpra[1]) / 60.0 + float(tmpra[2]) / 3600.0 # decimal RA
            tmpdec = tmp[3].split(":")
            if float(tmpdec[0]) >= 0.0:
                self.DEC = float(tmpdec[0]) + float(tmpdec[1]) / 60.0 + float(tmpdec[2]) / 3600.0
            else:
                self.DEC = -1.0 * float(tmpdec[0]) + float(tmpdec[1]) / 60.0 + float(tmpdec[2]) / 3600.0
                self.DEC = -1.0 * self.DEC
        else:
            self.RA = 0.0
            self.DEC = 0.0
            print("NO ORIGIN INFORMATION IN HEADER")

        # PROJECT CODE
        tmp = a[4].split()
        if tmp[1].upper() == "PROJECT_CODE:":
            self.project_code = tmp[2]
        else:
            self.project_code = "00000"
            print("NO PROJECT CODE INFORMATION IN HEADER")

        # PI
        tmp = a[5].split()
        if tmp[1].upper() == "PI:":
            self.project_pi = ""
            for wppl in range(2,len(tmp)):
                self.project_pi = self.project_pi + tmp[wppl] + " "
        else:
            self.project_pi = "-----|---"
            print("NO PI INFORMATION IN HEADER")

        # -- Deriving other parameters --
        # time (MJD)
        # astropy time object (will be part of the class)
        self.tee = Time(self.time_string, format="isot", scale="utc")
        # assigning MJD, JD and decimalyear to floats:
        self.decimalyear = self.tee.decimalyear
        self.jd = self.tee.jd
        self.mjd = self.tee.mjd

        # -- reading shifted part --
        projs_dir, raw_flnm = self.__find_root_directory()

        # try to read shifted
        try:
            # opening in "read" mode
            fle = open(projs_dir + 'shifted/' + 'new_origin_of_' + raw_flnm, 'r+')
            a = fle.readlines()
            fle.close()
        except:
            print("----> FOR FILE:", raw_flnm, "No shift information found!")
            return # it will prevent from executing code below
        
        # ---------------------
        # this code will be executed if "except" won't trigger
        # getting shift values
        tmp = a[1].split()
        origin_shift_ra = float(tmp[0])
        origin_shift_dec = float(tmp[1])
        # shifting to shifted epoch
        self.set_as_origin(origin_shift_ra, origin_shift_dec, save=False)
        # ----------------------

    # -- setting the 0,0 point --
    def set_as_origin(self, spot_ra, spot_dec, save=True):
        # assigning old spots to other tables
        self.dRA_noshift = self.dRA
        self.dDEC_noshift = self.dDEC
        # shifting the spots
        self.dRA = self.dRA - spot_ra
        self.dDEC = self.dDEC - spot_dec
        # shifting the origin
        # DEC is easy - we just need to convert spot_dec from mas to degrees
        # first, we do a backup of the old DEC
        self.DEC_noshift = self.DEC
        # then we shift
        self.DEC = self.DEC - (spot_dec / 3600.0 / 1000.0)
        # RA is harder:
        # mas of the RA axis is compensated for DEC (* cos(DEC) )
        # RA is in hrs, spot_ra is in mas
        # mas is RA [degrees] / 3600 / 1000
        # mas is also compensated for 1 / cos(dec)
        # so we need to do:
        # backup
        self.RA_noshift = self.RA
        spot_ra_to_shift = spot_ra / 3600 / 1000  # mas -> degrees
        spot_ra_to_shift = spot_ra_to_shift / 15.0 # degrees -> hourangle
        spot_ra_to_shift = spot_ra_to_shift * ( 1.0 / cos(radians(self.DEC) ) ) # hourangle, de-compensated for DEC
        self.RA = self.RA - spot_ra_to_shift
        
        # -- saving new origin --
        if save:
            self.__save_new_origin(spot_ra, spot_dec)

        # -- setting the bool --
        self.shifted_bool = True

    def unset_as_origin(self):
        # checking, if 'shifted' bool is True or false:
        if self.shifted_bool:
            self.dRA = self.dRA_noshift
            self.dDEC = self.dDEC_noshift
            self.RA = self.RA_noshift
            self.DEC = self.DEC_noshift
        else:
            # it does nothing fi there was no shift yet
            pass
    
    def __find_root_directory(self):
        # -- searching for root directory --
        tmp = self.flnme.split("/")
        root_directory = ""
        for i in range(len(tmp)-1):
            root_directory = root_directory + tmp[i] + "/"
        
        return root_directory, tmp[len(tmp)-1]

    def __save_new_origin(self, spot_ra, spot_dec):
        # we need to find the root directory at the beginning
        # so...
        projs_dir, raw_flnm = self.__find_root_directory()
        # we create new file, called "new_origin_of" + spots_filename
        try:
            # opening file (w+ stands for write mode) - if such file exists, it will be overwritten
            fle = open(projs_dir + 'shifted/' + 'new_origin_of_' + raw_flnm, 'w+')
            # writing header
            fle.write("# origin_dRA (mas)   origin_dDEC (mas)\n")
            # writing informations about origin
            fle.write('%f   %f' % (spot_ra, spot_dec))
            # closing the file
            fle.close()
        except:
            print("Failed to open file: ", projs_dir + 'shifted/' + 'new_origin_of_' + raw_flnm)