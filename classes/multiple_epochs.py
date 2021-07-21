'''
This class creates multiple instances of "maser_spots" and lists them to get direct acces
Class needs a list of files in the argument
List is generated in main file (pm_finder.py)
'''
from spot_class import maser_spots

class multiple_epochs_cl:

    def __init__(self):
        # -- list with "maser_spots" instances
        self.epochs = []



    
    def read_multiple_epochs(self, list_of_files, reload=False):
        # iterating in a list_of_files
        # we need to keep list of files
        if reload == False:
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

    
