warnings.filterwarnings('ignore')

plotconstricted = False # If True, will add plots about constricted street network metrics.

# %%capture
# Prepare the timing file path
timing_file = PATH["data"] / "timing_analysis_plots.csv"
timing_data = []

for placeid, placeinfo in cities.items():
    print(placeid + ": Plotting networks")

    start_time_total = time.time()  # Start total timing
    
    # Start timing for setting up plotting parameters
    start_time_setup = time.time()
    if prune_measure == "betweenness":
        weight_abstract = True
    else:
        weight_abstract = 6

    plots_networks_path = Path(PATH["plots_networks"]) / placeid
    end_time_setup = time.time()
    setup_duration = end_time_setup - start_time_setup

    # EXISTING INFRASTRUCTURE
    # Load networks
    start_time_load_networks = time.time()
    G_biketrack = csv_to_ig(PATH["data"] / placeid, placeid, 'biketrack')
    G_carall = csv_to_ig(PATH["data"] / placeid, placeid, 'carall')
    G_biketrackcarall = csv_to_ig(PATH["data"] / placeid, placeid, 'biketrackcarall')
    G_bikeable = csv_to_ig(PATH["data"] / placeid, placeid, 'bikeable')
    map_center = nxdraw(G_carall, "carall")
    end_time_load_networks = time.time()
    network_loading_duration = end_time_load_networks - start_time_load_networks

    # PLOT existing networks
    start_time_plot = time.time()

    # Plot and save G_carall
    fig = initplot()
    nxdraw(G_carall, "carall", map_center)
    plt.savefig(plots_networks_path / f'{placeid}_carall.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_carall.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    # Plot and save G_biketrack
    fig = initplot()
    nxdraw(G_biketrack, "biketrack", map_center)
    plt.savefig(plots_networks_path / f'{placeid}_biketrack.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_biketrack.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    # Plot and save G_bikeable
    fig = initplot()
    nxdraw(G_bikeable, "bikeable", map_center)
    plt.savefig(plots_networks_path / f'{placeid}_bikeable.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_bikeable.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    # Plot and save G_biketrackcarall
    fig = initplot()
    nxdraw(G_carall, "carall", map_center)
    nxdraw(G_biketrack, "biketrack", map_center, list(set([v["id"] for v in G_biketrack.vs]).intersection(set([v["id"] for v in G_carall.vs]))))
    nxdraw(G_biketrack, "biketrack_offstreet", map_center, list(set([v["id"] for v in G_biketrack.vs]).difference(set([v["id"] for v in G_carall.vs]))))
    plt.savefig(Path(PATH["plots_networks"]) / placeid / f'{placeid}_biketrackcarall.pdf', bbox_inches="tight")
    plt.savefig(Path(PATH["plots_networks"]) / placeid / f'{placeid}_biketrackcarall.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    end_time_plot = time.time()
    plot_duration = end_time_plot - start_time_plot

    # Load POIs
    start_time_load_pois = time.time()
    with open(Path(PATH["data"]) / placeid / f"{placeid}_poi_{poi_source}_nnidscarall.csv") as f:
        nnids = [int(line.rstrip()) for line in f]
    nodesize_poi = nodesize_from_pois(nnids)
    end_time_load_pois = time.time()
    poi_loading_duration = end_time_load_pois - start_time_load_pois

    # Plot and save POIs
    start_time_plot_poi = time.time()
    fig = initplot()
    nxdraw(G_carall, "carall", map_center)
    nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
    plt.savefig(plots_networks_path / f'{placeid}_carall_poi_{poi_source}.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_carall_poi_{poi_source}.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()
    end_time_plot_poi = time.time()
    poi_plotting_duration = end_time_plot_poi - start_time_plot_poi

    # End total timing
    end_time_total = time.time()
    total_duration = end_time_total - start_time_total

    # Append timing data for each placeid and step
    timing_data.append([placeid, "Setup", setup_duration])
    timing_data.append([placeid, "Network Loading", network_loading_duration])
    timing_data.append([placeid, "Plotting Networks", plot_duration])
    timing_data.append([placeid, "POI Loading", poi_loading_duration])
    timing_data.append([placeid, "POI Plotting", poi_plotting_duration])
    timing_data.append([placeid, "Total Process Time", total_duration])

# Save the timing data to a CSV file
with open(timing_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header
    writer.writerows(timing_data)

print(f"Timing data saved to {timing_file}")




# Path to store the timing log CSV file
timing_file = PATH["data"] / "timing_analysis_plots_2.csv"

# Initialize a list to store timing information in rows
timing_data = []

# Write the header before the loop
with open(timing_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header

# %%capture
for placeid, placeinfo in cities.items():
    print(placeid + ": Plotting networks")
    
    plots_networks_path = Path(PATH["plots_networks"]) / placeid
    
    if prune_measure == "betweenness":
        weight_abstract = True
    else:
        weight_abstract = 6

    # Timing: Load networks
    start_time = time.time()
    
    # EXISTING INFRASTRUCTURE
    G_carall = csv_to_ig(PATH["data"] / placeid, placeid, 'carall')
    map_center = nxdraw(G_carall, "carall")
    
    load_time = time.time() - start_time
    timing_data.append([placeid, "Load networks", load_time])

    # Load POIs
    start_time = time.time()
    
    with open(Path(PATH["data"]) / placeid / f'{placeid}_poi_{poi_source}_nnidscarall.csv') as f:
        nnids = [int(line.rstrip()) for line in f]
    
    nodesize_poi = nodesize_from_pois(nnids)
    
    # Plotting: carall + POIs
    fig = initplot()
    nxdraw(G_carall, "carall", map_center)
    nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
    plt.savefig(plots_networks_path / f'{placeid}_carall_poi_{poi_source}.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_carall_poi_{poi_source}.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    plot_time = time.time() - start_time
    timing_data.append([placeid, "Plot carall + POIs", plot_time])
    
    # Timing: Load results
    start_time = time.time()
    filename = placeid + '_poi_' + poi_source + "_" + prune_measure + ".pickle"
    with open(PATH["results"] / placeid / filename, 'rb') as f:
        res = pickle.load(f)

    result_load_time = time.time() - start_time
    timing_data.append([placeid, "Load results", result_load_time])
    
    # Plot abstract MST
    start_time = time.time()
    fig = initplot()
    nxdraw(G_carall, "carall", map_center)
    nxdraw(res["MST_abstract"], "abstract", map_center, weighted=6)
    nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
    nxdraw(G_carall, "poi_reached", map_center, list(set([v["id"] for v in res["MST"].vs]).intersection(set(nnids))), "nx.draw_networkx_nodes", nodesize_poi)
    plt.savefig(plots_networks_path / f'{placeid}_MSTabstract_poi_{poi_source}.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_MSTabstract_poi_{poi_source}.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    mst_abstract_plot_time = time.time() - start_time
    timing_data.append([placeid, "Plot abstract MST", mst_abstract_plot_time])

    # Plot MST all together
    start_time = time.time()
    fig = initplot()
    nxdraw(G_carall, "carall", map_center)
    nxdraw(res["MST"], "bikegrown", map_center, nodesize=0)
    nxdraw(res["MST_abstract"], "abstract", map_center, weighted=6)
    nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
    nxdraw(G_carall, "poi_reached", map_center, list(set([v["id"] for v in res["MST"].vs]).intersection(set(nnids))), "nx.draw_networkx_nodes", nodesize_poi)
    plt.savefig(plots_networks_path / f'{placeid}_MSTabstractall_poi_{poi_source}.pdf', bbox_inches="tight")
    plt.savefig(plots_networks_path / f'{placeid}_MSTabstractall_poi_{poi_source}.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()

    mst_all_plot_time = time.time() - start_time
    timing_data.append([placeid, "Plot MST all together", mst_all_plot_time])

    # Plot abstract greedy triangulation
    for GT_abstract, prune_quantile in zip(res["GT_abstracts"], res["prune_quantiles"]):
        start_time = time.time()
        fig = initplot()
        nxdraw(G_carall, "carall")
        try:
            GT_abstract.es["weight"] = GT_abstract.es["width"]
        except KeyError:
            pass  # Use specific exception handling
        
        nxdraw(GT_abstract, "abstract", map_center, drawfunc="nx.draw_networkx_edges", nodesize=0, weighted=weight_abstract, maxwidthsquared=nodesize_poi)
        nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
        nxdraw(G_carall, "poi_reached", map_center, list(set([v["id"] for v in GT_abstract.vs]).intersection(set(nnids))), "nx.draw_networkx_nodes", nodesize_poi)
        filename = f'{placeid}_GTabstract_poi_{poi_source}_{prune_measures[prune_measure]}_{prune_quantile:.3f}.png'
        plt.savefig(plots_networks_path / filename, bbox_inches="tight", dpi=plotparam["dpi"])
        plt.close()

        greedy_time = time.time() - start_time
        timing_data.append([placeid, f"Plot abstract greedy triangulation {prune_quantile:.3f}", greedy_time])

    # Plot all together
    for GT, prune_quantile in zip(res["GTs"], res["prune_quantiles"]):
        start_time = time.time()
        fig = initplot()
        nxdraw(G_carall, "carall")
        nxdraw(GT, "bikegrown", map_center, nodesize=nodesize_grown)
        nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
        nxdraw(G_carall, "poi_reached", map_center, list(set([v["id"] for v in GT.vs]).intersection(set(nnids))), "nx.draw_networkx_nodes", nodesize_poi)
        filename = f'{placeid}_GTall_poi_{poi_source}_{prune_measures[prune_measure]}_{prune_quantile:.3f}.png'
        plt.savefig(plots_networks_path / filename, bbox_inches="tight", dpi=plotparam["dpi"])
        plt.close()

        all_together_time = time.time() - start_time
        timing_data.append([placeid, f"Plot all together {prune_quantile:.3f}", all_together_time])

# Write the timing data to the CSV file
with open(timing_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(timing_data)

print(f"Timing data saved to {timing_file}")
        



# %%capture
# Path to the timing file
timing_file = PATH["data"] / "timing_analysis_plots_3.csv"

# Initialize a list to store timing information in rows
timing_data = []

# Write the header to the CSV file
with open(timing_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header

# Loop through cities and track the time for each step
for placeid, placeinfo in cities.items():
    print(placeid + ": Plotting network covers")

    # Track the time for each process and log it
    start_time = time.time()
    G_biketrack = csv_to_ig(PATH["data"] / placeid, placeid, 'biketrack')
    G_carall = csv_to_ig(PATH["data"] / placeid, placeid, 'carall')
    G_biketrackcarall = csv_to_ig(PATH["data"] / placeid, placeid, 'biketrackcarall')
    G_bikeable = csv_to_ig(PATH["data"] / placeid, placeid, 'bikeable')
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Loading Networks", time_taken])

    start_time = time.time()
    map_center = nxdraw(G_carall, "carall")
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Drawing Map Center", time_taken])

    data_path = Path(PATH["data"]) / placeid
    results_path = Path(PATH["results"]) / placeid

    start_time = time.time()
    with open(data_path / f'{placeid}_poi_{poi_source}_nnidscarall.csv') as f:
        nnids = [int(line.rstrip()) for line in f]
    nodesize_poi = nodesize_from_pois(nnids)
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Loading POIs", time_taken])

    start_time = time.time()
    filename = f'{placeid}_poi_{poi_source}_{prune_measure}.pickle'
    with open(results_path / filename, 'rb') as f:
        res = pickle.load(f)
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Loading Results", time_taken])

    start_time = time.time()
    filename_covers = f'{placeid}_poi_{poi_source}_{prune_measure}_covers.pickle'
    with open(results_path / filename_covers, 'rb') as f:
        covs = pickle.load(f)
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Loading Covers", time_taken])

    start_time = time.time()
    filename_existing_covers = f'{placeid}_existing_covers.pickle'
    with open(results_path / filename_existing_covers, 'rb') as f:
        cov_car = pickle.load(f)['carall']
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Loading Existing Covers", time_taken])

    start_time = time.time()
    patchlist_car, patchlist_car_holes = cov_to_patchlist(cov_car, map_center)
    patchlist_bike, patchlist_bike_holes = cov_to_patchlist(covs.get("bikeable", []), map_center)  # Use empty list as default  # Example for "bikeable" cover
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Constructing Patches", time_taken])

    start_time = time.time()
    fig = initplot()
    # (Add other plotting steps here if necessary)
    plt.savefig(plots_networks_path / f'{placeid}_plot.png', bbox_inches="tight", dpi=plotparam["dpi"])
    plt.close()
    time_taken = time.time() - start_time
    timing_data.append([placeid, "Saving Plot", time_taken])

# After the loop, save the timing data to the CSV file
with open(timing_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(timing_data)  # Write timing data rows
        
        
timing_file = PATH["data"] / "timing_analysis_networks.csv"

# Initialize a list to store timing information
timing_data = []

# Write the header before the loop
with open(timing_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header

for placeid, placeinfo in tqdm(cities.items(), desc="Cities"):
    print(placeid + ": Plotting networks...")
    
    # Start timing for loading results
    start_time = time.time()

    filename = placeid + '_poi_' + poi_source + "_" + prune_measure + ".pickle"
    with open(PATH["results"] / placeid / filename, 'rb') as f:
        res = pickle.load(f)

    load_time = time.time() - start_time
    timing_data.append([placeid, "Load Results", load_time])
    
    # Start timing for loading POIs
    start_time = time.time()

    with open(PATH["data"] / placeid / f"{placeid}_poi_{poi_source}_nnidscarall.csv") as f:
        nnids = [int(line.rstrip()) for line in f]
    nodesize_poi = nodesize_from_pois(nnids)

    load_poi_time = time.time() - start_time
    timing_data.append([placeid, "Load POIs", load_poi_time])
    
    try:
        # Start timing for loading networks
        start_time = time.time()

        G_biketrack = csv_to_ig(PATH["data"] / placeid, placeid, 'biketrack')
        G_carall = csv_to_ig(PATH["data"] / placeid, placeid, 'carall')
        G_biketrackcarall = csv_to_ig(PATH["data"] / placeid, placeid, 'biketrackcarall')
        G_bikeable = csv_to_ig(PATH["data"] / placeid , placeid, 'bikeable')
        map_center = nxdraw(G_carall, "carall")

        load_networks_time = time.time() - start_time
        timing_data.append([placeid, "Load Networks", load_networks_time])
        
        # Start timing for plotting overlaps with biketracks
        start_time = time.time()

        for GT, prune_quantile in tqdm(zip(res["GTs"], res["prune_quantiles"]), "Overlaps with biketracks", total=len(res["prune_quantiles"])):
            fig = initplot()
            nxdraw(G_carall, "carall")
            nxdraw(G_biketrack, "biketrack", map_center, list(set([v["id"] for v in G_biketrack.vs]).intersection(set([v["id"] for v in G_carall.vs]))))
            nxdraw(GT, "bikegrown", map_center, nodesize=0)
            nxdraw(GT, "highlight_biketrack", map_center, list(set([v["id"] for v in G_biketrack.vs]).intersection(set([v["id"] for v in GT.vs]))))
            plt.savefig(PATH["plots_networks"] / placeid / f"{placeid}_GTalloverlapbiketrack_poi_{poi_source}_{prune_measures[prune_measure]}_{prune_quantile:.3f}.png", bbox_inches="tight", dpi=plotparam["dpi"])
            plt.close()

        plot_biketrack_time = time.time() - start_time
        timing_data.append([placeid, "Plot Overlaps with Biketracks", plot_biketrack_time])
        
        # Start timing for plotting overlaps with bikeable networks
        start_time = time.time()

        for GT, prune_quantile in tqdm(zip(res["GTs"], res["prune_quantiles"]), "Overlaps with bikeable", total=len(res["prune_quantiles"])):
            fig = initplot()
            nxdraw(G_carall, "carall")
            nxdraw(G_bikeable, "bikeable", map_center, list(set([v["id"] for v in G_bikeable.vs]).intersection(set([v["id"] for v in G_carall.vs]))))
            nxdraw(GT, "bikegrown", map_center, nodesize=0)
            nxdraw(GT, "highlight_bikeable", map_center, list(set([v["id"] for v in G_bikeable.vs]).intersection(set([v["id"] for v in GT.vs]))))
            nxdraw(G_carall, "poi_unreached", map_center, nnids, "nx.draw_networkx_nodes", nodesize_poi)
            nxdraw(G_carall, "poi_reached", map_center, list(set([v["id"] for v in GT.vs]).intersection(set(nnids))), "nx.draw_networkx_nodes", nodesize_poi)
            plt.savefig(PATH["plots_networks"] / placeid / f"{placeid}_GTalloverlapbikeable_poi_{poi_source}_{prune_measures[prune_measure]}_{prune_quantile:.3f}.png", bbox_inches="tight", dpi=plotparam["dpi"])
            plt.close()

        plot_bikeable_time = time.time() - start_time
        timing_data.append([placeid, "Plot Overlaps with Bikeable Networks", plot_bikeable_time])

    except:
        print(placeinfo["name"] + ": No bike tracks found")

# Save timing data to the CSV file
with open(timing_file, mode='a', newline='') as file:
    writer = csv.writer(file)
        
# Either: Run all parameter sets
# poi_source_list = ["grid", "railwaystation"]
# prune_measure_list = ["betweenness", "closeness", "random"]
# parsets_used = list(itertools.product(poi_source_list, prune_measure_list))

# Or: Run one parameter set
parsets_used = [(poi_source, prune_measure)]

for poi_source_this, prune_measure_this in parsets_used:
    print(poi_source_this, prune_measure_this)
        
        
    for placeid, placeinfo in tqdm(cities.items(), desc="Cities"):

        # PLOT Analysis
        filename = f"{placeid}_poi_{poi_source_this}_{prune_measure_this}.csv"
        file_path = Path(PATH["results"]) / placeid / filename
        analysis_result = np.genfromtxt(file_path, delimiter=',', names=True)
        
        if len(analysis_result) == 0: # No plot if no results (for example no railwaystations)
            print(placeid + ": No analysis results available")
            continue

        print(placeid + ": Plotting analysis results...")

        # Load existing networks
        # G_biketrack = csv_to_ig(PATH["data"] + placeid + "/", placeid, 'biketrack')
        # G_carall = csv_to_ig(PATH["data"] + placeid + "/", placeid, 'carall')
        # G_bikeable = csv_to_ig(PATH["data"] + placeid + "/", placeid, 'bikeable')
        # G_biketrack_onstreet = intersect_igraphs(G_biketrack, G_carall)
        # G_bikeable_onstreet = intersect_igraphs(G_bikeable, G_carall)


        # First path
        filename = f"{placeid}_poi_{poi_source_this}_mst.csv"
        file_path = Path(PATH["results"]) / placeid / filename
        analysis_mst_result = np.genfromtxt(file_path, delimiter=',', names=True)

        filename = f"{placeid}_existing.csv"
        file_path = Path(PATH["results"]) / placeid / filename
        analysis_existing = np.genfromtxt(file_path, delimiter=',', names=True)
           
        prune_quantiles_constricted = prune_quantiles
        if plotconstricted:
            f = (Path(PATH["results_constricted"]) / f"results_{poi_source_this}_{prune_measure_this}" / f"metrics_{poi_source_this}_{prune_measure_this}"  / f"{placeid}_carconstrictedbike_poi_{poi_source_this}_{prune_measure_this}.csv")    
            if os.path.isfile(f):
                analysis_result_constricted = np.loadtxt(f, delimiter=',', usecols = (2,3,4,5,6,7,8,9,10), skiprows=1)
                if np.shape(analysis_result_constricted)[0] == 3: # for large cities we only calculated 3 values
                    prune_quantiles_constricted = [prune_quantiles[19], prune_quantiles[-1]]
                    
        nc = 5
        fig, axes = plt.subplots(nrows = 2, ncols = nc, figsize = (16, 6))
        # Bike network
        keys_metrics = {"length": "Length [km]","coverage": "Coverage [km$^2$]","overlap_biketrack": "Overlap Protected","directness_all_linkwise": "Directness","efficiency_global": "Global Efficiency",
                "length_lcc": "Length of LCC [km]","poi_coverage": "POIs covered","overlap_bikeable": "Overlap Bikeable","components": "Components","efficiency_local": "Local Efficiency"}
        
        for i, ax in enumerate(axes[0]):
            key = list(keys_metrics.keys())[i]
            if key in ["overlap_biketrack", "overlap_bikeable"]:
                ax.plot(prune_quantiles, analysis_result[key] / analysis_result["length"], **plotparam_analysis["bikegrown"])
            elif key in ["efficiency_global", "efficiency_local"]:
                ax.plot(prune_quantiles, analysis_result[key], **plotparam_analysis["bikegrown_abstract"])
                xmin, xmax = ax.get_xlim()
                tmp, = ax.plot([xmin, xmax], [analysis_mst_result[key], analysis_mst_result[key]], **plotparam_analysis["mst"])  # MST is equivalent for abstract and routed
                tmp.set_label('_hidden')
                tmp, = ax.plot(prune_quantiles, analysis_result[key+"_routed"], **plotparam_analysis["bikegrown"])
                tmp.set_label('_hidden')
            elif key in ["length", "length_lcc"]: # Convert m->km
                ax.plot(prune_quantiles, analysis_result[key]/1000, **plotparam_analysis["bikegrown"])
                xmin, xmax = ax.get_xlim()
                ax.plot([xmin, xmax], [analysis_mst_result[key]/1000, analysis_mst_result[key]/1000], **plotparam_analysis["mst"])
            else:
                ax.plot(prune_quantiles, analysis_result[key], **plotparam_analysis["bikegrown"])
                xmin, xmax = ax.get_xlim()
                ax.plot([xmin, xmax], [analysis_mst_result[key], analysis_mst_result[key]], **plotparam_analysis["mst"])
                
            try:
                if key in ["length", "length_lcc"]: # Convert m->km
                    tmp, = ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["biketrack"]]/1000, analysis_existing[key][analysis_existing_rowkeys["biketrack"]]/1000], **plotparam_analysis["biketrack"])
                else:
                    tmp, = ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["biketrack"]], analysis_existing[key][analysis_existing_rowkeys["biketrack"]]], **plotparam_analysis["biketrack"])
                if key in ["efficiency_global", "efficiency_local"]:
                    tmp.set_label('_hidden')

                if key in ["length", "length_lcc"]: # Convert m->km
                    tmp, = ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["bikeable"]]/1000, analysis_existing[key][analysis_existing_rowkeys["bikeable"]]/1000], **plotparam_analysis["bikeable"])
                else:
                    tmp, = ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["bikeable"]], analysis_existing[key][analysis_existing_rowkeys["bikeable"]]], **plotparam_analysis["bikeable"])
                if key in ["efficiency_global", "efficiency_local"]:
                    tmp.set_label('_hidden')
            except:
                pass

            if key == "efficiency_global" and plotconstricted:
                ax.plot([0]+prune_quantiles_constricted, analysis_result_constricted[:, 0], **plotparam_analysis["constricted"])

            if i == 0:
                ymax0 = ax.get_ylim()[1]
                ax.set_ylim(0, ymax0)
                ax.text(-0.15, ymax0*1.25, placeinfo['name'] + " (" + poi_source_this + " | " + prune_measure_this + ")", fontsize=16, horizontalalignment='left')
                ax.legend(loc = 'upper left')
            if i == 4:
                ax.legend(loc = 'best')

            if key == "directness_all_linkwise" and plotconstricted:
                ax.plot([0]+prune_quantiles_constricted, analysis_result_constricted[:, -1], **plotparam_analysis["constricted"])

            set_analysissubplot(key)
            ax.set_title(list(keys_metrics.values())[i])
            ax.set_xlabel('')
            ax.set_xticklabels([])


        for i, ax in enumerate(axes[1]):
            key = list(keys_metrics.keys())[i+nc]
            if key in ["overlap_biketrack", "overlap_bikeable"]:
                ax.plot(prune_quantiles, analysis_result[key] / analysis_result["length"], **plotparam_analysis["bikegrown"])
            elif key in ["efficiency_global", "efficiency_local"]:
                ax.plot(prune_quantiles, analysis_result[key], **plotparam_analysis["bikegrown_abstract"])
                xmin, xmax = ax.get_xlim()
                ax.plot([xmin, xmax], [analysis_mst_result[key], analysis_mst_result[key]], **plotparam_analysis["mst"]) # MST is equivalent for abstract and routed
                ax.plot(prune_quantiles, analysis_result[key+"_routed"], **plotparam_analysis["bikegrown"])
            elif key in ["length", "length_lcc"]: # Convert m->km
                ax.plot(prune_quantiles, analysis_result[key]/1000, **plotparam_analysis["bikegrown"])
                xmin, xmax = ax.get_xlim()
                ax.plot([xmin, xmax], [analysis_mst_result[key]/1000, analysis_mst_result[key]/1000], **plotparam_analysis["mst"])
            else:
                ax.plot(prune_quantiles, analysis_result[key], **plotparam_analysis["bikegrown"])
                xmin, xmax = ax.get_xlim()
                ax.plot([xmin, xmax], [analysis_mst_result[key], analysis_mst_result[key]], **plotparam_analysis["mst"])
            try:
                if key in ["length", "length_lcc"]: # Convert m->km
                    ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["biketrack"]]/1000, analysis_existing[key][analysis_existing_rowkeys["biketrack"]]/1000], **plotparam_analysis["biketrack"])
                    ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["bikeable"]]/1000, analysis_existing[key][analysis_existing_rowkeys["bikeable"]]/1000], **plotparam_analysis["bikeable"])
                else:
                    if not (key == "poi_coverage" and poi_source_this == "railwaystation"):
                        ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["biketrack"]], analysis_existing[key][analysis_existing_rowkeys["biketrack"]]], **plotparam_analysis["biketrack"])
                        ax.plot([xmin, xmax], [analysis_existing[key][analysis_existing_rowkeys["bikeable"]], analysis_existing[key][analysis_existing_rowkeys["bikeable"]]], **plotparam_analysis["bikeable"])
            except:
                pass
            if key == "efficiency_local" and plotconstricted:
                ax.plot([0]+prune_quantiles_constricted, analysis_result_constricted[:, 1], **plotparam_analysis["constricted"])

            if i == 0:
                ax.set_ylim(0, ymax0)
            set_analysissubplot(key)
            ax.set_title(list(keys_metrics.values())[i+nc])
            ax.set_xlabel(prune_measure_this + ' quantile')
            if key in ["poi_coverage"]:
                # https://stackoverflow.com/questions/30914462/matplotlib-how-to-force-integer-tick-labels
                ax.yaxis.set_major_locator(MaxNLocator(integer=True)) 

        plt.subplots_adjust(top = 0.87, bottom = 0.09, left = 0.05, right = 0.97, wspace = 0.25, hspace = 0.25)
        if plotconstricted:
            filename = f"{placeid}_analysis_poi_{poi_source_this}_{prune_measure_this}.png"
        else:
            filename = f"{placeid}_analysis_poi_{poi_source_this}_{prune_measure_this}_noconstr.png"

        # Create the full path using pathlib
        save_path = Path(PATH["plots"]) / placeid / filename

        # Save the figure
        fig.savefig(save_path, facecolor="white", edgecolor='none')
        plt.close()     
        
        end_time = time.time()
        duration = end_time - start_time
        timing_data.append([placeid, 'Plotting analysis results', duration])




