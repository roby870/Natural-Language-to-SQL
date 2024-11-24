# Natural Language to SQL Module Using LLMs


## Overview

You are tasked with developing a module that translates natural language queries into SQL
queries using large language models (LLMs). This module will enable users to interact with a
database using everyday language, without needing to write SQL code directly. The objective is
to assess your ability to understand the dataset, write efficient SQL queries, and leverage LLMs
for natural language processing.


## Problem statement

Create a module that accepts a natural language query and returns the corresponding SQL query.
Utilize LLMs to interpret and translate the natural language input into a syntactically correct SQL query.


## Dataset Description

The dataset provided contains information about contributions from various contributors to
different recipients. The data includes details such as contribution amount, contributor
information, recipient information, dates, and states. Here is a snapshot of the dataset structure:
cycle: The election cycle year.
State/Federal: Indicates if the contribution is for state or federal elections.
contribid: Unique identifier for the contributor.
contrib: Name of the contributor.
City: City of the contributor.
State: State of the contributor.
Zip: Zip code of the contributor.
Fecoccemp: Occupation/employer of the contributor.
orgname: Organization name associated with the contribution.
ultorg: Ultimate organization associated with the contribution.
date: Date of the contribution.
amount: Contribution amount.
recipid: Unique identifier for the recipient.
recipient: Name of the recipient.
party: Political party of the recipient.
recipcode: Recipient code.
type: Type of contribution.
fectransid: FEC transaction ID.
pg: Page number.
cmteid: Committee ID.


## How to run the script

Create a virtual environment on a new directory running `python3 -m venv venv`. Then activate it with `source ./venv/bin/activate`, and you have to run (on this new directory) `pip install -r requirements.txt`.

You can hardcode your OpenAI api key on the script or use an environment variable. Also you can hardcode any query below the `#TEST ANY QUERY HERE` comment.

Run the script with `python3 ./NLP_to_SQL.py`. 
