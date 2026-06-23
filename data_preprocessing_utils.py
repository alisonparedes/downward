# To support training a heuristic

def boolean_expansion(state: list[int], domain_sizes: dict[int, int]) -> list[int]:
    """
    Expands a SAS+ integer state vector into a boolean representation.
    
    Args:
        state:        e.g. [0, 0, 4, 2, 1, 1, 1]
        domain_sizes: e.g. {0: 2, 1: 5, 2: 5, 3: 3, 4: 3, 5: 3, 6: 3}
    
    Returns:
        A flat boolean list of length sum(domain_sizes.values())
    """
    result = []
    for var_idx, val in enumerate(state):
        domain_size = domain_sizes[var_idx]
        result.extend([1 if i == val else 0 for i in range(domain_size)])
    return result

def parse_output_dot_sas_file(output_dot_sas_file: str) -> list[dict]:
    """
    Parses variable names and domain sizes from an output.sas file.
    Returns a list of dicts with 'name', 'domain_size', and 'values'.
    """
    variables = []
    with open(output_dot_sas_file) as f:
        lines = [line.strip() for line in f]

    i = 0
    while i < len(lines):
        if lines[i] == "begin_variable":
            name = lines[i + 1]
            domain_size = int(lines[i + 3])
            values = [lines[i + 4 + j] for j in range(domain_size)]
            variables.append({
                "name": name,
                "domain_size": domain_size,
                "values": values,
            })
            i += 4 + domain_size + 1  # skip to end_variable
        else:
            i += 1

    return variables