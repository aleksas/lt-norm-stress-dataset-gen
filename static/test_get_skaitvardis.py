import unittest
from static.get_skaitvardis import get_number_complex_name, Stress

class TestGetSkaitvardis(unittest.TestCase):
    def _test_batch(self, test_data, default_params={}):
        for params, name in test_data:
            name_, _ = get_number_complex_name(**{**default_params, **params})
            self.assertEqual(name_, name)

    def test_complex_names(self):
        pairs = [
            (267500, "du šimtai šešiasdešimt septyni tūkstančiai penki šimtai")
        ]

        for value, name in pairs:
            name_, _ = get_number_complex_name(value=value, stress=Stress.No)
            self.assertEqual(name, name_)

    def test_stressed_complex_names(self):
        pairs = [
            (267500, "du` šimtai~ še~šiasdešimt septyni` tū^kstančiai penki` šimtai~")
        ]

        for value, name in pairs:
            name_, _ = get_number_complex_name(value=value, stress=Stress.ASCII)
            self.assertEqual(name, name_)

    def test_kiekiniai(self):
        params = {
            'category_type': 'Kiekiniai',
            'category_subtype': 'Pagrindiniai',
            'gender': 'mot. g.',
            'stress': Stress.No
        }

        test_data = [
            ({'value':6349000, 'number': None, 'case': 'kilm.'}, 'šešių milijonų trijų šimtų keturiasdešimt devynių tūkstančių'),
            ({'value':6349000, 'number':"vns", 'case':'vard.'}, 'šeši milijonai trys šimtai keturiasdešimt devyni tūkstančiai'),
            ({'value':21, 'number':'dgs', 'case':'kilm.'}, 'dvidešimt vienų'),
        ]        

        self._test_batch(test_data, params)

    def test_kelintiniai_ivardziuotiniai(self):
        params = {
            'category_type': 'Kelintiniai',
            'category_subtype': 'Įvardžiuotiniai',
            'gender': 'mot. g.',
            'case': 'kilm.',
            'number': 'vns',
            'stress': Stress.No
        }

        test_data = [
            ({'value': 6349000}, 'šeši milijonai trys šimtai keturiasdešimt devynių tūkstantosios'),
            ({'value': 100000}, 'šimtas tūkstantosios'),
            ({'value': 1155, 'number': 'dgs'}, 'tūkstantis šimtas penkiasdešimt penktųjų'),
            ({'value': 17}, 'septynioliktosios'),
        ]

        self._test_batch(test_data, params)

    def test_kelintiniai_neivardziuotiniai(self):
        params = {
            'category_type': 'Kelintiniai',
            'category_subtype': 'Neįvardžiuotiniai',
            'gender': 'mot. g.',
            'case': 'kilm.',
            'number': 'vns',
            'stress': Stress.No
        }

        test_data = [
            ({'value': 21}, 'dvidešimt pirmos'),
            ({'value': 17}, 'septynioliktos'),
        ]

        self._test_batch(test_data, params)

if __name__ == '__main__':
    unittest.main()