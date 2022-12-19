import sys
from functools import wraps
from main.utils.style import ANSI

#à transformer en environnement ?

class Jammer:
    """remplace sys.stdout\n
    self.print() et __str__ sont à disposition pour réccupérer le contenu intercepté
    """

    def __init__(self):
        self.stuff=""
        self.memory=""
        self.sys_stdout = sys.stdout
        self.flush= lambda :0
        self.is_active=False
        self.record_only=False
    
    def write(self,stuff)->None:
        self.stuff+=str(stuff)
        self.memory+=str(stuff)
        if (self.record_only):
            self.print()
    
    def print(self)->None:
        """print le contenu intercepté par le jammer depuis le dernier print
        """
        tmp = self.stuff
        self.stuff=""
        if (self.is_active):
            self.deactivate()
            print(tmp,end="")
            self.activate()
        else:
            print(tmp,end="")
        
    
    def __str__(self)->str:
        """
        Returns:
            str: contenu intercepté
        """
        return self.memory
    
    def __repr__(self)->str:
        return str(self).__repr__()
    
    def activate(self):
        """Starts the jammer, everything printed will be hidden and remembered by the jammer
        """
        self.is_active=True
        sys.stdout = self    
    
    def deactivate(self):
        """Frees the print function
        """
        self.is_active=False
        sys.stdout = self.sys_stdout
    
    def get_memory_size(self)->int:
        """Counts number of lines in jammer memory

        Returns:
            int: number of "\ n" caracters in memory
        """
        return self.memory.count("\n")
    
    def reset(self):
        """Erase memory
        """
        self.memory=""
        self.stuff=""
    
    def erase(self,add_one=False):
        """Erase everything the jammer memory has printed

        Args:
            add_one (bool, optional): Should we erase one more line, if 'print' has been used on jammer memory ("\ n" automatically added). Defaults to False.
        """
        lines = self.get_memory_size()
        if add_one:
            lines+=1
        if self.is_active:
            self.deactivate()
            for i in range(lines):
                print(ANSI.go_up_n_left+"\n"+ANSI.go_up_n_left,end="")#je monte, newline pour effacer, puis je remonte
            self.activate()
        else:
            for i in range(lines):
                print(ANSI.go_up_n_left+ANSI.erase_line,end="")#je monte, newline pour effacer, puis je remonte
    

JAMMER = Jammer()
    
    