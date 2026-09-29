CREATE 
    (alice:Person {name: 'Alice', age: 25}), 
    (bob:Person {name: 'Bob', age: 28}), 
    (charlie:Person {name: 'Charlie', age: 24}), 
    (david:Person {name: 'David', age: 30}); 
 
MATCH 
    (alice:Person {name: 'Alice'}), 
    (bob:Person {name: 'Bob'}), 
    (charlie:Person {name: 'Charlie'}), 
    (david:Person {name: 'David'}) 
CREATE 
    (alice)-[:KNOWS]->(bob), 
    (alice)-[:KNOWS]->(charlie), 
    (bob)-[:KNOWS]->(david), 
    (charlie)-[:KNOWS]->(david); 
 
 
 Query to display the stored graph 
To display all nodes and their relationships in Neo4j Browser, execute: 
MATCH (n)-[r]->(m) 
RETURN n, r, m; 
 
To display all KNOWS relationships 
MATCH (a:Person)-[r:KNOWS]->(b:Person) RETURN a, r, b; 
