import pandas as pd


# Copy link from https://www.genome.gov/about-genomics/fact-sheets/DNA-Sequencing-Costs-Data
URL = "https://www.genome.gov/sites/default/files/media/files/2021-11/Sequencing_Cost_Data_Table_Aug2021.xls"


def main():

    df = pd.read_excel(URL)

    df = df.rename(
        columns={
            "Date": "year",
            "Cost per Mb": "cost_per_mb",
            "Cost per Genome": "cost_per_genome",
        }
    )

    df["year"] = df["year"].dt.year

    df = df.sort_values(by="cost_per_genome")
    df = df.drop_duplicates(subset=["year"])

    df = df.sort_values(by="year")

    df["entity"] = "World"
    df = df[["entity", "year", "cost_per_mb", "cost_per_genome"]]

    df["cost_per_gb"] = df.cost_per_mb * 1000
    df = df.drop(columns="cost_per_mb")
    df[["cost_per_gb", "cost_per_genome"]] = df[
        ["cost_per_gb", "cost_per_genome"]
    ].round(2)

    df.to_csv("NIH - DNA Sequencing Costs.csv", index=False)


if __name__ == "__main__":
    main()
