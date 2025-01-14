Welcome!

The stack of this project utilizes the following tool:
1. dbt (data transformation)
2. dlt (data extract and load)
3. Postgres (data storage)
4. Dagster (data orchestration)

Dagster orchestrates the whole process, starting from data extract and load from the github's CSSE repository csv sources (using dlt), and transfrom the data mart models in postgres (using dbt). 

### pre-requisites
Ensure the following pre-requisites to be setup:

1. Python 3.10.0 to <3.13.0
2. PostgreSQL


### Using the starter project

Open the terminal into this repository forlder and follow these steps to get the dagster up and running:

1. run `python3 -m venv venv`

to setup the virtual environment. The further improvement for this project is to containerized the whole stack in Docker.

2. run `source ./venv/bin/activate`.
3. run `pip3 install -r requirements.txt` to install the required packages.
4. `cd csse_dagster` to get into the dagster project.
5. rename `.env.dist` to `.env`.
6. adjust the variables to your postgres environment creds.
7. run `dagster dev` then go into your favorite browser and visit http://127.0.0.1:3000

you should find the lineage and you are now able to materialized some asset(s).

the command can only be ran inside the dagster project.

### Analysis
go to `analyses\` and find the scripts.

go to the `profile.yml` and adjust the postgres password.

run `dbt compile` then the full-script will be available under `/target/compiled/dagster_dbt/analyses`

there will be `sql_analysis.sql` to run to answer the following questions:
- What are the top cases and its frequency?
- How does cases change over time?
- Is there any correlation from one to another?

we find that most of the country had its peak of confirmed covid cases in the year of 2022, where the 5 biggest cases in 2022 are US (382 million confirmed cases), France (132 million confirmed cases), United Kingdom (112 million confirmed cases), India (15 million confirmed cases), Netherlands (14 million confirmed cases). 

Tuvalu seems to be the outlier here when it reaches it peak on 2023 with 190 thousands confirmed cases.

Most countries started to have its cases reported from 2020, during 2020 to 2022, the cases keeps increasing and starts dropping from 2023.

The asumptions includes only to the reported cases under obervations, this is because not all confirmed cases has seem to report the recovery and the death, there's a significant gap between confirmed cases and recovery/death case.  

The reported recovery and death cases has seemed to tend to negatively correlated to each other throughout the years. Except in 2021, where the reported death cases and recovery cases has seem to correlate to many countries.