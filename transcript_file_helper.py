import glob
import json
import os
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tika import parser

import variables as v


def get_file_names(path):
    """
     Goes to location and finds all files in the folder
     :param path: Path to check for file
     :return: list of files
     """

    files_to_parse = list()
    for text_path in glob.glob(f"{path}/*"):
        files_to_parse.append(text_path)

    return files_to_parse


def check_file(file):
    """
    Checks if given file exists.
    :param file: File to check
    :return: True if file found, False if file not found
    """
    if os.path.isfile(file):
        print(f"Found {file}. Skipping")
        return True
    else:
        False


def download_pdf(case, url):
    """
     Goes to the given pdf URL and downloads it.
     :param case: string used to name pdf
     :param url: string where PDF is located
     :return: None
     """

    r = requests.get(f"https://www.supremecourt.gov/oral_arguments{url}", stream=True)

    file_path = f"{v.ROOT_PATH}/{v.PDF_FOLDER}/{case}.pdf"

    print(
        f"Saving PDF to {file_path} from https://www.supremecourt.gov/oral_arguments{url}"
    )
    with open(file_path, "wb") as f:
        f.write(r.content)

    # I think I got blocked by the site so putting in a sleep.
    time.sleep(10)
    return None


def get_transcript_html(year):
    """
    Goes to Supreme Court site for given year and pulls the full HTML from that site
    Does not grab HTML if file already exists in output path
    :param year: Gets transcripts for the year
    :return: None
    :raises Exception: Page was not accessible
    """

    file_to_write = f"{v.ROOT_PATH}/{v.HTML_FOLDER}/001_html_{year}.txt"
    if check_file(file_to_write):
        return None

    url = f"https://www.supremecourt.gov/oral_arguments/argument_transcript/{year}"
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception(
            f"Did not connect successfully. HTTP status code: {r.status_code}\nURL: {url}"
        )

    soup = BeautifulSoup(r.text, "lxml")

    with open(file_to_write, "w") as file:
        file.write(soup.prettify())

    return None


def get_oral_arg_metadata():
    """
     Goes through all the files in 001_html and extracts the metadata and saves it into new folder
     Skipped if file with name is already found.
     :return: None
     """
    for txt_path in glob.glob(f"{v.ROOT_PATH}/{v.HTML_FOLDER}/001_html_*"):
        get_year = txt_path.split("_")
        year = get_year[-1].strip(".txt")

        file_to_write = f"{v.ROOT_PATH}/{v.TR_META_FOLDER}/002_tr_meta_{year}.csv"

        # Check if file exists, if so, skip the whole function.
        if check_file(file_to_write):
            continue

        # Open the file for the year and save as soup.
        with open(f"{v.ROOT_PATH}/{v.HTML_FOLDER}/001_html_{year}.txt", "r") as file:
            soup = BeautifulSoup(file, "lxml")

        # List will be used to write out a csv at end of function
        metadata = [f"'arg_id' |  'name' |  'pdf_url'"]

        # This td has all the data we need for each case
        for row in soup.findAll("td", attrs={"style": "text-align: left;"}):

            # The first span contains the link information and something I'm calling "argument_id"
            link = row.find(
                "span", attrs={"style": "display:block;width:80px;float:left;"}
            )
            a = link.find("a", href=True)
            arg_id = a.text.strip()
            pdf_link = a["href"].strip("..")

            # The second span as the name of the case
            name = (
                row.find("span", attrs={"style": "display:block;"})
                .text.strip()
                .replace("/", "")
                .strip(".")
            )

            # Append to list as promised
            metadata.append(f"{arg_id} | {name} | {pdf_link}")

        # Save list to csv
        with open(f"{file_to_write}", "w") as file:
            file.write("\n".join(metadata))

    return None


def get_pdfs():
    """
     Goes through all the files in folder and
     downloads all the PDFs found in the pdf_url column
     Skipped if PDF is found
     :return: None
     """

    for tr_path in glob.glob(f"{v.ROOT_PATH}/{v.TR_META_FOLDER}/*"):
        metadata = pd.read_csv(
            tr_path, delimiter="|", header=0, names=["arg_id", "name", "pdf_url"]
        )
        for _, row in metadata.iterrows():
            name_of_file = f"{row['arg_id'].strip()}_{row['name'].strip()}"

            if check_file(f"{v.ROOT_PATH}/{v.PDF_FOLDER}/{name_of_file}.pdf"):
                continue

            download_pdf(name_of_file, row["pdf_url"].strip())
    return None


