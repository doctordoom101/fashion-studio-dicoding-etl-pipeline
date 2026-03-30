import unittest
import pandas as pd
from utils.transform import clean_data


class TestTransform(unittest.TestCase):

    def setUp(self):
        self.raw_data = pd.DataFrame({
            'Title': ['Jacket A', 'Unknown Product', 'Jacket A'],
            'Price': ['$10.00', '$20.00', '$10.00'],
            'Rating': ['Rating: ⭐ 4.0 / 5', 'Rating: ⭐ Invalid Rating / 5', 'Rating: ⭐ 4.0 / 5'],
            'Colors': ['3 Colors', '1 Colors', '3 Colors'],
            'Size': ['M', 'L', 'M'],
            'Gender': ['Women', 'Men', 'Women']
        })

    def test_clean_data_logic(self):
        df_cleaned = clean_data(self.raw_data)

        self.assertNotIn('Unknown Product', df_cleaned['Title'].values)

        self.assertEqual(len(df_cleaned), 1)

        row = df_cleaned.iloc[0]

        self.assertEqual(row['Price'], 160000)

        self.assertEqual(row['Rating'], 4.0)

        self.assertEqual(row['Colors'], 3)

        self.assertEqual(row['Size'], 'M')
        self.assertEqual(row['Gender'], 'Women')

    def test_handle_invalid_rating(self):
        df_cleaned = clean_data(self.raw_data)

        self.assertTrue(df_cleaned['Rating'].notna().all())

    def test_clean_data_empty(self):
        df_empty = pd.DataFrame()
        result = clean_data(df_empty)
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()