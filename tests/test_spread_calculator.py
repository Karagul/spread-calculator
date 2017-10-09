"""These are the tests for module spread calculator"""
import unittest
import sys
sys.path.append("spread-calculator")
from spread_calculator import Bond,create_adjacent_government_bonds_map, find_benchmark_bond,calculate_spread_to_curve

c1 = Bond("C1", "corporate", "10.3 year", "5.30%")
c2 = Bond("C2", "corporate", "15.2 year", "8.30%")
g1 = Bond("G1", "government", "9.4 year", "3.70%")
g2 = Bond("G2", "government", "12 year", "4.80%")
g3 = Bond("G3", "government", "16.3 year", "5.50%")

bonds = [c1, c2, g1, g2, g3]
adjacent_map = {c1: [g1, g2], c2: [g2, g3]}


class TestSpreadCalculator(unittest.TestCase):
    def test_create_adjacent_map(self):
        """
        test the function create_adjacent_map  in spread_calculator
        """
        created_map = create_adjacent_government_bonds_map(bonds)
        self.assertDictEqual(created_map, adjacent_map)

    def test_find_benchmark_bond(self):
        """
        test the function find_benchmark_bond in spread_calculator
        """
        found_bonds = sorted(find_benchmark_bond(adjacent_map))

        return self.assertListEqual(found_bonds, sorted([['C2', 'G3', '2.8%'], ['C1', 'G1', '1.6%']]))

    def test_calculate_spread_to_curve(self):
        """
        test the function calculate_spread_to_curve in spread_calculator
        """
        found_bonds = calculate_spread_to_curve(adjacent_map)

        return self.assertListEqual(found_bonds, [['C1', '1.22%'], ['C2', '2.98%']])


if __name__ == '__main__':
    unittest.main()
