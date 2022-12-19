import os
import shutil
import pickle

class Memory:
    
    def __init__(self,dir_path:str="memory"):
        """initializes memory in the path you defined (carefull, on reset the path is deleted)

        Args:
            dir_path (str, optional): directories will be created recursivly using this path. Defaults to "memory".
        """
        self.dir_path = dir_path
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path,exist_ok=True)
    
    def reset(self)->None:
        """removes folder containing the memory"""
        shutil.rmtree(self.dir_path)
    
    def parse(self,file_name:str)->str:
        """Returns path_to_directory + "/" + file_name + ".shadok", ie the location of the variable

        Args:
            file_name (str): variable name

        Returns:
            str: location of variable .shadok file
        """
        return self.dir_path+"/"+file_name+".shadok"
    
    def save(self,var,var_name:str)->None:
        """Save var (as bytes) in the memory folder under the given name (extension .shadok)

        Args:
            var (Any): variable you want to save
            var_name (str): how you want to name it (usually same name as the variable)
        """
        
        with open(self.parse(var_name),"wb") as file: #write bytes
            pickle.dump(var, file)
        return
    
    def load(self,var_name:str):
        """Returns the variable you saved

        Args:
            var_name (str): name of the .shadok file

        Returns:
            Any
        """
        with open(self.parse(var_name),"rb") as file:
            tmp = pickle.load(file)
        return tmp
