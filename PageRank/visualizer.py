from matrix import Matrix
import page_rank
import networkx
import matplotlib.pyplot


def __get_edges_list(transition_matrix: Matrix, unique_links: list[str]) -> list[(str, str)]:
    result = []
    for r in range(transition_matrix.rows):
        for c in range(transition_matrix.columns):
            if transition_matrix[r][c] != 0:
                result.append((unique_links[c], unique_links[r]))
    return result


def run():
    data = page_rank.build_transition_matrix()
    transition_matrix = data[0]
    unique_links = data[1]
    edges = __get_edges_list(transition_matrix, unique_links)
    graph = networkx.Graph()
    graph.add_nodes_from(unique_links)
    graph.add_edges_from(edges)
    networkx.draw(graph)
    matplotlib.pyplot.show()
