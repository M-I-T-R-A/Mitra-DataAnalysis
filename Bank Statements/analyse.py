import tabula
import pandas as pd

def PdfToDf(pdf_path):
    dfs = tabula.read_pdf(pdf_path, stream=True, pages = 'all')
    # read_pdf returns list of DataFrames
    print(len(dfs))
    bank_data = pd.concat(dfs, ignore_index=True)
    bank_data = bank_data[bank_data["Transaction"] != "Date"]
    bank_data = bank_data.reset_index(drop=True)
    bank_data["Debit"] = bank_data["Debit"].str.replace(',', '').astype(float)
    bank_data["Credit"] = bank_data["Credit"].str.replace(',', '').astype(float)
    indexes = bank_data[~ bank_data['Transaction'].isnull()].index.tolist()
    merged_bank_data = pd.DataFrame(data=None, columns=bank_data.columns)
    for i in range(len(indexes)-1):
        description = ""
        curr = indexes[i]
        for j in range(curr,indexes[i+1]):
            if isinstance(bank_data.at[j, "Description"], str):
                description += bank_data.at[j, "Description"] + ' '
        merged_bank_data.loc[len(merged_bank_data.index)] = [bank_data.at[curr, "Transaction"], bank_data.at[curr, "Value Date"],description, bank_data.at[curr, "Debit"], bank_data.at[curr, "Credit"], float(bank_data.at[curr, "Balance"])]
    return merged_bank_data

pdf_path = input()
print(PdfToDf(pdf_path))