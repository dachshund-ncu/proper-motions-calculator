'''
This class creates multiple instances of "maser_spots" and lists them to get direct acces
Class needs a list of files in the argument
List is generated in main file (pm_finder.py)
'''
from spot_class import maser_spots
from datetime import datetime
import os
from os.path import realpath
class multiple_epochs_cl:

    def __init__(self):
        # -- list with "maser_spots" instances
        self.epochs = []



    
    def read_multiple_epochs(self, list_of_files, reload=False, first_time=True, append=False):
        # first_time specifies, if we opened theese files before
        # therefore, if we picked these files from first menu
        # if yes, we need to copy these files and make proper directories
        
        # therefore, we:
        # 1 - find root directory
        self.root_directory, self.projs_path = self.__find_root_directory()
        if first_time == True:
            # 2 - make a new project directory
            now = datetime.now()
            self.project_dirname = now.strftime("%Y-%m-%dT%H:%M:%S")
            os.mkdir(self.projs_path + "/" + self.project_dirname )
            # we make subrirectories as well
            os.mkdir(self.projs_path + "/" + self.project_dirname  + "/" + "shifted")
            os.mkdir(self.projs_path + "/" + self.project_dirname  + "/" + "cloudets")
            os.mkdir(self.projs_path + "/" + self.project_dirname  + "/" + "baricenters")
            os.mkdir(self.projs_path + "/" + self.project_dirname  + "/" + "proper_motions")

            # 3 - copy files to new directory
            for i in range(len(list_of_files)):
                # copying
                tmp = list_of_files[i].split("/")
                flename = tmp[len(tmp)-1]
                os.system("cp " + list_of_files[i] + " " + self.projs_path + "/" + self.project_dirname + "/" + flename)
                # 4. changing list of files
                list_of_files[i] = self.projs_path + "/" + self.project_dirname + "/" + flename

        if append == True:
            # we need to find project_dirname
            tmp = list_of_files[0].split("/")
            self.project_dirname = ""
            for i in range(len(tmp)-1):
                if i == len(tmp)-2:
                    self.project_dirname = self.project_dirname + tmp[i]
                else:
                    self.project_dirname = self.project_dirname + tmp[i] + "/"
            # we modify files list
            for i in range(len(list_of_files)):
                flename = list_of_files[i].split("/")
                flename = flename[len(flename)-1]
                list_of_files[i] = self.project_dirname + "/" + flename
            # we append 
            self.fileslst.extend(list_of_files)

        # iterating in a list_of_files
        # we need to keep list of files
        if reload == False and append == False:
            self.fileslst = list_of_files
        try:
            for i in list_of_files:
                self.epochs.append(maser_spots(i))
        except:
            print("ERROR")
        
        # -- bubble sorting --
        self.epochs = self.__kukle_sort(self.epochs)

        # -- printing message --
        print("----------")
        print("----> Loaded:")
        for i in self.epochs:
            print("----> Date:", i.time_string, "Code:", i.project_code, "PI:", i.project_pi)

    def search_by_proj_code(self, projcode):
        # -- searches for the project with proper project code --
        for i in range(len(self.epochs)):
            if self.epochs[i].project_code == projcode:
                return i
        
        # -- returning -1 if found s**t --
        return -1

    # -- private methoods --
    def __kukle_sort(self, epochs_list):

        # -- main sorting loop --
        for i in range(len(epochs_list) - 1):
            for j in range(0, len(epochs_list) - i - 1):
                if epochs_list[j].mjd > epochs_list[j+1].mjd:
                    epochs_list[j], epochs_list[j+1] = epochs_list[j+1], epochs_list[j]

        return epochs_list

    def __find_root_directory(self):
        # -- path to file --
        scr_directory = realpath(__file__)
        # -- searching for root directory --
        tmp = scr_directory.split("/")
        root_directory = ""
        for i in range(len(tmp)-2):
            root_directory = root_directory + tmp[i] + "/"
        
        # -- path directory --
        projs_path = root_directory + "data"

        return root_directory, projs_path
