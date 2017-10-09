import argparse
import csv
import re


class Bond:
    def __init__(self, name, category, term, return_yield):
        self.name = name
        self.category = category
        self.term = float(re.search('([0-9\.]+)', term).group())
        self.return_yield = float(re.search('([0-9\.]+)', return_yield).group())

    def __lt__(self, other):
        return self.term < other.term


def read_bonds_from_csv(input_file):
    """
    read bond information from a csv file
    :param input_file: path to input csv file
    :return: a list of bonds
    """
    with open(input_file, 'rU') as file:
        reader = csv.reader(file)
        next(reader, None)
        bonds = []
        for item in reader:
            bond = Bond(item[0], item[1], item[2], item[3])
            bonds.append(bond)
        return bonds


def create_adjacent_government_bonds_map(bonds):
    """
    find the adjacent government bonds to every corporate bonds based on length of bond, return the map
    :param bonds: all bonds including government bonds and corporate bonds
    :return: return the map stored the adjacent government bonds to each corporate bond
    """
    adjacent_map = {}
    sorted_bonds = bonds
    sorted_bonds.sort()
    before_g = None
    after_g = None

    for bond in sorted_bonds:
        if bond.category == "government":
            before_g = bond
        else:
            adjacent_map[bond] = [before_g]

    for bond in reversed(sorted_bonds):
        if bond.category == "government":
            after_g = bond
        else:
            new_value = adjacent_map[bond]
            new_value.append(after_g)
            adjacent_map[bond] = new_value

    return adjacent_map


def find_benchmark_bond(adjacent_map):
    """
    find government benchmark bond for each corporate bonds based on length of bond
    :param adjacent_map: corporate bonds adjacent government bonds map
    :return: benchmark bond for each corporate bond
    """
    result = []
    for key, value in adjacent_map.iteritems():
        if abs(value[0].term - key.term) > abs(value[1].term - key.term):
            benchmark = value[1]
        else:
            benchmark = value[0]

        result.append([key.name, benchmark.name, str(key.return_yield - benchmark.return_yield) + "%"])

    return result


def calculate_spread_to_curve(adjacent_map):
    """
    calculate spread to curve using government benchmark bond for each corporate bonds based on linear interpolation
    :param adjacent_map: corporate bonds adjacent government bonds map
    :return: spread to curve for each corporate bond
    """
    result = []
    for key, value in adjacent_map.iteritems():
        term_diff = value[1].term - value[0].term
        spread = (value[0].return_yield * (value[1].term - key.term) +
                  value[1].return_yield * (key.term - value[0].term)) / term_diff

        result.append([key.name, str(round(key.return_yield - spread, 2)) + "%"])

    return result


def main(args):
    """
    To calculate spread based on the arguments and save in csv file
    :param args: passed in arguments
    :return:
    """
    bonds = read_bonds_from_csv(args.input_file)
    adjacent_map = create_adjacent_government_bonds_map(bonds)
    with open(args.output_file, 'wb') as file:
        writer = csv.writer(file)
        if args.find_benchmark_bonds:
            result = find_benchmark_bond(adjacent_map)
            writer.writerow(['bond', 'benchmark', 'spread_to_benchmark'])
            for row in result:
                writer.writerow(row)
        if args.calculate_spread_to_curve:
            result = calculate_spread_to_curve(adjacent_map)
            writer.writerow(['bond', 'spread_to_curve'])
            for row in result:
                writer.writerow(row)
    return args


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str,
                        help='path to bond information input file', required=True)
    parser.add_argument('--output_file', type=str,
                        help='path to file where will store the output', required=True)
    parser.add_argument('--find_benchmark_bonds', type=bool,
                        help='whether want to calculate the benchmark bonds or not', required=True)
    parser.add_argument('--calculate_spread_to_curve', type=bool,
                        help="whether want to calculate the spread to curve or not", required=True)

    args = parser.parse_args()
    main(args)
