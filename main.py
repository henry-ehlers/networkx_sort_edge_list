import itertools as it

def unlist(nested_list):
    return list(it.chain.from_iterable(nested_list))


def has_unique_order(edges, starting_vertex=None):

    # Extract a list of vertices from the list of edges
    vertices = unlist(edges)

    # If a starting vertex is provided, ensure it actually exists in the vertex list
    if starting_vertex is not None:
        assert starting_vertex in vertices, \
            f"Providing starting vertex {starting_vertex} is not in edge's vertex set {vertices}."

    # Count the number of occurences of each vertex in the list of vertices
    vertex_counts = {vertex: 0 for vertex in list(set(vertices))}
    for vertex in vertices:
        vertex_counts[vertex] += 1

    # Count the number of "knots" and "forks" in the edge sequence
    forks = [node for node, count in vertex_counts.items() if count > 2]
    assert len(forks) == 0, \
        f"Edge Sequence has no unique order, as nodes {forks} are featured more than twice."

    # Count the number of ends in the sequence is only 2, or all vertices must appear exactly twice
    ends = [node for node, count in vertex_counts.items() if count == 1]
    cycles = [node for node, count in vertex_counts.items() if count == 2]
    assert (len(ends) == 2) or (len(cycles) == len(vertex_counts)),\
        f"Edge sequence has too many or too few end vertices, as nodes {ends} all only appear once, or the number" \
        f"of double matched vertices, {len(cycles)} is not the length of the available nodes {len(vertex_counts)}"

    # If the starting vertex is provided, ensure that it corresponds to end point vertex
    if (starting_vertex is not None) and (len(ends) > 0):
        assert starting_vertex in ends, \
            f"Provided starting vertex {starting_vertex} not a valid selection from end points {ends}."

    # Return a starting vertex if it was provided and is legal
    if starting_vertex is not None:
        return starting_vertex

    # If a legal sequence of edges was provided, return one of its end-points
    elif len(ends) > 0:
        return ends[0]

    # If a legal cycle was provided, return an (effectively) random vertex
    else:
        return vertices[0]


def get_ordered_edges(edges, starting_vertex=None):

    edges = [tuple(edge) for edge in edges]  # TODO: length differs for cycle vs sequence?

    #
    sorted_edges = [(None, None)] * len(edges)
    sorted_edges[0] = edges[0]
    visited_edges = [{edges[0]}]

    #
    for i in range(1, len(edges)):
        for edge in edges:
            if {edge} in visited_edges:
                continue
            if edge[0] == sorted_edges[i-1][1] and (edge[0], edge[1] not in sorted_edges):
                sorted_edges[i] = edge
                visited_edges.append({edge})
            elif edge[1] == sorted_edges[i-1][1] and (edge[1], edge[0] not in sorted_edges):
                sorted_edges[i] = (edge[1], edge[0])
                visited_edges.append({edge})

    #
    return sorted_edges


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    edge_list_sequence = [(1, 2), (5, 2), (1, 0), (5, 4)]
    edge_list_cyclical = [(1, 2), (5, 2), (1, 0), (5, 0)]
    edge_list_illegals = [(1, 2), (5, 2), (1, 0), (5, 1)]

    print(f"Sequence with no starting Vertex -> {has_unique_order(edge_list_sequence)}")
    print(f"Sequence with starting Vertex {4} -> {has_unique_order(edge_list_sequence, starting_vertex=4)}")
    print(f"Cycle with no starting vertex -> {has_unique_order(edge_list_cyclical)}")
    print(f"Cycle with starting vertex {5} -> {has_unique_order(edge_list_cyclical, starting_vertex=5)}")

    print(f"Sequence with illegal starting Vertex {1} -> {has_unique_order(edge_list_sequence, starting_vertex=1)}")
    # print(f"Cycle with illegal starting vertex {6} -> {has_unique_order(edge_list_cyclical, starting_vertex=6)}")
    #print(f"Illegal Edge Set with no starting vertex -> {has_unique_order(edge_list_illegals)}")