# Save timing data to CSV
timing_file = PATH["data"] / "overlap_bikable_time.csv"  # Define your timing file path
with open(timing_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header
    writer.writerows(timing_data)
    
print(f"Timing data saved to {timing_file}")
        
if plotconstricted:
    for placeid, placeinfo in tqdm(cities.items(), desc="Cities"):
        prune_measure_this = "betweenness"
        for poi_source_this in ["railwaystation", "grid"]:
            f = PATH["results_constricted"] + poi_source_this + "/" + placeid + constricted_parameternamemap[prune_measure_this] + constricted_parameternamemap[poi_source_this] + ".csv"
            if os.path.isfile(f):
                analysis_result_constricted = np.loadtxt(f, delimiter=',', usecols = (2,3,4,5,6,7,8,9,10), skiprows=1)
    
                fig, axes = plt.subplots(nrows = 1, ncols = 5, figsize = (16, 3))
    
                for i, ax in enumerate(axes):
                    ax.set_title(constricted_plotinfo["title"][i])
                    ax.set_xlabel(prune_measure_this + ' quantile')
                    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
                    ax.set_xlim(-0.05, 1.05)
                    ax.spines['right'].set_visible(False)
                    ax.spines['top'].set_visible(False)
    
                    # Efficiency global
                    if i == 0:
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 0], **plotparam_analysis["constricted"])
                        ymin, ymax = ax.get_ylim()
                        ax.text(-0.25, ymin + (ymax-ymin)*1.2, placeinfo['name'] + " streets (" + poi_source_this + ", " + prune_measure_this + " growth)", fontsize=16, horizontalalignment='left')
    
                    # Efficiency local
                    elif i == 1:
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 1], **plotparam_analysis["constricted"])
    
                    # Directness
                    elif i == 2:
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, -1], **plotparam_analysis["constricted"])
    
                    # Clustering
                    elif i == 3:
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 2], **plotparam_analysis["constricted_10"])
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 3], **plotparam_analysis["constricted_5"])
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 4], **plotparam_analysis["constricted_3"])
                        ax.legend(loc = 'best')
    
                    # Anisotropy
                    elif i == 4:
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 5], **plotparam_analysis["constricted_10"])
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 6], **plotparam_analysis["constricted_5"])
                        ax.plot([0]+prune_quantiles, analysis_result_constricted[:, 7], **plotparam_analysis["constricted_3"])
                        
                plt.subplots_adjust(top = 0.79, bottom = 0.16, left = 0.05, right = 0.97, wspace = 0.25)
                fig.savefig(PATH["plots"] / placeid / f"{placeid}_analysis_poi_{poi_source_this}_{prune_measure_this}_constricted.png", facecolor="white", edgecolor='none')

            else:
                print(placeid + " / " + poi_source_this +": No results data for constricted analysis to plot")