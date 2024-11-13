
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

#------------------------------------------------#
from scripts import path
from scripts.initialize import itertools, cities

debug = False
PATH = path.PATH
print(cities)
from scripts import poi_based_generation, analyze_results, plot_results 

if __name__ == '__main__':
    if len(sys.argv) > 1: # limit to specific city
        citynumber = int(sys.argv[1])
        cityid = list(cities.keys())[citynumber]
        print(cityid)
        cities = {k:v for (k,v) in cities.items() if k == cityid}

    # 01 and 02 are done locally instead to supervise 
    # the OSM connection process manually
    #print("Running 01.py")
    #exec(open("01.py").read())
    #print("Running 02.py")
    #exec(open("02.py").read())

    poi_source_list = ["grid", "railwaystation"]
    prune_measure_list = ["betweenness", "closeness", "random"]
    parsets = list(itertools.product(poi_source_list, prune_measure_list))

    if len(sys.argv) > 2: # limit to specific parameter set
        parsets_used = [parsets[int(sys.argv[2])]]
    else:
        parsets_used = parsets 

    for poi_source, prune_measure in parsets_used:
        print(poi_source, prune_measure)

        print("Running 03.py")
        poi_based_generation.main(PATH, cities)

        print("Running 04.py")
        analyze_results.main(PATH, cities)

        print("Running 05.py")
        plot_results.main(PATH, cities)