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
from numpy import loadtxt, cos, radians, asarray, average
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
    
    # it simply gets spot positions, velocities, channels and fluxes from specified spatial range
    def get_spots_params_from_range(self, ra_min, ra_max, dec_min, dec_max):
        # sometimes ra_max can be smaller, than ra_min
        # in this case, we might want to switch them in places
        # same applies to dec_min and dec_max
        if ra_min > ra_max: # RA
            ra_mintmp = ra_min
            ra_maxtmp = ra_max
            ra_min = ra_maxtmp
            ra_max = ra_mintmp
        
        if dec_min > dec_max:
            dec_mintmp = dec_min
            dec_maxtmp = dec_max
            dec_min = dec_maxtmp
            dec_max = dec_mintmp

        # we need our tmp tables, that will be returned:
        marked_dRA = []
        marked_dRA_err = []
        marked_dDEC = []
        marked_dDEC_err = []
        marked_channel = []
        marked_velocity = []
        marked_fluxes = []
        marked_fluxes_err = []
        
        # we iterate in search of proper spots
        for i in range(len(self.dRA)):
            # proper condition of including this spot:
            if (self.dRA[i] > ra_min and self.dRA[i] < ra_max) and (self.dDEC[i] > dec_min and self.dDEC[i] < dec_max):
                # if condition is fulfilled, we append parameter to the tables
                marked_dRA.append(self.dRA[i])
                marked_dRA_err.append(self.dRA_error[i])
                marked_dDEC.append(self.dDEC[i])
                marked_dDEC_err.append(self.dDEC_error[i])
                marked_channel.append(self.channel[i])
                marked_velocity.append(self.velocity[i])
                marked_fluxes.append(self.flux_density[i])
                marked_fluxes_err.append(self.flux_density_error[i])
        
        return asarray(marked_channel), asarray(marked_velocity), asarray(marked_dRA), asarray(marked_dRA_err), asarray(marked_dDEC), asarray(marked_dDEC_err), asarray(marked_fluxes), asarray(marked_fluxes_err)

    def calculate_cloudet_params(self, velocities, dRA, dRA_err, dDEC, dDEC_err, fluxes, fluxes_err):
        # failsafe, if the dRA, dDEC and fluxes tables are not equal
        if len(dRA) != len(dDEC) or len(dRA) != len(fluxes) or len(dDEC) != len(fluxes):
            return 0.0, 0.0, 0.0
        
        # calculate the mean baricenter of the cloudet
        center_dRA = average(dRA, weights=fluxes)
        center_dDEC = average(dDEC, weights=fluxes)
        center_flux = max(fluxes)
        center_velocity = average(velocities, weights = fluxes)

        # errors
        center_dRA_err = average(dRA_err, weights = fluxes)
        center_dDEC_err = average(dDEC_err, weights = fluxes)
        center_flux_err = fluxes_err[fluxes.tolist().index(center_flux)]


        return center_velocity, center_dRA, center_dRA_err, center_dDEC, center_dDEC_err, center_flux, center_flux_err