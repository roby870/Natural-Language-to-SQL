import pandas as pd
import sqlite3
from openai import OpenAI


class NLPToSQL:
    def __init__(self, api_key, csv_path):
        self.client = OpenAI(api_key=api_key)
        self.conn = sqlite3.connect(':memory:')
        self.df = pd.read_csv(csv_path, quotechar='"', delimiter=',', skipinitialspace=True)
        self._prepare_data()

    def _prepare_data(self):
        """Clean and transform the dataframe, and store it in SQLite."""
        self.df['amount'] = self.df['amount'].replace({'\$': '', ',': ''}, regex=True)
        self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
        self.df.to_sql('contributions', self.conn, index=False, if_exists='replace')

    def natural_language_to_sql(self, natural_query):
        """Convert a natural language query to SQL using OpenAI."""
        prompt = f"""
        I have a csv dataset. Pay close attention to the format of each column. The structure is as follows:
        - CYCLE (integer): Year of the contribution, in uppercase.
        - State/Federal (text): Level of government (State or Federal), mixed case.
        - CONTRIBID (text): Contributor ID, in uppercase.
        - CONTRIB (text): Contributor name, mixed case.
        - CITY (text): Contributor's city.
        - STATE (text): Contributor's state (abbreviated, e.g., NY for New York, CA for California).
        - ZIP (text): Zip code.
        - FECOCCEMP (text): Employment field, mixed case.
        - ORGNAME (text): Organization name, mixed case.
        - ULTORG (text): Last known organization of the contributor, mixed case.
        - DATE (date): Date of contribution, formatted as MM/DD/YYYY.
        - AMOUNT (currency): Contribution amount.
        - RECIPID (text): Recipient ID, uppercase.
        - RECIPIENT (text): Recipient name, mixed case.
        - PARTY (text): Political party of the recipient, uppercase (e.g., "D" or "R").
        - RECIPCODE (text): Recipient code, uppercase.
        - TYPE (text): Type of contribution, uppercase.
        - FECTRANSID (text): Transaction ID, uppercase.
        - CMTEID (text): Committee ID, uppercase.

        Here you can check some example data:

        2022,State,1920715992,"KAUFMAN, WILLIE",NEW YORK,NY,10005,,Alameda Research,,5/14/2022,$400,55587498,"DICKSON, RUBY",D,DO,15,,,
        2022,Federal,f1000218669,"BANKMAN, ALAN JOE",STANFORD,CA,94305,STANFORD AND FTX US,FTX.US,,7/2/2022,"$1,000",N00051422,"Bond, Michelle",R,RL,15E,4082520221566200368,P,C00816561
        2020,Federal,j1001936195,"WETJEN, MARK",WASHINGTON,DC,20017,MIAMI INTERNATIONAL HOLDINGS,Miami International Holdings,,7/9/2020,"$5,600",N00000699,"Menendez, Robert",D,DI,15E,T217948909,,C00264564
        2020,Federal,j1001936195,"WETJEN, MARK",WASHINGTON,DC,20017,MIAMI INTERNATIONAL HOLDINGS,Miami International Holdings,,7/9/2020,"$4,000",N00000699,"Menendez, Robert",D,DI,15E,T200003382,,C00264564
        2022,Federal,j1001936195,"WETJEN, MARK",WASHINGTON,DC,20017,FTX,FTX.US,,2/11/2022,"$2,900",N00004118,"Stabenow, Debbie",D,DI,15J,4042820221473189023,P,C00344473
        2022,Federal,j1001936195,"WETJEN, MARK",WASHINGTON,DC,20017,FTX,FTX.US,,2/11/2022,"$2,900",N00004118,"Stabenow, Debbie",D,DI,15J,4042820221473189024,G,C00344473
        2022,Federal,j1001936195,"WETJEN, MARK",CHEVY CHASE,MD,20815,FTX,FTX.US,,3/22/2022,"$2,900",N00013873,"Boozman, John",R,RI,15E,4042520221472041104,P,C00476317
        
        In my python script, I transform the csv into a table called "contributions" using pandas and sqlite.
        Translate the following natural language query into an SQL query that works on the "contributions" table:
        "{natural_query}".
        Give me only the query, because I will copy it automatically and run it to query the database. So don't add anything, return only the query.

        When generating SQL queries, please ensure they are efficient. For instance, avoid:
        - Using `SELECT *`, and instead specify only the necessary columns.
        - Using subqueries unless absolutely necessary.
        - Any operations that could result in slow performance for large datasets.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        sql_query = response.choices[0].message.content.strip()
        sql_query = sql_query.replace('```', '').strip()
        sql_query = sql_query.replace('sql', '').strip()
        return sql_query

    def execute_sql_query(self, sql_query):
        """Execute an SQL query against the SQLite database and return the results."""
        return pd.read_sql_query(sql_query, self.conn)


if __name__ == "__main__":
    API_KEY = "private"
    CSV_PATH = "Copy of OpenSecrets.org _ FTX_Alameda Research Contributions - Direct Contributions & JFC Distributions.csv"
    nlp_to_sql = NLPToSQL(api_key=API_KEY, csv_path=CSV_PATH)
    #TEST ANY QUERY HERE
    natural_query = "Show the total amount of contributions in New York for 2022."
    sql_query = nlp_to_sql.natural_language_to_sql(natural_query)
    print("Generated SQL query:", sql_query)
    result = nlp_to_sql.execute_sql_query(sql_query)
    print(result)
