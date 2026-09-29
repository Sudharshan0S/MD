CREATE 
    (alice:Person {name: 'Alice'}), 
    (bob:Person {name: 'Bob'}), 
    (charlie:Person {name: 'Charlie'}), 
 
    (phone:Product {name: 'Smartphone', price: 50000}), 
    (laptop:Product {name: 'Laptop', price: 70000}), 
    (headphones:Product {name: 'Headphones', price: 3000}), 
    (tablet:Product {name: 'Tablet', price: 25000}), 
    (camera:Product {name: 'Camera', price: 45000}), 
 
    (alice)-[:PURCHASED]->(phone), 
    (alice)-[:PURCHASED]->(headphones), 
 
    (bob)-[:PURCHASED]->(laptop), 
    (bob)-[:PURCHASED]->(camera), 
 
    (charlie)-[:PURCHASED]->(tablet), 
    (charlie)-[:PURCHASED]->(headphones), 
 
    (phone)-[:SIMILAR_TO]->(tablet), 
    (laptop)-[:SIMILAR_TO]->(camera), 
    (headphones)-[:SIMILAR_TO]->(phone), 
(camera)-[:SIMILAR_TO]->(laptop); 
2.List the items purchased by Alice 
MATCH (a:Person {name: 'Alice'})-[:PURCHASED]->(p:Product) 
RETURN p.name AS Product, p.price AS Price; 
3: Find the total spending per person 
MATCH (person:Person)-[:PURCHASED]->(product:Product) 
RETURN person.name AS Person, 
SUM(product.price) AS TotalSpending 
ORDER BY TotalSpending DESC; 
4: Recommend a product to the user 
MATCH (a:Person {name: 'Alice'})-[:PURCHASED]->(p:Product) 
MATCH (p)-[:SIMILAR_TO]->(recommended:Product) 
WHERE NOT (a)-[:PURCHASED]->(recommended) 
RETURN DISTINCT recommended.name AS RecommendedProduct;
