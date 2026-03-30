import unittest
import pandas as pd
from utils.transform import clean_data


class TestTransform(unittest.TestCase):

    def setUp(self):
        # ✅ Disesuaikan dengan output hasil extract terbaru
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

        # ✅ Unknown Product harus hilang
        self.assertNotIn('Unknown Product', df_cleaned['Title'].values)

        # ✅ Duplicate harus hilang → tinggal 1 row valid
        self.assertEqual(len(df_cleaned), 1)

        row = df_cleaned.iloc[0]

        # ✅ Price harus sudah numeric (USD → IDR, asumsi 1$ = 16000)
        self.assertEqual(row['Price'], 160000)

        # ✅ Rating harus sudah float
        self.assertEqual(row['Rating'], 4.0)

        # ✅ Colors harus integer
        self.assertEqual(row['Colors'], 3)

        # ✅ Size & Gender sudah clean (tanpa prefix)
        self.assertEqual(row['Size'], 'M')
        self.assertEqual(row['Gender'], 'Women')

    def test_handle_invalid_rating(self):
        df_cleaned = clean_data(self.raw_data)

        # Pastikan tidak ada rating invalid tersisa
        self.assertTrue(df_cleaned['Rating'].notna().all())

    def test_clean_data_empty(self):
        df_empty = pd.DataFrame()
        result = clean_data(df_empty)
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()