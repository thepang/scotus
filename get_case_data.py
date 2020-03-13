import pandas as pd

import transcript_file_helper as gt
import variables as v

pd.set_option("display.max_columns", 500)

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
                "petitionerState",
                "adminActionState",
                "threeJudgeFdc",
                "caseOriginState",
                "lawSupp",  # seems redundant with lawType
                "lawMinor",
            ]
        )
    )

    return case_meta


# Data of the truthe: 'majVotes', 'minVotes', 'partyWinning'
# Update the following to dummy out the top 1-3 or to values
# petitioner, and respondent, adminAction, certReason, issue, issueArea
# 'lcDisagreement', 'lcDisposition', 'lcDisposition', lawType
# Change petitionerState to just track if the case is from California, and respondentState to track if from TX
# Change Jurisdiction to b e a bool, only two values anyways
# caseOrigin/caseSource might be redundant with other columns. start with it only using the top few dummied out

cases = get_case_meta_from_scdb()
# print(cases)
variable = "lawMinor"
print(cases)
