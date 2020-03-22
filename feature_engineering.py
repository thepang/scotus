import glob

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import variables as v

pd.set_option("display.max_columns", 40)


def get_list_of_cases():
    """
     Goes through the speech folder and grabs all the text file locations
     :return: List of all the text file locations (absolute)
     """
    all_files = list()
    files_to_parse = list()

    problem_files = [
        "/Users/pang/repos/scotus/data/006_speech/000_all.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-184_Kloeckner v. Solis.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-6418_Welch v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-10876_Bullcoming v. New Mexico.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-96_Shelby County v. Holder.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-461_American Broadcasting Co.  v. Aereo, Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-1039_Sandoz Inc. v. Amgen Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-130_Lucia v. SEC.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-537_Bravo-Fernandez v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-5991_Shaw v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-930_Mayorkas v. Cuellar de Osorio.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-9307_Henderson v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-1618_Bostock v. Clayton County.csv",
        "/Users/pang/repos/scotus/data/006_speech/12-417_Sandifer v. United States Steel Cor.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-777_Samsung Electronics Co., v. Apple Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-387_Upper Skagit Tribe v. Lundgren.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-43_Dahda v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/16-349_Henson v. Santander Consumer USA Inc.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-6822_Pepper v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-1433_Brumfield v. Cain.csv",
        "/Users/pang/repos/scotus/data/006_speech/17-1606_Smith v. Berryhill.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-628_Salman v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/15-233_Puerto Rico v. Franklin Cal. Tax-Free Trust.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-1175_Los Angeles v. Patel.csv",
        "/Users/pang/repos/scotus/data/006_speech/09-1227_Bond v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/11-5683_Dorsey v. United States.csv",
        "/Users/pang/repos/scotus/data/006_speech/13-895_Alabama Legislative Black Caucus v. Alabama.csv",
        "/Users/pang/repos/scotus/data/006_speech/10-7387_Setser v. United States.csv",
    ]

    for text_path in glob.glob(f"{v.ROOT_PATH}/{v.SPEECH_FOLDER}/*"):
        all_files.append(text_path)

    for file in all_files:
        if file not in problem_files:
            files_to_parse.append(file)
        else:
            print(f"Skipping: {file}")

    return files_to_parse


def num_speak_data():
    def count_num(text):
        """
          Counts the number of times a speaker speaks in a given transcript
          :param text: text to find speaker counts
          :return: petitioner_judge, petitioner_lawyer, respondent_judge, respondent_lawyer
          """
        speaker_cts = text.groupby(by=["party", "speaker_type"]).count().reset_index()

        return speaker_cts["speaker"].tolist()

    files = get_list_of_cases()
    to_df = []
    for file in files:
        (
            petitioner_judge,
            petitioner_lawyer,
            respondent_judge,
            respondent_lawyer,
        ) = count_num(pd.read_csv(file))
        to_df.append(
            [
                file.split("/")[-1].split("_")[0],
                petitioner_judge,
                petitioner_lawyer,
                respondent_judge,
                respondent_lawyer,
            ]
        )
    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "speak_num_pet_jdg",
            "speak_num_pet_law",
            "speak_num_res_jdg",
            "speak_num_res_law",
        ],
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/num_speak_data.csv", index=False)
    return None


def num_interruptions():
    def count_interruptions(text):
        """
          Counts the number of times a speaker is interrupted by looking for sentences that end in "--"
          :return: pj_interrupt, pl_interrupt, rj_interrupt, rl_interrupt
          """

        text["interrupt_count"] = np.where(
            text["text"].str.contains(r"--$", regex=True), 1, 0
        )
        df = text.groupby(by=["party", "speaker_type"]).sum().reset_index()

        pj, pl, rj, rl = df["interrupt_count"].tolist()
        return pj, pl, rj, rl, text

    full_df = pd.DataFrame(
        columns=["party", "speaker_type", "speaker", "text", "interrupt_count"]
    )
    files = get_list_of_cases()
    to_df = []

    # columns = [party,speaker_type,speaker,text,interrupt_count]
    # df = pd.DataFrame(columns=columns)

    for file in files:
        print(f"Processing: {file})")

        (
            pj_interrupt,
            pl_interrupt,
            rj_interrupt,
            rl_interrupt,
            docket_df,
        ) = count_interruptions(pd.read_csv(file))
        docket_df["docket"] = file.split("/")[-1].split("_")[0]
        full_df = full_df.append(docket_df, ignore_index=False)
        to_df.append(
            [
                file.split("/")[-1].split("_")[0],
                pj_interrupt,
                pl_interrupt,
                rj_interrupt,
                rl_interrupt,
            ]
        )

    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "pj_interrupted",
            "pl_interrupted",
            "rj_interrupted",
            "rl_interrupted",
        ],
    )

    full_df.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_interruption_count.csv",
        columns=[
            "docket",
            "party",
            "speaker_type",
            "speaker",
            "text",
            "interrupt_count",
        ],
        index=False,
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/interruption_data.csv", index=False)
    return None


