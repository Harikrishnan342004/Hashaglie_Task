from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def createCollection(p_collection_name):
    if not es.indices.exists(index=p_collection_name):
        es.indices.create(index=p_collection_name)
        print(f"Collection {p_collection_name} created.")
    else:
        print(f"Collection {p_collection_name} already exists.")


#### 2. *Index Data*

import pandas as pd

def indexData(p_collection_name, p_exclude_column):
    # Load the employee data
    df = pd.read_csv('employees.csv')
    
    # Drop the excluded column
    if p_exclude_column in df.columns:
        df = df.drop(columns=[p_exclude_column])
    
    # Index each row into Elasticsearch
    for i, row in df.iterrows():
        es.index(index=p_collection_name, id=row['Employee ID'], body=row.to_dict())
    print(f"Data indexed into {p_collection_name}, excluding {p_exclude_column}.")


#### 3. *Search by Column*

def searchByColumn(p_collection_name, p_column_name, p_column_value):
    query = {
        "query": {
            "match": {
                p_column_name: p_column_value
            }
        }
    }
    res = es.search(index=p_collection_name, body=query)
    return res['hits']['hits']


#### 4. *Get Employee Count*

def getEmpCount(p_collection_name):
    res = es.count(index=p_collection_name)
    return res['count']


#### 5. *Delete Employee by ID*
# Define a function to delete an employee by ID:
# python
def delEmpById(p_collection_name, p_employee_id):
    res = es.delete(index=p_collection_name, id=p_employee_id)
    return res['result']


#### 6. *Get Department Facet (Aggregation)*
# Define a function to retrieve the count of employees grouped by department:
# python
def getDepFacet(p_collection_name):
    query = {
        "size": 0,
        "aggs": {
            "departments": {
                "terms": {
                    "field": "Department.keyword"
                }
            }
        }
    }
    res = es.search(index=p_collection_name, body=query)
    return res['aggregations']['departments']['buckets']


### Step 4: Execute the Functions
# Follow the given order to execute the functions as per your assignment instructions:

python
# Define collection names
v_nameCollection = 'Hash_YourName'
v_phoneCollection = 'Hash_1234'  # Last 4 digits of your phone

# Create collections
createCollection(v_nameCollection)
createCollection(v_phoneCollection)

# Get employee count
print(f"Employee count in {v_nameCollection}: {getEmpCount(v_nameCollection)}")

# Index data, excluding certain columns
indexData(v_nameCollection, 'Department')
indexData(v_phoneCollection, 'Gender')

# Delete employee by ID
delEmpById(v_nameCollection, 'E02003')

# Get employee count after deletion
print(f"Employee count in {v_nameCollection} after deletion: {getEmpCount(v_nameCollection)}")

# Search by column
print(f"Search results by Department 'IT' in {v_nameCollection}: {searchByColumn(v_nameCollection, 'Department', 'IT')}")
print(f"Search results by Gender 'Male' in {v_nameCollection}: {searchByColumn(v_nameCollection, 'Gender', 'Male')}")
print(f"Search results by Department 'IT' in {v_phoneCollection}: {searchByColumn(v_phoneCollection, 'Department', 'IT')}")

# Get department facets
print(f"Department facet in {v_nameCollection}: {getDepFacet(v_nameCollection)}")
print(f"Department facet in {v_phoneCollection}: {getDepFacet(v_phoneCollection)}")


