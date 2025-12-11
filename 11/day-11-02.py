import sys
import networkx as nx


def main():
    G = nx.DiGraph()
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            device_from, devices_to = line.split(":")
            device_from = device_from.strip()
            devices_to = devices_to.strip().split(" ")
            for device_to in devices_to:
                G.add_edges_from([(device_from, device_to)])

    result = None
    paths_fft_dac = list(nx.all_simple_paths(G, source="fft", target="dac"))
    if len(paths_fft_dac) > 0:
        paths_svr_fft = list(nx.all_simple_paths(G, source="svr", target="fft"))
        assert len(paths_svr_fft) > 0
        paths_dac_out = list(nx.all_simple_paths(G, source="dac", target="out"))
        assert len(paths_dac_out) > 0
        result = len(paths_svr_fft) * len(paths_fft_dac) * len(paths_dac_out)
    else:
        paths_dac_fft = list(nx.all_simple_paths(G, source="dac", target="fft"))
        assert len(paths_dac_fft) > 0
        paths_svr_dac = list(nx.all_simple_paths(G, source="svr", target="dac"))
        assert len(paths_svr_dac) > 0
        paths_fft_out = list(nx.all_simple_paths(G, source="fft", target="out"))
        assert len(paths_fft_out) > 0
        result = len(paths_svr_dac) * len(paths_dac_fft) * len(paths_fft_out)
    assert result is not None
    print(result)


if __name__ == "__main__":
    main()
