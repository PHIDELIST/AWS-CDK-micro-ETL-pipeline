import boto3

def run_athena_query(query_string, output_location):
    # Create Athena client
    client = boto3.client('athena')
    
    # Execution context
    query_execution = client.start_query_execution(
        QueryString=query_string,
        ResultConfiguration={
            'OutputLocation': output_location
        }
    )
    
    # Get query execution details
    query_execution_id = query_execution['QueryExecutionId']
    response = client.get_query_execution(
        QueryExecutionId=query_execution_id
    )
    
    state = response['QueryExecution']['Status']['State']
    
    # Wait until query execution is completed
    while state in ['QUEUED', 'RUNNING']:
        response = client.get_query_execution(
            QueryExecutionId=query_execution_id
        )
        state = response['QueryExecution']['Status']['State']
    
    # If query execution failed, print error message
    if state == 'FAILED':
        reason = response['QueryExecution']['Status']['StateChangeReason']
        print(f"Query execution failed: {reason}")
        return None
    
    # If query execution succeeded, get query results
    result_location = response['QueryExecution']['ResultConfiguration']['OutputLocation']
    results = client.get_query_results(
        QueryExecutionId=query_execution_id
    )
    
    # Extract and return results
    columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    rows = [row['Data'] for row in results['ResultSet']['Rows']]
    data = [dict(zip(columns, row)) for row in rows[1:]]  # Skip header row
    return data

# query
query_string = """
SELECT
    trip_id,
    COUNT(*) AS trip_count,
    AVG(personid) AS avg_person_id
FROM
    microetldb.micro_etl_output
GROUP BY
    trip_id
ORDER BY
    trip_count DESC
LIMIT
    5;
"""

# output location
output_location = 's3://micro-etl-output/athena-query-results/'

# Run Athena query
query_results = run_athena_query(query_string, output_location)
if query_results:
    print(query_results)
