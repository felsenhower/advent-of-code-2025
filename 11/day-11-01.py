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
    paths = list(nx.all_simple_paths(G, source="you", target="out"))
    print(len(paths))


if __name__ == "__main__":
    main()
