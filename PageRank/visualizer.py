from matrix import Matrix
import page_rank
import networkx
import matplotlib.pyplot


def __get_edges_list(transition_matrix: Matrix, unique_links: list[str]) -> list[(str, str)]:
    print('Started generating edges list')
    result = []
    for r in range(transition_matrix.rows):
        for c in range(transition_matrix.columns):
            if transition_matrix[r][c] != 0:
                result.append((unique_links[c], unique_links[r]))
    print('Finished generating edges list')
    return result


def run():
    data = page_rank.build_transition_matrix()
    transition_matrix = data[0]
    unique_links = data[1]
    edges = __get_edges_list(transition_matrix, unique_links)
    graph = networkx.Graph()
    print('Adding nodes')
    graph.add_nodes_from(unique_links)
    print('Adding edges')
    graph.add_edges_from(edges)
    matplotlib.pyplot.figure(1, figsize=(100,100))
    networkx.draw(graph, node_size = 6, font_size = 4)
    # matplotlib.pyplot.show()
    print('Saving file')
    matplotlib.pyplot.savefig("Graph.png", format="PNG")
    print('Finished!')
