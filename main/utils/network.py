
import numpy as np

from main.utils.progress_bar import ProgressIterator
from main.utils.memory import Memory
from main.utils.style import Style



class Layer:
    
    def __init__(self,input_size:int,output_size:int):
        self.input_size=input_size
        self.output_size=output_size
        
        self.matrix = np.zeros((output_size,input_size))
        self.bias = np.zeros(output_size)
    
    def __call__(self,input):
        input = np.array(input,dtype=float)
        return Layer.sigmoid(np.dot(self.matrix,input)+self.bias)

    def __getitem__(self,i):
        if i=="matrix":
            return self.matrix
        if i=="bias":
            return self.bias
        if type(i)==tuple:
            j,k=i
            return self.matrix[j,k]
        if type(i)==int:
            return self.bias[i]
        raise NameError(f"name {i} is not defined")
    
    def __setitem__(self,i,value):
        if i=="matrix":
            value = np.array(value,dtype=float,copy=True)
            if value.shape != self.matrix.shape:
                value=np.transpose(value)
            if value.shape != self.matrix.shape:
                raise ValueError(f"Shapes {value.shape} (your input) and {self.matrix.shape} (layer shape) don't match")
            self.matrix=value
            return
        if i=="bias":
            value = np.array(value,dtype=float,copy=True)
            if value.shape != self.bias.shape:
                raise ValueError(f"Shapes {value.shape} (your input) and {self.bias.shape} (layer shape) don't match")
            self.bias = value
            return
        if type(i)==tuple:
            j,k=i
            self.matrix[j,k]=float(value)
            return
        if type(i)==int:
            self.bias[i] = float(value)
            return
        raise NameError(f"name {i} is not defined")
    
    def __str__(self)->str:
        return f"<Layer ({self.input_size}-->{self.output_size})>"
    
    def copy(self):
        out = Layer(self.input_size,self.output_size)
        out["matrix"] = self["matrix"] #copy already included here
        out["bias"] = self["bias"]
        
        return out
    
    @staticmethod
    def sigmoid(x):
        return 1/(1+np.exp(x))
    
    @staticmethod
    def random(input_size:int,output_size:int):
        layer = Layer(input_size,output_size)
        layer["matrix"]=np.random.rand(output_size,input_size)
        layer["bias"]=np.random.rand(output_size)
        return layer

    @staticmethod
    def values(value:float,input_size:int,output_size:int):
        layer = Layer(input_size,output_size)
        layer["matrix"]=np.full((output_size,input_size),value)
        layer["bias"]=np.full(output_size,value)
        return layer

