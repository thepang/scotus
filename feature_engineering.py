import glob

import numpy as np
import pandas as pd

import variables as v

pd.set_option("display.max_columns", 40)
problem_files = [
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


def get_list_of_cases():
    """
     Goes through the speech folder and grabs all the text file locations
     :return: List of all the text file locations (absolute)
     """
    files_to_parse = list()
    for text_path in glob.glob(f"{v.ROOT_PATH}/{v.SPEECH_FOLDER}/*"):
        files_to_parse.append(text_path)

    return files_to_parse


def count_num(text):
    """
      Counts the number of times a speaker speaks in a given transcript
      :param text: text to find speaker counts
      :return: petitioner_judge, petitioner_lawyer, respondent_judge, respondent_lawyer
      """
    speaker_cts = text.groupby(by=["party", "speaker_type"]).count().reset_index()

    return speaker_cts["speaker"].tolist()


def num_speak_data():
    files = get_list_of_cases()
    to_df = []
    for file in files:
        if file in problem_files:
            continue

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


def count_interruptions(text):
    """
      Counts the number of times a speaker is interrupted by looking for sentences that end in "--"
      :return: pj_interrupt, pl_interrupt, rj_interrupt, rl_interrupt
      """
    # print(text['text'].value[-2:])
    text["interrupt_count"] = np.where(
        text["text"].str.contains(r"--$", regex=True), 1, 0
    )
    df = text.groupby(by=["party", "speaker_type"]).sum().reset_index()

    return df["interrupt_count"].tolist()


def num_interruptions():
    files = get_list_of_cases()
    to_df = []
    for file in files:
        if file in problem_files:
            continue

        pj_interrupt, pl_interrupt, rj_interrupt, rl_interrupt = count_interruptions(
            pd.read_csv(file)
        )

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
            "pj_interrupt",
            "pl_interrupt",
            "rj_interrupt",
            "rl_interrupt",
        ],
    )

    df.to_csv(f"{v.ROOT_PATH}/{v.FEATURES_FOLDER}/interruption_data.csv", index=False)
    return None


num_interruptions()
