from data_logger import DataLogger
from data_reader import *
from genetic_algorithm import *

pop_size = 100
gen = 100
Px = 0.7
Pm = 0.01
Tour = 5


for i in range(12, 21, 2):
    reader = DataReader()
    n, flow_matrix, distance_matrix = reader.read_data("data/had%s.dat" % str(i))
    for j in range(0, 20):
        logger = DataLogger('had%s' % str(i))
        logger.write_header()
        genetic_algorithm = GeneticAlgorithm(n, pop_size, flow_matrix, distance_matrix, Pm, Px, Tour, logger, )
        print('Had%s file best result: %s' % (i, genetic_algorithm.run(gen)))
        logger.close()



