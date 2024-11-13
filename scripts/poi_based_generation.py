from scripts.initialize import *
from scripts.functions import *
from parameters.parameters import *

def main(PATH, cities):
        
    timing_data = []

    timing_file = PATH["data"] / "03_poi_based_generation.csv"

    for placeid, placeinfo in cities.items():
        
    
        print(placeid + ": Generating networks")

        # Start timer for network generation
        start_time_total = time.time()

        # Load networks
        start_time_network = time.time()
        G_carall = csv_to_ig(PATH["data"] / placeid, placeid, 'carall')
        end_time_network = time.time()
        network_duration = end_time_network - start_time_network
        
        # Load POIs
        start_time_poi = time.time()
        with open(Path(PATH["data"]) / placeid / f"{placeid}_poi_{poi_source}_nnidscarall.csv") as f:
            nnids = [int(line.rstrip()) for line in f]
        end_time_poi = time.time()
        poi_duration = end_time_poi - start_time_poi

        # Generation
        start_time_triangulation = time.time()
        (GTs, GT_abstracts) = greedy_triangulation_routing(G_carall,G_carall, nnids, prune_quantiles, prune_measure)
        end_time_triangulation = time.time()
        triangulation_duration = end_time_triangulation - start_time_triangulation

        start_time_mst = time.time()
        (MST, MST_abstract) = mst_routing(G_carall,G_carall, nnids)
        end_time_mst = time.time()
        mst_duration = end_time_mst - start_time_mst

        # End total timer
        end_time_total = time.time()
        total_duration = end_time_total - start_time_total

        # Write results
        results = {
            "placeid": placeid,
            "prune_measure": prune_measure,
            "poi_source": poi_source,
            "prune_quantiles": prune_quantiles,
            "GTs": GTs,
            "GT_abstracts": GT_abstracts,
            "MST": MST,
            "MST_abstract": MST_abstract
        }
        write_result(results, "pickle", placeid, poi_source, prune_measure, ".pickle")

        # Append timing data
        timing_data.append([placeid, "Network Loading", network_duration])
        timing_data.append([placeid, "POI Loading", poi_duration])
        timing_data.append([placeid, "Triangulation Generation", triangulation_duration])
        timing_data.append([placeid, "MST Generation", mst_duration])
        timing_data.append([placeid, "Total Process Time", total_duration])
        
    with open(timing_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header
        writer.writerows(timing_data)

    print(f"Timing data saved to {timing_file}")
    pass

if __name__ == "__main__":
    main()