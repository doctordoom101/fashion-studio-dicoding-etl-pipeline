import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from utils.load import save_to_csv, save_to_postgres, load_all


class TestLoad(unittest.TestCase):

    # =========================
    # TEST CSV
    # =========================
    def test_save_to_csv_success(self):
        df = pd.DataFrame({'test': [1, 2, 3]})

        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            save_to_csv(df, "dummy.csv")
            mock_to_csv.assert_called_once_with("dummy.csv", index=False)

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv_error(self, mock_to_csv):
        mock_to_csv.side_effect = Exception("Permission Denied")
        df = pd.DataFrame({'test': [1]})

        # Tidak boleh crash
        try:
            save_to_csv(df, "locked.csv")
        except Exception as e:
            self.fail(f"save_to_csv raised {e} unexpectedly!")

    # =========================
    # TEST POSTGRES
    # =========================
    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_save_to_postgres_success(self, mock_to_sql, mock_engine):
        df = pd.DataFrame({'test': [1]})

        mock_engine.return_value = MagicMock()

        save_to_postgres(df, "products")

        mock_engine.assert_called_once()
        mock_to_sql.assert_called_once()

    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_save_to_postgres_error(self, mock_to_sql, mock_engine):
        df = pd.DataFrame({'test': [1]})

        mock_engine.return_value = MagicMock()
        mock_to_sql.side_effect = Exception("DB Error")

        # Tidak boleh crash
        try:
            save_to_postgres(df, "products")
        except Exception as e:
            self.fail(f"save_to_postgres raised {e} unexpectedly!")

    # =========================
    # TEST ORCHESTRATOR
    # =========================
    @patch('utils.load.save_to_csv')
    @patch('utils.load.save_to_postgres')
    def test_load_all_success(self, mock_postgres, mock_csv):
        df = pd.DataFrame({'test': [1]})

        load_all(df)

        mock_csv.assert_called_once()
        mock_postgres.assert_called_once()

    @patch('utils.load.save_to_csv')
    @patch('utils.load.save_to_postgres')
    def test_load_all_empty_df(self, mock_postgres, mock_csv):
        df = pd.DataFrame()

        load_all(df)

        # Tidak boleh dipanggil kalau kosong
        mock_csv.assert_not_called()
        mock_postgres.assert_not_called()


if __name__ == '__main__':
    unittest.main()