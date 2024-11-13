
# This script is copied from code/09_supplements.ipynb
# It supplements and updates existing results with additional calculations.
from scripts.initialize import *
from scripts.functions import *

def main(PATH, cities):
    
    warnings.filterwarnings('ignore')

    # Assuming PATH is a dictionary where "data" and "results" are Path objects
    for placeid, placeinfo in cities.items():
        print(f"{placeid}: Analyzing results")

        # Load networks
        G_carall = csv_to_ig(PATH["data"] / placeid, placeid, 'carall')

        # Load POIs
        poi_file = PATH["data"] / placeid / f"{placeid}_poi_{poi_source}_nnidscarall.csv"
        with open(poi_file) as f:
            nnids = [int(line.rstrip()) for line in f]

        # Load results
        filename = f"{placeid}_poi_{poi_source}_{prune_measure}"
        result_file_path = PATH["results"] / placeid / f"{filename}.pickle"
        with open(result_file_path, 'rb') as resultfile:
            res = pickle.load(resultfile)

        # Calculate
        output, covs = calculate_metrics_additively(
            res["GTs"], res["GT_abstracts"], res["prune_quantiles"],
            G_carall, nnids, buffer_walk=buffer_walk,
            numnodepairs=numnodepairs, verbose=False, return_cov=True,
            Gexisting={}, output={"directness_lcc_linkwise": [], "directness_all_linkwise": []}
        )

        # Read old results
        results_old_file = PATH["results"] / placeid / f"{placeid}_poi_{poi_source}_{prune_measure}.csv"
        results_old = np.genfromtxt(results_old_file, delimiter=',', names=True)

        # Stitch the results together
        output_final = {}
        for fieldname in results_old.dtype.names:
            if fieldname not in ["directness_lcc_linkwise", "directness_all_linkwise"]:
                output_final[fieldname] = list(results_old[fieldname])
        for fieldname in output.keys():
            output_final[fieldname] = output[fieldname]

        # Overwrite old results
        write_result(output_final, "dict", placeid, poi_source, prune_measure, ".csv")

        # Same for MST
        output_MST, cov_MST = calculate_metrics(
            res["MST"], res["MST_abstract"], G_carall, nnids,
            calcmetrics={"directness_lcc_linkwise": 0, "directness_all_linkwise": 0},
            buffer_walk=buffer_walk, numnodepairs=numnodepairs,
            verbose=debug, return_cov=True, G_prev=ig.Graph(),
            cov_prev=Polygon(), ignore_GT_abstract=False, Gexisting={}
        )

        # Read old MST results
        mst_results_file = PATH["results"] / placeid / f"{placeid}_poi_{poi_source}_mst.csv"
        results_MST_old = np.genfromtxt(mst_results_file, delimiter=',', names=True)

        # Stitch MST results together
        output_MST_final = {}
        for fieldname in results_MST_old.dtype.names:
            if fieldname not in ["directness_lcc_linkwise", "directness_all_linkwise"]:
                output_MST_final[fieldname] = results_MST_old[fieldname]
        for fieldname in output_MST.keys():
            output_MST_final[fieldname] = output_MST[fieldname]

        # Overwrite old MST results
        write_result(output_MST_final, "dict", placeid, poi_source, "", "mst.csv")
    pass

if __name__ == "__main__":
    main()
    
