import unittest
import pandas as pd
from utils.transform import clean_data

class TestTransform(unittest.TestCase):
    def setUp(self):
        # Data dummy yang kotor
        self.raw_data = pd.DataFrame({
            'Title': ['Jacket A', 'Unknown Product', 'Jacket A'], # Ada duplikat & Unknown
            'Price': ['$10', '$20', '$10'],
            'Rating': ['4.0 / 5', 'Invalid', '4.0 / 5'],
            'Colors': ['3 Colors', '1 Colors', '3 Colors'],
            'Size': ['Size: M', 'Size: L', 'Size: M'],
            'Gender': ['Gender: Women', 'Gender: Men', 'Gender: Women']
        })

    def test_clean_data_logic(self):
        df_cleaned = clean_data(self.raw_data)
        
        # Cek apakah "Unknown Product" terhapus
        self.assertNotIn('Unknown Product', df_cleaned['Title'].values)
        
        # Cek apakah duplikat terhapus (dari 3 baris jadi 1 baris valid)
        self.assertEqual(len(df_cleaned), 1)
        
        # Cek konversi harga ($10 * 16000 = 160000)
        self.assertEqual(df_cleaned.iloc[0]['Price'], 160000)
        
        # Cek pembersihan string
        self.assertEqual(df_cleaned.iloc[0]['Colors'], 3)
        self.assertEqual(df_cleaned.iloc[0]['Size'], 'M')
        self.assertEqual(df_cleaned.iloc[0]['Gender'], 'Women')
        
    def test_clean_data_empty(self):
        df_empty = pd.DataFrame()
        result = clean_data(df_empty)
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
