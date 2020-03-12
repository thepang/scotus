import pandas as pd

import transcript_file_helper as gt
import variables as v

# scdb data manually downloaded from http://supremecourtdatabase.org/index.php
scdb_docket_location = "data/SCDB_2019_01_caseCentered_Docket.csv"


def get_case_meta_from_scdb():
    docket_meta = pd.read_csv(scdb_docket_location, encoding="ISO-8859-1")
    file_names = gt.get_file_names(f"{v.ROOT_PATH}/{v.SPEECH_FOLDER}")

    dockets = list()
    for item in file_names:
        # Get the file name and split it on the _
        # Example file name: "18-5924_Ramos v. Louisiana.txt"
        id_, _ = item.split("/")[-1].split("_")
        dockets.append(id_)

    # Convert list to data frame for merge later on.
    dockets_for_analysis = pd.DataFrame(dockets, columns=["docket"])

    # Inner join because there are cases that were argued but have not been decided on.
    # The join gets us cases that went through oral argument and have received a decision.
    case_meta = dockets_for_analysis.merge(
        docket_meta, how="inner", on="docket"
    ).sort_values(by="docket")

    return case_meta


cases = get_case_meta_from_scdb()
print(len(cases["partyWinning"].unique()))
