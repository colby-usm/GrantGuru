import os
import mysql.connector
from dotenv import load_dotenv
"""
    File: grant_query_comparison.py
    Version: 15 November 2025
    Author: James Tedder

    Made with the help of Gemini

    Description: Uses explain to show how an index improves the query. 
    I struggled to show meaningful changes in time with the state of our database.
    The explain method helps to show the difference that an index can make in our query.
    I chose to optimize the select_grants_by_research_fields query. This query seems ideal for indexing 
    as it is a very straight forward search that will be user prompted and thus should be fast. 
    Before implementing an index on research_fields, the type given by the explain function was 'all'. 
    This means that it is examining every instance of the grant relation. After indexing its type is ref. 
    This means that it can complete without checking every instance of the relation. As our database grows 
    this will be important for allowing our users to access grants in their field quickly.

"""
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

RESEARCH_FIELD_PARAM = ('Biology',) 

def explain_query(cursor, query_name, sql_query, params=None):
    """Executes EXPLAIN on a query and prints the execution plan."""
    print(f"\n--- EXPLAINING QUERY: {query_name} ---")
    
    # Prepend EXPLAIN to the SQL query
    explain_sql = f"EXPLAIN {sql_query}"
    
    try:
        # If parameters are provided, we must use PREPARE/EXECUTE or a client-side
        # binding. Since we are using mysql.connector, we can pass the params 
        # directly to execute, which handles the substitution safely.
        
        # Note: EXPLAIN queries can sometimes behave differently when parameters 
        # are used. For simplicity and broad compatibility, we'll try to execute it 
        # as a string first. For MySQL, if parameters were needed, we'd generally 
        # hardcode them for EXPLAIN or use EXPLAIN ANALYZE.
        
        # Since we're using a single parameter for the targeted query, we'll format 
        # the EXPLAIN output to make it clearer what query is being run.

        if params:
            # For the parameterized query, we'll substitute the %s placeholder 
            # with the actual value for the EXPLAIN command to work correctly.
            # NOTE: This substitution is only for EXPLAIN and should not be used 
            # for standard data queries due to SQL injection risks.
            if len(params) == 1 and sql_query.count('%s') == 1:
                explain_sql = explain_sql.replace('%s', f"'{params[0]}'")
            
        cursor.execute(explain_sql)
        explain_results = cursor.fetchall()
        
        # Print the header for the execution plan
        header = [i[0] for i in cursor.description]
        
        # Simple table formatting
        print("  | " + " | ".join(header))
        print("  " + "-" * (sum(len(h) for h in header) + len(header) * 3 + 1))
        
        # Print the rows of the execution plan
        for row in explain_results:
            print("  | " + " | ".join(map(str, row)))
            
    except mysql.connector.Error as err:
        print(f"Database error executing EXPLAIN for {query_name}: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during EXPLAIN: {e}")

def main():
    db_connection = None
    
    targeted_filter_query = """
    SELECT BIN_TO_UUID(grant_id) as grant_id,
        grant_title,
        opportunity_number,
        description,
        research_field,
        expected_award_count,
        eligibility,
        award_max_amount,
        award_min_amount,
        program_funding,
        provider,
        link_to_source,
        point_of_contact,
        date_posted,
        archive_date,
        date_closed,
        last_update_date
    FROM Grants as g 
    WHERE g.research_field = %s
    """

    try:
        # Establish the database connection
        print("Attempting to connect to the database...")
        db_connection = mysql.connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        print("Connection successful!")
        
        cursor = db_connection.cursor()

        print("\n" + "="*50)
        print("   QUERY EXECUTION PLAN (EXPLAIN)   ")
        print("="*50)

        explain_query(
            cursor, 
            f"3. TARGETED FILTER (research_field='{RESEARCH_FIELD_PARAM[0]}')", 
            targeted_filter_query, 
            params=RESEARCH_FIELD_PARAM
        )
        
        print("\n" + "="*50)
        print("   QUERY EXECUTION AND TIMING (DATA)   ")
        print("="*50)

    except mysql.connector.Error as err:
        print(f"\nCould not connect to database or execute query. Error: {err}")
        print("Please check your database connection and the credentials in 'example.env'.")
    
    finally:
        # Close the connection
        if db_connection and db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()