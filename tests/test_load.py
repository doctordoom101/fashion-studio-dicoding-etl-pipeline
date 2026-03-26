import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv

class TestLoad(unittest.TestCase):
    def test_save_to_csv_success(self):
        df = pd.DataFrame({'test': [1, 2, 3]})
        
        # Mocking fungsi to_csv milik pandas
        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            save_to_csv(df, "dummy.csv")
            mock_to_csv.assert_called_once_with("dummy.csv", index=False)

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv_error(self, mock_to_csv):
        # Simulasi error saat menulis file (misal permission denied)
        mock_to_csv.side_effect = Exception("Permission Denied")
        df = pd.DataFrame({'test': [1]})
        
        # Pastikan tidak crash saat error (karena ada try-except di load.py)
        try:
            save_to_csv(df, "locked_file.csv")
        except Exception as e:
            self.fail(f"save_to_csv raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
