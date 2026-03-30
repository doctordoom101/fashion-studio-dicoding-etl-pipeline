import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.extract import scrape_data


class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')  
    def test_scrape_data_success(self, mock_get):
        # ✅ HTML disesuaikan dengan struktur terbaru
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">T-Shirt Blue</h3>
                    <div class="price-container">
                        <span class="price">$10</span>
                    </div>
                    <p>Rating: ⭐ 4.5 / 5</p>
                    <p>2 Colors</p>
                    <p>Size: L</p>
                    <p>Gender: Men</p>
                </div>
            </div>
        '''
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with patch('utils.extract.range', return_value=[1]):
            df = scrape_data()

        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]['Title'], 'T-Shirt Blue')
        self.assertEqual(df.iloc[0]['Price'], '$10')
        self.assertIn('Rating', df.columns)
        self.assertIn('timestamp', df.columns)

    @patch('utils.extract.requests.get')
    def test_scrape_data_404(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with patch('utils.extract.range', return_value=[1]):
            df = scrape_data()

        self.assertTrue(df.empty)

    @patch('utils.extract.requests.get')
    def test_scrape_data_error(self, mock_get):
        mock_get.side_effect = Exception("Connection Error")

        df = scrape_data()
        self.assertTrue(df.empty)


if __name__ == '__main__':
    unittest.main()