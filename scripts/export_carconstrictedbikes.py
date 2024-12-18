from pathlib import Path
from scripts.path import PATH
from parameters.parameters import plotparam, prune_measure, poi_source, prune_measures

# System
import copy

import pickle

# GRAPH PLOTTING
import matplotlib.pyplot as plt

# Local
from scripts.functions import csv_to_ig, simplify_ig, nxdraw, constrict_overlaps
from scripts.initialize import cities

debug = False
 
def main(PATH, cities, poi_source, prune_measure, prune_quantiles, debug=False, plotparam=None):
    for placeid, placeinfo in cities.items():
        print(f"{placeid}: Exporting carconstrictedbike to picklez")

        # Load existing
        place_path = Path(PATH["data"]) / placeid
        export_path = Path(PATH["exports"]) / placeid
        results_path = Path(PATH["results"]) / placeid

        G_carall = csv_to_ig(place_path, placeid, 'carall')
        export_path.mkdir(parents=True, exist_ok=True)  # Ensure export directory exists

        with open(export_path / f"{placeid}_carall.picklez", 'wb') as f:
            G_carall_simplified = simplify_ig(G_carall)
            G_carall_simplified.write_picklez(fname=f)

        if debug:
            map_center = nxdraw(G_carall, "carall")

        # Load results
        filename = f"{placeid}_poi_{poi_source}_{prune_measure}"
        result_file = results_path / f"{filename}.pickle"

        with result_file.open('rb') as resultfile:
            res = pickle.load(resultfile)

        if debug:
            fig = initplot()
            nxdraw(
                G_carall_simplified, 
                "abstract", 
                map_center, 
                nodesize=0, 
                weighted=True, 
                maxwidthsquared=500
            )
            plt.savefig(export_path / f"{placeid}_carallweighted.png", bbox_inches="tight", dpi=plotparam["dpi"])
            plt.close()

        for GT, prune_quantile in zip(res["GTs"], res["prune_quantiles"]):
            if prune_quantile in prune_quantiles:
                prune_suffix = f"{prune_measure}{prune_quantile:.3f}"  # Ensure prune_suffix is defined here

                GT_carconstrictedbike = copy.deepcopy(G_carall)
                constrict_overlaps(GT_carconstrictedbike, GT)
                GT_carconstrictedbike = simplify_ig(GT_carconstrictedbike)

                if debug:
                    fig = initplot()
                    nxdraw(
                        GT_carconstrictedbike, 
                        "abstract", 
                        map_center, 
                        nodesize=0, 
                        weighted=True, 
                        maxwidthsquared=500
                    )
                    plt.savefig(
                        export_path / f"{placeid}_carconstrictedbike_poi_{poi_source}_{prune_suffix}.png",
                        bbox_inches="tight", 
                        dpi=plotparam["dpi"]
                    )
                    plt.close()

                with open(
                    export_path / f"{placeid}_carconstrictedbike_poi_{poi_source}_{prune_suffix}.picklez", 
                    'wb'
                ) as f:
                    GT_carconstrictedbike.write_picklez(fname=f)


if __name__ == "__main__":
    main()