import unittest
from static.get_zodis import get_complex_name, Stress

class TestGetZodis(unittest.TestCase):
    def _test_batch(self, test_data, default_params={}):
        for params, name in test_data:
            name_ = get_complex_name(**{**default_params, **params})
            self.assertEqual(name_, name)

    def test_month(self):
        params = {
            'category_type': 'Month',
            'case': 'kilm.',
            'number': 'dgs',
            'stress': Stress.ASCII
        }

        test_data = [
            ({'value': 0}, 'sau~sių'),  
            ({'value': 1}, 'vasa~rių'),       
        ]

        self._test_batch(test_data, params)

    def test_all(self):
        params = {
            'category_type': 'All',
            'case': 'kilm.',
            'number': 'dgs',
            'stress': Stress.ASCII
        }
        
        test_data = [
            ({'value': 'diena'}, 'dienų~'),  
            ({'value': 'laipsnis'}, 'la^ipsnių'),       
        ]

        self._test_batch(test_data, params)

if __name__ == '__main__':
    unittest.main()