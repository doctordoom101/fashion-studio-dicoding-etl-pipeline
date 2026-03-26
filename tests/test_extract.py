import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.extract import scrape_data

class TestExtract(unittest.TestCase):
    @patch('requests.get')
    def test_scrape_data_success(self, mock_get):
        # Simulasi HTML sederhana
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
            <div class="product-item">
                <h5 class="product-title">T-Shirt Blue</h5>
                <span class="price">$10</span>
                <p class="rating">4.5 / 5</p>
                <p class="colors">2 Colors</p>
                <p class="size">Size: L</p>
                <p class="gender">Gender: Men</p>
            </div>
        '''
        mock_get.return_value = mock_response

        # Kita batasi loop hanya 1 kali untuk keperluan testing (mocking loop)
        with patch('utils.extract.range', return_value=[1]):
            df = scrape_data()
            
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]['Title'], 'T-Shirt Blue')
        self.assertIn('timestamp', df.columns)

    @patch('requests.get')
    def test_scrape_data_error(self, mock_get):
        # Simulasi kegagalan koneksi
        mock_get.side_effect = Exception("Connection Error")
        df = scrape_data()
        self.assertTrue(df.empty)

if __name__ == '__main__':
    unittest.main()
