from multistage_algorithm import Multistage
from basket_parser import parse_csv
from linear_hash_functions import f_5_13, f_3_7


multistage = Multistage(50, parse_csv('transactions.csv'), f_5_13, f_3_7, 4000)
result = multistage.run()
print('Number of singletons:')
print(multistage.number_of_singletons())
print('Number of baskets:')
print(multistage.number_of_baskets())
print('Frequent singletons:')
print(result[0])
print('Frequent doubletons:')
print(result[1])