def sentiment_scores():
    def get_sentiment(df):
        analyzer = SentimentIntensityAnalyzer()

        columns = ["neg", "pos", "neu", "compound"]

        for name in columns:
            df[name] = 0

        for index, row in df.iterrows():
            try:
                vs = analyzer.polarity_scores(row["text"])
                for score in columns:
                    df.loc[index, score] = vs[score]
            except AttributeError:
                pass

        sum_df = df.groupby(by=["party", "speaker_type"]).mean().reset_index()
        sentiments = list()

        for name in columns:
            for item in sum_df[name].values:
                sentiments.append(item)

        return sentiments, df

    files = get_list_of_cases()
    to_df = []
    full_data = pd.DataFrame()

    for file in files:
        print(f"Processing: {file})")
        docket_num = file.split("/")[-1].split("_")[0]

        scores, df = get_sentiment(pd.read_csv(file))
        df["docket"] = docket_num
        full_data = full_data.append(df, ignore_index=False)
        temp_ = [docket_num]

        [temp_.append(item) for item in scores]
        to_df.append(temp_)

    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "pj_sent_neg",
            "pl_sent_neg",
            "rj_sent_neg",
            "rl_sent_neg",
            "pj_sent_pos",
            "pl_sent_pos",
            "rj_sent_pos",
            "rl_sent_pos",
            "pj_sent_neu",
            "pl_sent_neu",
            "rj_sent_neu",
            "rl_sent_neu",
            "pj_sent_compound",
            "pl_sent_compound",
            "rj_sent_compound",
            "rl_sent_compound",
        ],
    )

    full_data.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_sentiment_data.csv",
        columns=[
            "docket",
            "party",
            "speaker_type",
            "speaker",
            "text",
            "neg",
            "pos",
            "neu",
            "compound",
        ],
        index=False,
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/sentiment_data.csv", index=False)
    return None


def num_word_counts():
    def count_words(text):
        """
          Counts the number of times a speaker is interrupted by looking for sentences that end in "--"
          :return: pj_interrupt, pl_interrupt, rj_interrupt, rl_interrupt
          """

        text["word_count"] = 0
        for index, row in text.iterrows():
            words = str(row["text"]).split(" ")
            text.loc[index, "word_count"] = len(words)

        df = text.groupby(by=["party", "speaker_type"]).sum().reset_index()

        pj, pl, rj, rl = df["word_count"].tolist()

        return pj, pl, rj, rl, text

    files = get_list_of_cases()
    to_df = []
    full_df = pd.DataFrame()

    for file in files:
        print(f"Processing: {file})")

        docket_num = file.split("/")[-1].split("_")[0]
        (
            pj_word_count,
            pl_word_count,
            rj_word_count,
            rl_word_count,
            text_df,
        ) = count_words(pd.read_csv(file))

        text_df["docket"] = docket_num
        to_df.append(
            [docket_num, pj_word_count, pl_word_count, rj_word_count, rl_word_count]
        )
        full_df = full_df.append(text_df, ignore_index=False)
    df = pd.DataFrame(
        to_df,
        columns=[
            "docket",
            "pj_word_count",
            "pl_word_count",
            "rj_word_count",
            "rl_word_count",
        ],
    )
    full_df.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_word_count_data.csv",
        columns=["docket", "party", "speaker_type", "speaker", "text", "word_count"],
        index=False,
    )
    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/num_word_count_data.csv", index=False)
    return None


def num_short_exchanges():
    test = pd.read_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_word_count_data.csv")
    test = (
        test[test["word_count"] < 5]
        .groupby(by=["docket", "party", "speaker_type"])
        .count()
        .reset_index()
    )
    dockets = test["docket"].unique()

    dictionary = dict()

    for docket in dockets:
        docket_subset = test[test["docket"] == docket].sort_values(
            by=["docket", "party", "speaker_type"]
        )
        counts = dict()

        for index, row in docket_subset.iterrows():
            if row["party"] == "petitioner" and row["speaker_type"] == "lawyer":
                variable = "short_x_pl"
            elif row["party"] == "petitioner" and row["speaker_type"] == "judge":
                variable = "short_x_pj"
            elif row["party"] == "respondent" and row["speaker_type"] == "lawyer":
                variable = "short_x_rl"
            elif row["party"] == "respondent" and row["speaker_type"] == "judge":
                variable = "short_x_rj"
            counts[variable] = row["word_count"]

        dictionary[docket] = counts

    full_data = pd.DataFrame(dictionary).T
    full_data = full_data.fillna(0)

    full_data.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/short_exchange_count.csv",
        index_label="docket",
    )

    return None


def num_stutter():
    all_words = pd.read_csv("/Users/pang/repos/scotus/data/007_features/words.csv")
    full_stutter_counts = dict()
    for index, row in all_words.iterrows():
        row_count = dict()
        for item in row.index.values:
            if item == "docket":
                docket = row[item]
            elif item == "pj_text":
                row_count["pj_stutter_ct"] = row[item].count(" -- ")
            elif item == "pl_text":
                row_count["pl_stutter_ct"] = row[item].count(" -- ")
            elif item == "rj_text":
                row_count["rj_stutter_ct"] = row[item].count(" -- ")
            elif item == "rl_text":
                row_count["rl_stutter_ct"] = row[item].count(" -- ")
            else:
                print("Shouldn't hit this")
        full_stutter_counts[docket] = row_count
    df = pd.DataFrame(full_stutter_counts).T

    df.to_csv(
        f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/full_stutter_count.csv",
        index_label="docket",
    )

    return None


# num_speak_data()
# num_interruptions()
# sentiment_scores()
# num_word_counts()
# num_short_exchanges()
# num_stutter()
