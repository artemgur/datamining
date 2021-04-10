from matrix import Matrix
import page_rank
import networkx
import matplotlib.pyplot


def __get_edges_list(transition_matrix: Matrix) -> list[(str, str)]:
    print('Started generating edges list')
    result = []
    for r in range(transition_matrix.rows):
        for c in range(transition_matrix.columns):
            if transition_matrix[r][c] != 0:
                result.append((c, r))
    print('Finished generating edges list')
    return result


def run():
    data = page_rank.build_transition_matrix()
    transition_matrix = data[0]
    page_rank.write_unique_links_to_database(data[1])
    edges = __get_edges_list(transition_matrix)
    graph = networkx.DiGraph(directed=True)
    print('Adding nodes')
    graph.add_nodes_from(range(1, transition_matrix.rows))
    print('Adding edges')
    graph.add_edges_from(edges)
    print('Drawing graph')
    matplotlib.pyplot.figure(1, figsize=(100,100))
    networkx.draw(graph, arrows=True, node_size = 10, font_size = 6, with_labels=True)
    # matplotlib.pyplot.show()
    print('Saving file')
    matplotlib.pyplot.savefig("Graph.png", format="PNG")
    print('Finished!')
