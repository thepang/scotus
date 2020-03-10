import glob
import os.path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tika import parser

path_to_root = "/Users/pang/repos/scotus"


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

    file_path = f"{path_to_root}/data/003_pdfs/{case}.pdf"

    print(
        f"Saving PDF to {file_path} from https://www.supremecourt.gov/oral_arguments{url}"
    )
    with open(file_path, "wb") as f:
        f.write(r.content)
    return None


def get_transcript_html(year):
    """
    Goes to Supreme Court site for given year and pulls the full HTML from that site
    Does not grab HTML if file already exists in output path
    :param year: Gets transcripts for the year
    :return: None
    """

    file_to_write = f"{path_to_root}/data/001_html/001_html_{year}.txt"
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


def get_oral_arg_metadata(path):
    """
     Goes through all the files in 001_html and extracts the metadata and saves it into new folder
     :param path: Root path that the 001_html directory is.
     :return: None
     """
    for txt_path in glob.glob(f"{path}/data/001_html/001_html_*"):
        get_year = txt_path.split("_")
        year = get_year[-1].strip(".txt")

        file_to_write = f"{path}/data/002_transcript_metadata/002_tr_meta_{year}.csv"

        # Check if file exists, if so, skip the whole function.
        if check_file(file_to_write):
            continue

        # Open the file for the year and save as soup.
        with open(f"{path}/data/001_html/001_html_{year}.txt", "r") as file:
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
            )

            # Append to list as promised
            metadata.append(f"{arg_id} | {name} | {pdf_link}")

        # Save list to csv
        with open(f"{file_to_write}", "w") as file:
            file.write("\n".join(metadata))

    return None


def get_pdfs(path):
    """
     Goes through all the files in 002_transcript_metadata folder and
     downloads all the PDFs found in the pdf_url column
     :param path: Root path that the 001_html directory is.
     :return: None
     """

    for tr_path in glob.glob(f"{path}/data/002_transcript_metadata/*"):
        metadata = pd.read_csv(
            tr_path, delimiter="|", header=0, names=["arg_id", "name", "pdf_url"]
        )
        for _, row in metadata.iterrows():
            name_of_file = f"{row['arg_id'].strip()}_{row['name'].strip()}"

            if check_file(f"{path}/data/003_pdfs/{name_of_file}.pdf"):
                continue

            download_pdf(name_of_file, row["pdf_url"].strip())
    return None


def get_text_from_df():
    return


# for my_year in range(2010,2020):
#     get_transcript_html(my_year)
#
# get_oral_arg_metadata(path_to_root)
# get_pdfs(path_to_root)
#
#
#
#
raw = parser.from_file("/Users/pang/repos/scotus/data/003_pdfs/16-399.pdf")
# print(raw['content'])
