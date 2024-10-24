warnings.filterwarnings('ignore')
rerun_existing = True

timing_file = PATH["data"] / "analysis_results_time.csv"
timing_data = []

for placeid, placeinfo in cities.items():
    print(placeid + ": Analyzing existing infrastructure.")

    # Start total timing
    start_time_total = time.time()
    
    # Filename check
    start_time_check = time.time()
    filename = placeid + "_existing.csv"
    rerun_check = rerun_existing or not os.path.isfile(PATH["results"] + placeid + "/" + filename)
    end_time_check = time.time()
    check_duration = end_time_check - start_time_check

    if rerun_check:
        empty_metrics = {
                         "length":0,
                         "length_lcc":0,
                         "coverage": 0,
                         "directness": 0,
                         "directness_lcc": 0,
                         "poi_coverage": 0,
                         "components": 0,
                         "efficiency_global": 0,
                         "efficiency_local": 0,
                         "efficiency_global_routed": 0,
                         "efficiency_local_routed": 0,
                         "directness_lcc_linkwise": 0,
                         "directness_all_linkwise": 0
                        }
        output_place = {}
        for networktype in networktypes:
            output_place[networktype] = copy.deepcopy(empty_metrics)

        # Analyze all networks
        start_time_networks = time.time()
        Gs = {}
        for networktype in networktypes:
            if networktype != "biketrack_onstreet" and networktype != "bikeable_offstreet":
                Gs[networktype] = csv_to_ig(PATH["data"] / placeid, placeid, networktype)
                Gs[networktype + "_simplified"] = csv_to_ig(PATH["data"] / placeid , placeid, networktype + "_simplified")
            elif networktype == "biketrack_onstreet":
                Gs[networktype] = intersect_igraphs(Gs["biketrack"], Gs["carall"])
                Gs[networktype + "_simplified"] = intersect_igraphs(Gs["biketrack_simplified"], Gs["carall_simplified"])
            elif networktype == "bikeable_offstreet":
                G_temp = copy.deepcopy(Gs["bikeable"])
                delete_overlaps(G_temp, Gs["carall"])
                Gs[networktype] = G_temp
                G_temp = copy.deepcopy(Gs["bikeable_simplified"])
                delete_overlaps(G_temp, Gs["carall_simplified"])
                Gs[networktype + "_simplified"] = G_temp
        end_time_networks = time.time()
        network_analysis_duration = end_time_networks - start_time_networks

        # Load POIs
        start_time_poi = time.time()
        with open(Path(PATH["data"]) / placeid / f"{placeid}_poi_{poi_source}_nnidscarall.csv") as f:
            nnids = [int(line.rstrip()) for line in f]
        end_time_poi = time.time()
        poi_loading_duration = end_time_poi - start_time_poi

        # Metrics calculation
        start_time_metrics = time.time()
        covs = {}
        for networktype in tqdm(networktypes, desc="Networks", leave=False):
            if debug: print(placeid + ": Analyzing results: " + networktype)
            metrics, cov = calculate_metrics(Gs[networktype], Gs[networktype + "_simplified"], Gs['carall'], nnids, empty_metrics, buffer_walk, numnodepairs, debug)
            for key, val in metrics.items():
                output_place[networktype][key] = val
            covs[networktype] = cov
        end_time_metrics = time.time()
        metrics_duration = end_time_metrics - start_time_metrics

        # Save covers
        write_result(covs, "pickle", placeid, "", "", "existing_covers.pickle")

        # Write to CSV
        write_result(output_place, "dictnested", placeid, "", "", "existing.csv", empty_metrics)

    # End total timing
    end_time_total = time.time()
    total_duration = end_time_total - start_time_total

    # Append timing data
    timing_data.append([placeid, "Check File Existence", check_duration])
    timing_data.append([placeid, "Network Analysis", network_analysis_duration])
    timing_data.append([placeid, "POI Loading", poi_loading_duration])
    timing_data.append([placeid, "Metrics Calculation", metrics_duration])
    timing_data.append([placeid, "Total Process Time", total_duration])



for placeid, placeinfo in cities.items():
    print(placeid + ": Analyzing results")

    # Start total timing
    start_time_total = time.time()

    # Load networks
    start_time_load_networks = time.time()
    G_carall = csv_to_ig(PATH["data"] / placeid , placeid, 'carall')
    Gexisting = {}
    for networktype in ["biketrack", "bikeable"]:
        Gexisting[networktype] = csv_to_ig(PATH["data"] / placeid , placeid, networktype)
    end_time_load_networks = time.time()
    network_loading_duration = end_time_load_networks - start_time_load_networks

    # Load POIs
    start_time_poi = time.time()
    file_path = Path(PATH["data"]) / placeid / f"{placeid}_poi_{poi_source}_nnidscarall.csv"
    with open(file_path) as f:
        nnids = [int(line.rstrip()) for line in f]
    end_time_poi = time.time()
    poi_loading_duration = end_time_poi - start_time_poi

    # Load results
    start_time_load_results = time.time()
    filename = f"{placeid}_poi_{poi_source}_{prune_measure}.pickle"
    resultfile_path = PATH["results"] / placeid / filename
    with open(resultfile_path, 'rb') as resultfile:
        res = pickle.load(resultfile)
    end_time_load_results = time.time()
    result_loading_duration = end_time_load_results - start_time_load_results

    # Calculate metrics
    start_time_metrics = time.time()
    output, covs = calculate_metrics_additively(
        res["GTs"], res["GT_abstracts"], res["prune_quantiles"], G_carall, nnids,
        buffer_walk, numnodepairs, debug, True, Gexisting
    )
    output_MST, cov_MST = calculate_metrics(
        res["MST"], res["MST_abstract"], G_carall, nnids, output,
        buffer_walk, numnodepairs, debug, True, ig.Graph(), Polygon(), False, Gexisting
    )
    end_time_metrics = time.time()
    metrics_calculation_duration = end_time_metrics - start_time_metrics

    # Save the covers
    start_time_save_covers = time.time()
    write_result(covs, "pickle", placeid, poi_source, prune_measure, "_covers.pickle")
    write_result(cov_MST, "pickle", placeid, poi_source, prune_measure, "_cover_mst.pickle")
    end_time_save_covers = time.time()
    covers_saving_duration = end_time_save_covers - start_time_save_covers

    # Write to CSV
    start_time_csv = time.time()
    write_result(output, "dict", placeid, poi_source, prune_measure, ".csv")
    write_result(output_MST, "dict", placeid, poi_source, "", "mst.csv")
    end_time_csv = time.time()
    csv_writing_duration = end_time_csv - start_time_csv

    # End total timing
    end_time_total = time.time()
    total_duration = end_time_total - start_time_total

    # Append timing data
    timing_data.append([placeid, "Network Loading", network_loading_duration])
    timing_data.append([placeid, "POI Loading", poi_loading_duration])
    timing_data.append([placeid, "Results Loading", result_loading_duration])
    timing_data.append([placeid, "Metrics Calculation", metrics_calculation_duration])
    timing_data.append([placeid, "Saving Covers", covers_saving_duration])
    timing_data.append([placeid, "CSV Writing", csv_writing_duration])
    timing_data.append([placeid, "Total Process Time", total_duration])
    
with open(timing_file, mode='w', newline='') as file:
writer = csv.writer(file)
writer.writerow(["PlaceID", "Process", "Time (seconds)"])  # CSV header
writer.writerows(timing_data)