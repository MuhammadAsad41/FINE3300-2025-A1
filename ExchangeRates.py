#Question 2: Currency Conversion & Exchange Rate 
#Importing Pandas for File Interpretation
import pandas as pd
from pathlib import Path

#Exchange Rate Class 
class ExchangeRates:
    """
    Read Bank of Canada exchange-rate table (CSV or Excel),
    finds the latest USD/CAD from the last row, and converts USD to CAD & vice versa.
    """
    #These various mitigations are being used to ensure that file is read since initially Python was not able to detect file on my Mac.

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        self.df = self._load_table(self.path)
        if self.df.empty:
            raise ValueError("The file appears to be empty.")
        
        # Normalize headers
        self.df.columns = [str(c).strip() for c in self.df.columns]

        # Finding USD/CAD or CAD/USD
        self.usd_cad_col = self._find_pair_column(self.df.columns, "USD", "CAD")
        self.cad_usd_col = self._find_pair_column(self.df.columns, "CAD", "USD")

        if self.usd_cad_col is None and self.cad_usd_col is None:
            raise KeyError("Could not find USD/CAD or CAD/USD column in the file.")

        # Latest Rate = Last Row
        last_row = self.df.iloc[-1]
        if self.usd_cad_col is not None:
            self.latest_usd_cad = float(last_row[self.usd_cad_col])
        else:
            cad_usd = float(last_row[self.cad_usd_col])
            if cad_usd == 0:
                raise ValueError("CAD/USD latest value is zero; cannot invert.")
            self.latest_usd_cad = 1.0 / cad_usd

        if not (self.latest_usd_cad > 0):
            raise ValueError(f"Invalid latest USD/CAD rate: {self.latest_usd_cad}")

    @staticmethod
    def _load_table(path: Path) -> pd.DataFrame:
        """Read Excel or CSV (tolerant to encodings)."""
        if path.suffix.lower() in (".xlsx", ".xls"):
            # requires: pip install openpyxl
            return pd.read_excel(path, engine="openpyxl")

        # CSV path
        for enc in ("utf-8-sig", "utf-8"):
            try:
                return pd.read_csv(path, encoding=enc, engine="python", on_bad_lines="skip")
            except Exception:
                continue
        raise RuntimeError("Could not read file as CSV or Excel. Re-export as UTF-8 CSV or .xlsx.")

    @staticmethod
    def _find_pair_column(columns, base: str, quote: str) -> str | None:
        """Locate a header like 'USD/CAD'"""
        preferred = {
            f"{base}/{quote}",
        }
        for c in columns:
            if str(c).strip() in preferred:
                return c
        # heuristic
        for c in columns:
            low = str(c).lower().replace(" ", "")
            if base.lower() in low and quote.lower() in low:
                return c
        return None

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert between USD and CAD using the latest USD/CAD rate."""
        from_currency, to_currency = from_currency.strip().upper(), to_currency.strip().upper()
        if from_currency == to_currency:
            return float(amount)
        if {from_currency, to_currency} != {"USD", "CAD"}:
            raise ValueError("Only USD and CAD are supported.")
        rate = self.latest_usd_cad  # USD/CAD
        return float(amount) * rate if (from_currency, to_currency) == ("USD", "CAD") else float(amount) / rate


def main():
    # Autopick whichever file is present in the same folder. This is done because my Mac was having problems with file storage & interpretation. 
    candidates = ["BankOfCanadaExchangeRates.xlsx", "BankOfCanadaExchangeRates.csv"]
    existing = next((c for c in candidates if Path(c).exists()), None)
    if not existing:
        print("Files in this folder:", [p.name for p in Path('.').iterdir()])
        raise FileNotFoundError(
            "Place BankOfCanadaExchangeRates.xlsx or BankOfCanadaExchangeRates.csv "
            "in the same folder." )

    xr = ExchangeRates(existing)
    print(f"\nLatest USD/CAD rate (from last row): {xr.latest_usd_cad:.6f}\n")

    # Input Collection for Conversion
    amount = float(input("Enter the amount you would like to convert: ").strip())
    from_cur = input("What currency are you converting from? (USD or CAD): ").strip()
    to_cur = input("And what currency are you converting to? (USD or CAD): ").strip()


    #Gives Output to User with a thank you note.
    result = xr.convert(amount, from_cur, to_cur)
    print(f"\n{amount:.2f} {from_cur.upper()} = {result:.2f} {to_cur.upper()}\n")
    print("Thank you for using the Currency Conversion Tool!")
    
if __name__ == "__main__":
    main()




