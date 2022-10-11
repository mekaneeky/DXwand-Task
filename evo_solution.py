import numpy as np
from tqdm import tqdm
from random import choice, randint, sample
from copy import deepcopy

def _mutate_one_val(gene):
    new_gene = deepcopy(gene)
    idx_to_mutate = randint(0,len(gene)-1)
    new_gene[idx_to_mutate] = randint(0,ARR_LEN)
    return new_gene

def _mutate_whole_arr(gene):
    return np.random.randint(0,ARR_LEN, size=(len(gene)))

def mutate_arr(gene):
    mutator = choice([_mutate_one_val, _mutate_whole_arr])
    new_gene = mutator(gene)
    return new_gene

def fitness_func(gene, arr):

    idx_left = gene[0]#[0]
    idx_right = gene[1]#[0]
    if idx_left >= idx_right: # assert that left_idx is smaller than right_idx
        return 9999 

    if idx_left < 1:
        return 9999

    if abs(idx_left-idx_right) < 2:
        return 9999

    if len(arr)-idx_right < 2:
        return 9999

    if len(arr[:idx_left]) == 0 or len(arr[idx_left:idx_right]) ==0 or len(arr[idx_right:]) ==0:
        return 9999 
   
    if sum(arr[:idx_left]) == sum(arr[idx_right:]) and  sum(arr[idx_right:]) == sum(arr[idx_left:idx_right]):
        return 0

    return 9999

## Recycled code from my https://github.com/mekaneeky/Simple-AutoML-Zero project
## Yes, I am aware of my username xD
def run_tournament(contestants):
    min_fitness = float("inf")
    for idx in range(len(contestants)):
        if contestants[idx][0] < min_fitness:
            min_fitness = contestants[idx][0]
            min_idx = idx
    tournament_winner = contestants[min_idx]
    return tournament_winner
## Recycled code from my https://github.com/mekaneeky/Simple-AutoML-Zero project
def run_evolution(arr, iters = 100000,fitness_func = fitness_func, population = None, tournament_size = 10):
    
    for i in tqdm(range(iters)):   
        
        min_fitness = float("inf")        
        if i%10 == 0:
            for fitness, gene in population:
                if min_fitness > fitness:
                    min_fitness, min_gene = fitness, gene
            print("BEST FITNESS TO DATE: {}".format(min_fitness))
            print("BEST GENE TO DATE: {}".format(min_gene))

        #TODO use arrays not lists they are faster
        contestants = sample(population, tournament_size)
        
        _, winner_gene = run_tournament(contestants)
        new_gene = mutate_arr(winner_gene)
        fitness = fitness_func(new_gene, arr)
        if fitness == 0:
            print("BEST FITNESS TO DATE: {}".format(fitness))
            print("BEST GENE TO DATE: {}".format(new_gene))
            return new_gene
        population.append(( fitness, new_gene) )
        population.pop(0)        

    min_fitness = float("inf")        
    for fitness, gene in population:
        if min_fitness > fitness:
            min_fitness, min_gene = fitness, gene
    print("BEST FITNESS TO DATE: {}".format(min_fitness))
    print("BEST GENE TO DATE: {}".format(min_gene))

    return min_gene

def initialize_population(arr = None, population_count = 10, gene_len = 2):
    
    population = []
    for _ in range(population_count):
        gene = np.random.randint(0,len(arr), size=(gene_len))
        fitness = fitness_func(gene,arr)
        population.append((fitness, gene))
    return population

def evolutionary_cumulative_arr(arr = None, population_count = 10, gene_len = 2, iters =100):
    init_population = initialize_population(arr = arr)
    best_gene = run_evolution(arr = arr, population= init_population, iters = iters)
    return best_gene

if __name__ == "__main__":
    ex_arr = [ 2, 2 ,0,0,0, 4, 0, 4]
    ARR_LEN = len(ex_arr)
    best_gene = evolutionary_cumulative_arr(arr = ex_arr)
    idx1 = best_gene[0]
    idx2 = best_gene[1]
    print("idx1: " + str(idx1) )
    print("idx2: " + str(idx2) )
    print("sub_arr_1: " + str(ex_arr[:idx1]) )
    print("sub_arr_2: " + str(ex_arr[idx1:idx2]) )
    print("sub_arr_3: " + str(ex_arr[idx2:]) )