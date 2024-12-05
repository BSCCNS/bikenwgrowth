import sys
from pathlib import Path

#sys.path.append(str(Path(__file__).resolve().parents[2]))

#-------------------------------------------------------#
from ..scripts import path
import itertools
from ..scripts.initialize import cities


debug = False
PATH = path.PATH
from scripts import additional_calculations

if __name__ == '__main__':
    if len(sys.argv) > 1: # limit to specific city
        citynumber = int(sys.argv[1])
        cityid = list(cities.keys())[citynumber]
        print(cityid)
        cities = {k:v for (k,v) in cities.items() if k == cityid}

    poi_source_list = ["grid", "railwaystation"]
    prune_measure_list = ["betweenness", "closeness", "random"]
    parsets = list(itertools.product(poi_source_list, prune_measure_list))

    if len(sys.argv) > 2: # limit to specific parameter set
        parsets_used = [parsets[int(sys.argv[2])]]
    else:
        parsets_used = parsets

    for poi_source, prune_measure in parsets_used:
        print(poi_source, prune_measure)

        print("Running 09.py")
        additional_calculations.main(PATH,cities)