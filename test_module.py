import unittest
from static.get_skaitvardis import get_number_complex_name, Stress
from static.get_zodis import get_complex_name

#tūkstantis vienas šimtas penkiasdešimt penktųjų metų kovo  septynioliktosios diena

class TastDate(unittest.TestCase):
    def test_date(self):
        stress=Stress.No

        word_name = get_complex_name(
            value='metai', category_type='All',
            number='dgs', case='kilm.', stress=stress
        )

        self.assertEqual(word_name, 'metų')

        m = get_complex_name(
            value=2, category_type="Month",
            number='vns', case='kilm.', stress=stress)

        self.assertEqual(m, 'kovo')

        word_name = get_complex_name(
            value='diena', category_type='All',
            number='vns', case='kilm.', stress=stress
        )

        self.assertEqual(word_name, 'dienos')

class TestGetZodis(unittest.TestCase):
    def _get_complex_name_(self, param):
        val, cat_type, case, number, stress = param

        return get_complex_name(
            value=val, category_type=cat_type,
            case=case, number=number,
            stress=stress)

    def test_month(self):
        test_data = [
            ((0, "Month", "kilm.", 'dgs', Stress.ASCII), 'sau~sių'),  
            ((1, "Month", "kilm.", 'dgs', Stress.ASCII), 'vasa~rių'),       
        ]

        for param, name in test_data:
            name_ = self._get_complex_name_(param)
            self.assertEqual(name_, name)

    def test_all(self):
        test_data = [
            (('diena', "All", "kilm.", "dgs", Stress.ASCII), 'dienų~'),  
            (('laipsnis', "All", "kilm.", "dgs", Stress.ASCII), 'la^ipsnių'),       
        ]

        for param, name in test_data:
            name_ = self._get_complex_name_(param)
            self.assertEqual(name_, name)

if __name__ == '__main__':
    unittest.main()