class Network:
    def __init__(self,input_size:int,output_size:int,discretize_output:int=1):
        """_summary_

        Args:
            input_size (int): size of list/array/iterable in input
            output_size (int): size of output
            discretize_output (int, optional): If discret = n, then output will be only numbers between 0 and n-1. discret = 0 means no discretization =>. Defaults to 1.
        """
        self.input_size = input_size
        self.output_size = output_size
        self.layers=[]
        self.discret=discretize_output
    
    def __str__(self)->str:
        return f"<Network ({self.input_size}-->{self.output_size}) : [ {' , '.join([str(layer) for layer in self.layers])} ]>"
    
    def add(self,layer:Layer)->None:
        """adds a layer to the network

        Args:
            layer (Layer): should match the output of precedent layer
        """
        self.layers.append(layer)
    
    def is_empty(self)->bool:
        return len(self.layers)==0
    
    def get_layers(self)->list:
        return self.layers

    def compile(self)->None:
        """check if all the layers are compatible

        Raises:
            ValueError: if layer input and output don't match
        """
        if self.is_empty():
            return 
        
        in_size = self.input_size
        
        for i,layer in enumerate(self.layers):
            if layer.input_size != in_size:
                if i==0:
                    raise ValueError(f"Shape of layer {i} input ({layer.input_size}) doesn't match with network input size ({in_size})")
                else:
                    raise ValueError(f"Size of layer {i} input ({layer.input_size}) doesn't match with precedent layer output size ({in_size})")
            in_size = layer.output_size
            
        last_layer = self.layers[-1]
        if last_layer.output_size != self.output_size:
            raise ValueError(f"Size of last layer output ({layer.output_size}) doesn't match with network output size ({self.output_size})")
    
    def __call__(self,input):
        input = np.array(input,dtype=float)
        
        if self.is_empty():
            return self.parse_output(input)
        
        for layer in self.layers:
            input = layer(input)
        
        return self.parse_output(input)
    
    def parse_output(self,output:np.ndarray)->np.ndarray:
        """discretise output if necessary. Used within the class, you don't have to use it

        Args:
            input (array)

        Returns:
            array
        """
        
        if self.output_size==1:
            output = output[0]
            
        if self.discret<=0:
            return output
        
        return np.around(output*self.discret)
    
    def __iter__(self):
        return self.layers.__iter__()
    
    def copy(self):
        out = Network(self.input_size,self.output_size)
        for layer in self:
            out.add(layer.copy())
        out.compile()
        return out
    
    def split(self,mutation:float,target:str=""):
        """Creates a child of the network by making a copy of it and creating random mutations

        Args:
            mutation (float): size of the mutation (random float between -mutation and +mutation will be added to weight)
            target (str, optional): 'matrix' -> mutation to 1 element of each matrix of the layers / 'bias' -> same with bias / '' -> mutation to all the elements of the matrices. Defaults to "".

        Returns:
            Network: child
        """
        
        if target=="":
            child = self.copy()
            
            for layer in child.layers:
                layer["matrix"]+=(np.random.rand(*layer["matrix"].shape)-0.5)*mutation*2
                layer["bias"]+=(np.random.rand(*layer["bias"].shape)-0.5)*mutation*2
                
            return child
        
        if target=="matrix":
            child = self.copy()
            
            for layer in child.layers:
                i,j = layer["matrix"].shape
                i = np.random.randint(i)
                j = np.random.randint(j)
                
                layer[i,j]+=(np.random.rand()-0.5)*mutation       
            return child
        
        if target=="bias":
            child = self.copy()
            
            for layer in child.layers:
                i = self.output_size
                i = np.random.randint(i)                
                layer[i]+=(np.random.rand()-0.5)*mutation       
            return child
        return self.copy()
    
    @staticmethod
    def random(input_size:int,output_size:int,layer_sizes:list,discretize:int=1):
        """creates random network with given structure

        Args for exemple:
            input_size (int): 10
            output_size (int): 2
            layer_sizes (list): [5,3]

        Returns:
            Network: Layer(10-->5) Layer(5-->3) Layer(3-->2)
        """
        network = Network(input_size,output_size,discretize)
        in_size = input_size
        
        for size in layer_sizes:
            out_size = size
            network.add(Layer.random(in_size,out_size))
            in_size=size
        network.add(Layer.random(in_size,output_size))
        
        network.compile()
        return network

    @staticmethod
    def values(value:float,input_size:int,output_size:int,layer_sizes:list,discretize:int=1):
        """creates network with given structure, filled with unique value

        Args for exemple:
            input_size (int): 10
            output_size (int): 2
            layer_sizes (list): [5,3]

        Returns:
            Network: Layer(10-->5) Layer(5-->3) Layer(3-->2)
        """
        network = Network(input_size,output_size,discretize)
        in_size = input_size
        
        for size in layer_sizes:
            out_size = size
            network.add(Layer.values(value,in_size,out_size))
            in_size=size
        network.add(Layer.values(value,in_size,output_size))
        
        network.compile()
        return network
    
    @staticmethod
    def zeros(input_size:int,output_size:int,layer_sizes:list,discretize:int=1):
        """creates network with given structure, filled with zeros

        Args for exemple:
            input_size (int): 10
            output_size (int): 2
            layer_sizes (list): [5,3]

        Returns:
            Network: Layer(10-->5) Layer(5-->3) Layer(3-->2)
        """
        return Network.values(0,input_size,output_size,layer_sizes,discretize)
    