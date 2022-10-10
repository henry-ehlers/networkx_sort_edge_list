import itertools as it


def unlist(nested_list: [[]]) -> []:
    """
    A function which transforms a nested list into a list of a single level, for example a list of lists
    [[a, c], [d, b], [b, e]] would be transformed to a list of [a, c, d, b, b, e]
    :param nested_list: a nested list of iterables
    :return: a list of depth -= 1
    """

    # Return an un-nested list
    return list(it.chain.from_iterable(nested_list))


def get_valid_starting_vertex(edges: [(int, int)], starting_vertex: int = None) -> int:
    """
    A function to either obtain a valid starting vertex from a list of edges, or ensure the provided starting vertex is
    indeed a valid choice, i.e. that the provided list of edges is either a cycle of edges or a sequence with two
    defined end-points
    :param edges: a list of (unsorted) edges as tuples to be sorted
    :param starting_vertex: an optional single integer vertex at which to start the sorting
    :return: the integer identifier of the starting vertex
    """

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
    assert (len(ends) == 2) or (len(cycles) == len(vertex_counts)), \
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


def get_first_edge(edges: [(int, int)], starting_vertex: int) -> (int, int):
    """
    A function which returns an edge which features the provided starting vertex in its first position
    :param edges: a list of (unsorted) edges as tuples to be sorted
    :param starting_vertex: an optional single integer vertex at which to start the sorting
    :return: a sorted list of edges
    """

    # Iterate over all edges in set
    for edge in edges:

        # Check whether first vertex of edge is the starting vertex
        if edge[0] == starting_vertex:
            return edge

        # Check whether second vertex of edge is the starting vertex
        elif edge[1] == starting_vertex:
            return edge[1], edge[0]

    # Provided starting vertex Mapped to no edge
    assert True, f"Starting Vertex {starting_vertex} mapped to no edge {edges}"


def get_ordered_edges(edges: [(int, int)], starting_vertex: int = None) -> [(int, int)]:
    """
    A function to sort a list of edges provided as tuples, such that the second vertex of an edge corresponds to the
    first vertex of the next edge, i.e. (a, c) (c, b) (b, a)
    :param edges: a list of (unsorted) edges as tuples to be sorted
    :param starting_vertex: an optional single integer vertex at which to start the sorting
    :return: a sorted list of edges
    """

    # Get a valid starting vertex / Ensure the provided one is valid
    starting_vertex = get_valid_starting_vertex(edges, starting_vertex)

    # Convert list of tuples to list of frozen-sets
    remaining_edges = [frozenset(edge) for edge in edges]

    # Obtain an edge which features the starting vertex
    first_edge = get_first_edge(edges, starting_vertex)

    # Initialize the list of sorted edges, and remove first one from the remaining set
    sorted_edges = [first_edge] + [(None, None)] * (len(edges) - 1)
    remaining_edges.remove(frozenset(first_edge))

    # Iterate over each remaining index to be sorted
    for i in range(1, len(sorted_edges)):

        # Iterate over all remaining edges to be included
        for edge_set in remaining_edges:

            # Convert Set Edge to forward and 'reversed' edge
            f_edge = tuple(edge_set)
            r_edge = f_edge[::-1]

            # Check whether the forward facing edge matches the last sorted edge
            if f_edge[0] == sorted_edges[i - 1][1]:
                sorted_edges[i] = f_edge
                remaining_edges.remove(frozenset(f_edge))
                break

            # Check whether the 'reversed' facing edge matches the last sorted edge
            elif r_edge[0] == sorted_edges[i - 1][1]:
                sorted_edges[i] = r_edge
                remaining_edges.remove(frozenset(r_edge))
                break

    # Ensure no edges remain to be sorted
    assert len(remaining_edges) == 0, \
        f"Not all edges sorted. These remain: {sorted_edges}"

    # Return sorted edges as list of tuples
    return sorted_edges


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    edge_list_sequence = [(1, 2), (5, 2), (1, 0), (5, 4)]
    edge_list_cyclical = [(1, 2), (5, 2), (1, 0), (5, 0)]
    edge_list_illegals = [(1, 2), (5, 2), (1, 0), (5, 1)]

    print(f"Sorted Sequence: {get_ordered_edges(edge_list_sequence)}")
    print(f"Sorted Sequence with starting vertex {4}: {get_ordered_edges(edge_list_sequence, 4)}")
    print(f"Sorted Cycle: {get_ordered_edges(edge_list_cyclical)}")
    print(f"Sorted Cycle with starting vertex {5}: {get_ordered_edges(edge_list_cyclical, 5)}")
