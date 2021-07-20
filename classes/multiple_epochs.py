'''
This class creates multiple instances of "maser_spots" and lists them to get direct acces
Class needs a list of files in the argument
List is generated in main file (pm_finder.py)
'''
from spot_class import maser_spots

class multiple_epochs_cl:

    def __init__(self, list_of_files):
        # -- list with "maser_spots" instances
        self.epochs = []

        # -- loading --
        self.__read_multiple_epochs(list_of_files)

        # -- bubble sorting --
        self.__kukle_sort()

    # -- private methoods --
    def __read_multiple_epochs(self, list_of_files):
        # iterating in a list_of_files 
        try:
            for i in list_of_files:
                self.epochs.append(maser_spots(i))
        except:
            print("ERROR")
    
    def __kukle_sort(self):
        # -- temporary table, that will be holding sorted classes --
        # -- we DO NOT want to change orginal "epochs" table until it is done --
        epochs_sorted = self.epochs

        # -- main sorting loop --
        for i in range(len(epochs_sorted) - 1):
            for j in range(0, len(epochs_sorted) - i - 1):
                if epochs_sorted[j].mjd > epochs_sorted[j+1].mjd:
                    epochs_sorted[j], epochs_sorted[j+1] = epochs_sorted[j+1], epochs_sorted[j]

        self.epochs = epochs_sorted
    
    def search_by_proj_code(self, projcode):
        # -- searches for the project with proper project code --
        for i in range(len(self.epochs)):
            if self.epochs[i].project_code == projcode:
                return i
        
        # -- returning -1 if found s**t --
        return -1