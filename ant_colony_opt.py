from genes import run, initialize
from random import randint as rng
from rotat import *
from path import *


def generate_neigh(gene, n_amount):
    k = [-1,1]
    r = []
    for _ in range(n_amount):
        new_gene = gene[:]
        for y in range(0, len(new_gene)):
            if y % 3 != 2:
                new_gene[y] += k[rng(0,1)]
        r.append(new_gene)
    return r

def unique_append(lista, items):
    for item in items:
        if item not in lista:
            lista.append(item)
    return lista
def except_item(lista: list, item):
    try:
        lista.remove(item)
    except:
        pass
    return lista

def get_fitness(roads, cars, sems):
    run(roads, cars, sems)
    s = 0
    for x in cars:
        x: Car
        s += x.wait_time
    s = (1/(s+1)) * 10000000
    return s

def generate_ant_colony(gene, _rounds, neigh_amount, cars_amount):
    genes = [gene]
    genes_connections = [set()]
    current_round = [gene]

    i = 0
    for x in range(_rounds):
        next_round = []
        for gene in current_round:
            others = generate_neigh(gene, neigh_amount)

            for other in others:
                if other not in genes:
                    genes_connections.append(set([i]))
                else:
                    genes_connections[genes.index(other)].add(i)
            genes = unique_append(genes, others)
            for z in others:
                genes_connections[i].add(genes.index(z))
            next_round = except_item(unique_append(next_round, others), gene)
            i += 1
        current_round = next_round

    k = len(genes) - len(genes_connections)
    if k > 0:
        genes_connections += [[]]*k


    fit = []
    for gene in genes:
        # fit.append(rng(1,4))
        cars,roads,sems = initialize(roads_info, matrix, gene, cars_amount)
        fit.append(get_fitness(cars=cars,roads=roads,sems=sems))

    adj_matrix = []
    fero_matrix = []
    for y in range(len(genes)):
        adj_matrix.append([None]*len(genes))
        fero_matrix.append([0]*len(genes))
        for x in genes_connections[y]:
            # adj_matrix[y][x] = (float(str((fit[x] - fit[y])/10000000)[:5]))
            adj_matrix[y][x] = fit[x] - fit[y]
            fero_matrix[y][x] = 0


    return genes, genes_connections, adj_matrix, fero_matrix

def choose(values, target):
    i = 0
    choosen = values[i]
    while(target > choosen and i < len(values)):
        target -= values[i]
        i += 1
        choosen = values[i]
    # print(f" ${values}/{target}/{i}")
    return i

def ant_colony(gene, _rounds, neigh_amount, cars_amount, ants_amount, ants_max_step, iterations):
    genes, genes_connections, adj_matrix, fero_matrix = generate_ant_colony(gene, _rounds, neigh_amount, cars_amount)
    # print(len(genes))
    # for x in adj_matrix:
    #     print(x)
    # print()
    
    after_evaporation = 0.9
    _alfa = 4
    _beta = 7

    for x in range(iterations):
        ants = [0 for x in range(ants_amount)]
        i = 0
        while i < ants_max_step:
            # print("Step",i)
            z = 0
            for ant in ants:
                # print(f" <Ant[{z+1}]: {ants[z]}>")
                options = list(genes_connections[ant])
                values = []
                soma = 0
                _from = ant
                for r in range(len(options)):
                    _to = options[r]
                    fero = fero_matrix[_from][_to]
                    fitness = adj_matrix[_from][_to]
                    # print(f"  Option<{_from}->{_to}>: Fero {fero} and Fit {fitness}")
                    v = fero**_alfa * fitness**_beta
                    if v <= 0:
                        v = 1
                    soma += v
                    values.append(v)

                chosen = options[choose(values, rng(0,int(soma)))]
                # print(f" {chosen} from {values}")
                fero_matrix[_from][chosen] += 1
                ants[z] = chosen
                z += 1
            i += 1

    ants = [0]
    i = 0
    while i < ants_max_step:
        z = 0
        for ant in ants:
            options = list(genes_connections[ant])
            values = []
            soma = 0
            _from = ant
            for r in range(len(options)):
                _to = options[r]
                fero = fero_matrix[_from][_to]
                fitness = adj_matrix[_from][_to]
                v = fero**_alfa * fitness**_beta
                if v <= 0:
                    v = 1
                soma += v
                values.append(v)

            chosen = options[choose(values, rng(0,int(soma)))]
            fero_matrix[_from][chosen] += 1
            ants[z] = chosen
            z += 1
        i += 1

    for y in range(len(fero_matrix)):
        for x in range(len(fero_matrix[y])):
            fero_matrix[y][x] *= after_evaporation

    return genes[ants[0]]

    # for x in adj_matrix:
    #     print("[",end=' ')
    #     [print(int(y) if y != None else ".", end=' ') for y in x]
    #     print("]")
    # print()

    # for x in fero_matrix:
    #     print("[",end=' ')
    #     [print(int(y), end=' ') for y in x]
    #     print("]")

def ant_optimization(gene, cars_amount):
    _rounds = 4
    neigh_amount = 5

    ants_amount = 10
    ants_max_step = 20
    iterations = 10
    best_gene = ant_colony(gene, _rounds, neigh_amount, cars_amount, ants_amount, ants_max_step, iterations)
    return best_gene


# gene = [rng(6,60) if x != 3 else rng(0,1) for x in range(num_sem * 3)]
# better_gene = ant_optimization(gene, 10)
# print(better_gene)