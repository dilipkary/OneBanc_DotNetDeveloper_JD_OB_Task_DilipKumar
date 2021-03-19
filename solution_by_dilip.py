#%% Dilip's Solution in Python 3.7.9
import pandas as pd
import numpy as np


def StandardizeStatement(inputFile: str, outputFile: str):
    opt_dct = {
        "Date": [],
        "Transaction Description": [],
        "Debit": [],
        "Credit": [],
        "Currency": [],
        "CardName": [],
        "Transaction": [],
        "Location": [],
    }

    inp_df = pd.read_csv(inputFile, header=None).dropna(how="all")
    t_flag = -1
    r_flag = -1
    r_fcnt = -1
    for i, x in inp_df.iterrows():
        if (
            x.str.contains("Domestic Transactions").any()
            or x.str.contains("Domestic Transaction").any()
        ):
            Transaction = "Domestic"
            t_flag = 1
            r_flag = 0
            r_fcnt = 0
            Currency = "INR"
        if (
            x.str.contains("International Transactions").any()
            or x.str.contains("International Transaction").any()
        ):
            Transaction = "International"
            t_flag = 2
            r_flag = 0
            r_fcnt = 0
            Currency = None
        if (
            x.str.contains("Transaction Description").any()
            or x.str.contains("Transaction Details").any()
        ):
            r_flag = 1
            r_fcnt = 1
        if r_flag == 1:
            header_x = [str(a).strip() for a in x]
            r_flag = 2
        if r_fcnt > 1 and len(x) - x.isna().sum() == 1:
            CardName = "".join(x.fillna(""))
            r_fcnt = 2
            r_flag = 3
        if r_fcnt > 2:
            r_dct = {
                "Date": None,
                "Transaction Description": None,
                "Debit": "0",
                "Credit": "0",
                "Currency": Currency,
                "CardName": CardName,
                "Transaction": Transaction,
                "Location": None,
            }
            for vi in range(len(header_x)):
                if header_x[vi] == "Amount":
                    if x.str.contains("cr").any() or x.str.contains("Cr").any():
                        r_dct["Credit"] = str(x[vi].split()[0]).strip()
                    else:
                        r_dct["Debit"] = str(x[vi]).strip()
                elif header_x[vi] in ("Transaction Description", "Transaction Details"):
                    r_dct["Transaction Description"] = str(x[vi]).strip()
                    if t_flag == 1:
                        r_dct["Location"] = str(x[vi]).split()[-1].strip()
                    elif t_flag == 2:
                        r_dct["Currency"] = str(x[vi]).split()[-1].strip()
                        r_dct["Location"] = str(x[vi]).split()[-2].strip()
                else:
                    r_dct[header_x[vi].strip()] = str(x[vi]).strip()
            for ph in (
                "Date",
                "Transaction Description",
                "Debit",
                "Credit",
                "Currency",
                "CardName",
                "Transaction",
                "Location",
            ):
                opt_dct[ph].append(r_dct[ph])
        r_fcnt += 1
    opt_df = pd.DataFrame(opt_dct)
    opt_df[["Debit", "Credit"]] = (
        opt_df[["Debit", "Credit"]].fillna("nan").replace("nan", "0")
    )
    opt_df.to_csv(outputFile, index=False)


StandardizeStatement("HDFC-Input-Case1.csv", "HDFC-Output-Case1.csv")
StandardizeStatement("ICICI-Input-Case2.csv", "ICICI-Output-Case2.csv")
StandardizeStatement("Axis-Input-Case3.csv", "Axis-Output-Case3.csv")
StandardizeStatement("IDFC-Input-Case4.csv", "IDFC-Output-Case4.csv")


# %%
