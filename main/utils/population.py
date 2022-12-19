
from main.utils.network import Network

class Population:
    
    def __init__(self,input_size:int, output_size:int, layer_structure:list=[],discretize:int=1,evolution_step:float=0.01,population_size:int=100):
        """
        Args:
            input_size (int): see Network
            output_size (int):see Network
            layer_structure (list, optional): see Network. Defaults to [].
            descretize (int, optional): see Network. Defaults to 1.
            evolution_step (float, optional): mutation size for each generation. Defaults to 0.01.
            population_size (int, optional): number of networks in the population. Defaults to 100.
        """
        self.individuals = [[Network.zeros(input_size,output_size,layer_structure,discretize),0] for i in range(population_size)]
        self.step = evolution_step
    
    def reward(self,individual:int,reward:float)->None:
        """increase score

        Args:
            individual (int): _description_
            reward (float): _description_
        """
        self.individuals[individual][1]+=reward
    
    def sort(self)->None:
        self.individuals.sort(key = lambda x:-x[1])
    
    def filter(self,best_pourcentage:float=0.10,target="")->None:
        """keep best_pourcentage best and fill the rest with children of the bests

        Args:
            best_pourcentage (float, optional): what percentage of the population shall we keep. Defaults to 0.10.
            target (str, optional): passed to split. See Network.split documentation. Defaults to "".
        """
        self.sort()
        to_keep = max(1,min(len(self.individuals),int(best_pourcentage*len(self.individuals))))
        new_pop = [[self.individuals[i][0],0] for i in range(to_keep)]
        for i in range(len(self.individuals)-to_keep):
            to_clone:Network = self.individuals[i%to_keep][0]
            new_pop.append([to_clone.split(self.step,target),0])
        self.individuals = new_pop
    
    def avg_score(self)->float:
        return sum([score for _,score in self.individuals])/len(self.individuals)
    
    def network(self,index:int)->Network:
        return self.individuals[index][0]
    
    def score(self,index:int)->float:
        return self.individuals[index][1]