def get_text_from_pdf():
    """
     Goes through all the files in PDF folder and takes text and writes them out
     Skipped if output file already exists
     :return: None
     """

    for pdf_path in glob.glob(f"{v.ROOT_PATH}/{v.PDF_FOLDER}/*"):
        get_pdf_name = pdf_path.split("/")
        txt_path = (
            f"{v.ROOT_PATH}/{v.PDF_RAW_TXT_FOLDER}/{get_pdf_name[-1].strip('.pdf')}.txt"
        )
        if check_file(txt_path):
            continue

        raw = parser.from_file(pdf_path)
        print(f"Writing pdf text to {txt_path}")
        with open(txt_path, "w") as file:
            file.write(raw["content"])
    return None


def check_transcript():
    """
     Some PDFs did not download correctly by checking for access denied message.
     Deletes PDF and transcript so upstream functions can run again.
     :return: None
     """

    for pdf_path in glob.glob(f"{v.ROOT_PATH}/{v.PDF_RAW_TXT_FOLDER}/*"):
        check_string = """Access Denied\n\n\nAccess Denied\n\n\n You don't have permission to access"""
        with open(pdf_path, "r") as file:
            if check_string in file.read():
                orig_pdf = pdf_path.replace(v.PDF_RAW_TXT_FOLDER, v.PDF_FOLDER).replace(
                    ".txt", ".pdf"
                )
                print(f"Removing original PDF at {orig_pdf}")
                os.remove(orig_pdf)
                print(f"Removing transcript at {pdf_path}")
                os.remove(pdf_path)
    return None


def scrub_transcript():
    """
     Scrubs out multiple empty lines, and other issues that could muddy analysis.
     :return: None
     """

    for text_path in glob.glob(f"{v.ROOT_PATH}/{v.PDF_RAW_TXT_FOLDER}/*"):
        file_name = text_path.split("/")[-1]
        all_text = list()

        new_path = f"{v.ROOT_PATH}/{v.CLEAN_TXT_FOLDER}/{file_name}"
        if check_file(new_path):
            continue

        # Get file and remove rows where:
        # the line is empty
        # just numbers (the line counts or page numbers)
        # is just the text of the reporting company or "subject to final review"
        with open(text_path, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                elif re.match(r"^ *\d+ *$", line):
                    continue
                elif re.match(r"^Alderson.*", line):
                    continue
                elif "heritage reporting corporation" in line.lower().strip():
                    continue
                elif "official - subject to final review" in line.lower().strip():
                    continue
                elif re.match(r"^Official *$", line):
                    continue
                elif re.match(r"^ *\d+ *", line):
                    line = re.sub(r"^ *\d+ *", "", line)

                # Replacing soft hyphens with real hyphen, just in case
                # They look the same but are treated differently
                all_text.append(line.replace("­", "-"))
            clean_text = "".join(all_text[1:])

        print(f"Writing to {new_path}")
        with open(new_path, "w") as file:
            file.write(clean_text)

    return None


def get_speaker_text():
    """
     Pulls out speaker and speaker's words into "line index : {speaker : words}" dictionaries
     :return: None
     """

    for text_path in glob.glob(f"{v.ROOT_PATH}/{v.CLEAN_TXT_FOLDER}/*"):
        file_name = text_path.split("/")[-1]
        new_path = f"{v.ROOT_PATH}/{v.SPEECH_FOLDER}/{file_name}"

        if check_file(new_path):
            continue

        with open(text_path, "r") as file:
            long_s = file.read().replace("\n", " ")

        # Regex is looking for at least one word in all caps
        # Possibly followed by a possible period (to match a name like MR. PHILIPS)
        # Possibly followed by two more words (CHIEF JUSTICE ROBERTS is the only three word name we're interested in)
        q = re.compile(r"\b[A-Z]+\b\.*.\b[A-Z]*\b *\b[A-Z]*\b:")
        speech_position = list()
        d = list()

        # Creates a list of lists
        # m.end is when the speech text begins,
        # m.group()[-1] gives us the speaker without the final colon
        for m in q.finditer(long_s):
            speech_position.append([m.end(), m.group()[:-1]])

        # for each item in the row, figures out when the speech ended
        # using a new search for the next name
        for position, speaker in speech_position:
            new_s = long_s[position:]
            if not q.search(new_s):
                continue

            end_position = q.search(long_s[position:]).start()
            speech = new_s[:end_position].strip()

            d.append((speaker, speech))

        print(f"Writing to {new_path}")
        with open(new_path, "w") as file:
            file.write(json.dumps(d))
    return None


def run_all_the_things():
    for my_year in range(2010, 2020):
        get_transcript_html(my_year)

    get_oral_arg_metadata()
    get_pdfs()
    get_text_from_pdf()
    check_transcript()
    scrub_transcript()
    get_speaker_text()