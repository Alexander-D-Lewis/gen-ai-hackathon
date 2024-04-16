import logging
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_links(url, link_snips, link_remove= []):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, "html.parser")

    links = []

    for link in soup.findAll("a"):
        if all(l in str(link.get("href")).lower() for l in link_snips):
            if link_remove == []:
                links.append(link.get("href"))
            elif link_remove not in str(link.get("href")):
                links.append(link.get("href"))

    return links



def scrape_ipa_reports(output_path="", output_combined=False):
    """Scrape all csv files from the IPA website, grouping by year"""
    base_url = "https://www.gov.uk/government/collections/major-projects-data"

    # get all annual links on page
    page_links = get_links(base_url, 
                           ["-government-major-projects-portfolio-data-"])

    # for each annual link, find the first csv
    scraped_files = {}
    for page in sorted(page_links):
        try:

            # There's a typo in 'Portfolio' in 2023's links
            individual_link = get_links(f"https://www.gov.uk{page}", ["government_major_project"])
            individual_link.extend(get_links(f"https://www.gov.uk{page}", ["gmpp-data"]))
            individual_link.extend(get_links(f"https://www.gov.uk{page}", ["government-major-projects"]))

            if len(individual_link)<1:
                logging.info(f"No sublinks for {page}")

            else: 
                individual_link = individual_link[0]
                if individual_link.split(".")[-1] == "csv":
                        dept_csv = pd.read_csv(individual_link)

                elif "xls" in individual_link.split(".")[-1]:
                    dept_csv = pd.read_excel(individual_link)

                else:
                    logging.info(f"Unknown filetype for {individual_link}")
                    continue

                file_year = page.split("-")[-1]
                dept = individual_link.split("/")[-1].split("_")[0]
                logging.info(f"Scraping {dept}-{file_year}")

                if file_year in scraped_files.keys():
                    scraped_files[file_year].append(dept_csv)
                
                else:
                    scraped_files[file_year] = [dept_csv]
                    
        except:
            logging.warning(f"Failed to scrape {individual_link}")


    if output_combined:
        dfs = [df for sublist in scraped_files.values for df in sublist]
        logging.info(f"Saving {len(dfs)} reports in one file")
        full_df = pd.concat(dfs)
        full_df.to_csv(f"{output_path}IPA-reports-ALL.csv")

    else:
        # output as merge files for each year
        for year, dfs in scraped_files.items():
            logging.info(f"Saving {len(dfs)} reports for {year}")
            year_df = pd.concat(dfs)
            year_df.to_csv(f"{output_path}IPA-reports-{year}.csv")

    logging.info("Finished scraping IPA annual projects")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scrape_ipa_reports(output_path="data/", output_combined=False)