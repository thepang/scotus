import pandas as pd

import transcript_file_helper as gt
import variables as v

pd.set_option("display.max_columns", 40)
ft_folder = f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}"

# scdb data manually downloaded from http://supremecourtdatabase.org/index.php
scdb_docket_location = "data/SCDB_2019_01_caseCentered_Docket.csv"


def get_case_meta_from_scdb():
    """
     Goes to predefined location and finds metadata for cases that are in the speech folder.
     (Using the file's supreme court docket id to join the two pieces of data)
     Saves the data in the features folder.
     :return: None
     """
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
    case_meta = (
        dockets_for_analysis.merge(docket_meta, how="inner", on="docket")
        .sort_values(by="docket")
        .drop(
            columns=[
                # SCDB specific data and is not useful for analysis
                "caseId",
                "docketId",
                "caseIssuesId",
                "voteId",
                # Other cite data not useful for analysis
                "usCite",
                "sctCite",
                "ledCite",
                "lexisCite",
                # Data related to outcome that can't be used for analysis
                "decisionType",
                "declarationUncon",
                "caseDisposition",
                "caseDispositionUnusual",
                "precedentAlteration",
                "voteUnclear",
                "decisionDirection",
                "decisionDirectionDissent",
                "authorityDecision1",
                "authorityDecision2",
                "majOpinWriter",
                "majOpinAssigner",
                "splitVote",
                # Other data not useful for analysis
                "chief",
                "caseName",
                # Too sparse. Data will require too many dummy variables.
                "issue"  # possibly put this back in if I need more features
                "petitionerState",
                "adminActionState",
                "threeJudgeFdc",
                "caseOriginState",
                "lawSupp",  # seems redundant with lawType
                "lawMinor",
            ]
        )
    )

    print(f"Saving metadata to {ft_folder}")

    case_meta.to_csv(
        f"{ft_folder}/raw_features.csv", index=False, quoting=1, quotechar="'"
    )

    return case_meta


def clean_meta():
    """
     Open the predetermined raw_features folder and does all the cleaning for analysis in Jupyter
     Dummies out columns as defined by to_dummy variable.
     Fills in nulls.
     :return: dataframe
     """
    import_df = pd.read_csv(
        f"{ft_folder}/raw_features.csv", quotechar="'", parse_dates=[1, 4, 5]
    )

    # Remove the duplicate row for 15-1498

    to_dummy = {
        "petitioner": 6,
        "respondent": 3,
        "respondentState": 1,  # This is California, maybe rename to is_CA?
        "jurisdiction": 1,  # 1=cert, 2=appeal change to is_Cert?
        "adminAction": 2,  # 117=stateagency, 7=board of immigration appeals
        "caseOrigin": 1,  # for now, possibly look into grouping them another way later
        "caseSource": 1,  # for now, possibly look into grouping them another way later
        "caseSourceState": 1,  # 6=California
        "certReason": 3,
        "lcDisposition": 2,
        "lcDispositionDirection": 2,
        "issueArea": 3,
        "lawType": 3,
        "issue": 1,
    }

    for column in to_dummy:
        import_df = dummy_variables(column, import_df, to_dummy[column])

    import_df["dateRearg"] = [
        0 if str(item) == "NaT" else 1 for item in import_df.pop("dateRearg")
    ]

    return import_df.fillna(0)


def dummy_variables(column_name, df, limit=3):
    """
     Goes to predefined location and finds metadata for cases that are in the speech folder.
     (Using the file's supreme court docket id to join the two pieces of data)
     Saves the data in the features folder.
     returns df with updated dummy variables
     :param column_name: name of column to dummy
     :param df: df to update with dummy variables
     :param limit: by default, limits to the top three values to dummy, otherwise, provide an integer
     :return: df with column_name column removed and new dummies added
     """

    column_to_dummy = df.pop(column_name)
    dummies = pd.get_dummies(column_to_dummy, prefix=column_name)

    keep_columns = column_to_dummy.value_counts().index[:limit]
    columns_to_keep = [f"{column_name}_{item}" for item in keep_columns]

    to_add = dummies.filter(items=columns_to_keep)

    df = df.join(to_add)

    return df


def remove_validate_data(df):
    """
     Removes all rows where the decision came out in 2019 to save for validate.
     :param df: df to update remove rows
     :return: x_df for analysis and y_df for validating later on
     """

    df["dateDecision"] = pd.DataFrame(df["dateDecision"])

    x_df = df[df["dateDecision"] < "2019-01-01"]
    y_df = df[df["dateDecision"] >= "2019-01-01"]

    return x_df, y_df


def remove_duplicates(df):
    """
     Takes the df and uses Panda functionality and removes duplicate.
     Docket 15-1498 had two oral arguments, kinda making sure the dedupe only drops the one copy
     :param df: df to drop dupes
     :return: df dupes gone
     :raises Exception: when more than one row is removed
     """
    dedupe_df = df.drop_duplicates(keep="first")

    expected_count = 617
    if len(dedupe_df) != 617:
        raise Exception(
            f"Unexpected count of items. Expected {expected_count}, but found {len(dedupe_df)}"
        )

    return dedupe_df


def save_to_csv(df):
    """
     Reorders the columns
     :param column_name: name of column to dummy
     :param df: df to update with dummy variables
     :param limit: by default, limits to the top three values to dummy, otherwise, provide an integer
     :return: None
     """
    columns = df.columns.tolist()
    [
        columns.remove(item)
        for item in ["docket", "partyWinning", "majVotes", "minVotes", "dateRearg"]
    ]

    dedupe_df = remove_duplicates(df)

    # If possible, can add ['majVotes', 'minVotes'] back in, for now just focus on the 1, 0
    x_df, y_df = remove_validate_data(
        pd.DataFrame(dedupe_df[["docket", "partyWinning"] + columns])
    )

    for metadata_csv in ["num_speak_data.csv"]:
        df = pd.read_csv(f"{ft_folder}/{metadata_csv}", index_col="docket")
        x_df = x_df.join(df, on="docket")
        print(x_df)

    x_df.to_csv(f"{ft_folder}/for_analysis.csv", index=False)

    y_df.to_csv(f"{ft_folder}/validation_data.csv", index=False)

    return None


# get_case_meta_from_scdb()
df = clean_meta()
save_to_csv(df)
