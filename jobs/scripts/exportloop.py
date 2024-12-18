import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

#------------------------------------------------#
from scripts import path
from scripts.initialize import itertools, cities
from parameters.parameters import  prune_measure, poi_source, smallcitythreshold, prune_measures, prune_quantiles,plotparam
from scripts import export_carconstrictedbikes

debug = False
PATH = path.PATH


if __name__ == '__main__':
    if len(sys.argv) > 1:  # Limit to specific city
        citynumber = int(sys.argv[1])
        cityid = list(cities.keys())[citynumber]
        print(cityid)
        cities = {k: v for (k, v) in cities.items() if k == cityid}
        if citynumber > smallcitythreshold:
            prune_quantiles = [0.5, 1]

    poi_source_list = ["grid", "railwaystation"]
    prune_measure_list = ["betweenness", "closeness", "random"]
    parsets = list(itertools.product(poi_source_list, prune_measure_list))

    if len(sys.argv) > 2:  # Limit to specific parameter set
        parsets_used = [parsets[int(sys.argv[2])]]
    else:
        parsets_used = parsets

    for poi_source, prune_measure in parsets_used:
        print(poi_source, prune_measure)

        print("Running export_carconstrictedbikes.main()")
        # Call the main function with required arguments
        export_carconstrictedbikes.main(
            PATH=PATH,
            cities=cities,
            poi_source=poi_source,
            prune_measure=prune_measure,
            prune_quantiles=prune_quantiles,
            debug=debug,
            plotparam=plotparam
        )