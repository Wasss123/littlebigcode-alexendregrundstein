# Test 2 - SQL

### Requête 1 - Trouver le chiffre d'affaires jour par jour du 1er janvier 2019 au 31 décembre 2019

SELECT date, SUM(prod_price*prod_qty) as ventes FROM transactions WHERE STR_TO_DATE(date,'%d/%m/%Y’) BETWEEN ‘2019-01-01’ AND ‘2019-12-31’ GROUP BY date ORDER BY date


### Requête 2 - Déterminer, par client et sur la période allant du 1er janvier 2019 au 31 décembre 2019, les ventes meuble et déco réalisées
* Commentaires : j'ai programmé cette requête sur mySQL. Or, le FULL JOIN n'existant pas sur mySQL, j'ai dû passer par un UNION d'une requête LEFT JOIN et d'une requête RIGHT JOIN.


`(SELECT COALESCE(C.client_id, D.client_id) as client_id, ventes_meuble, ventes_deco`
`FROM`
(SELECT client_id, SUM(prod_price*prod_qty) as ventes_meuble FROM (SELECT * FROM transactions) AS A INNER JOIN (SELECT * FROM product_nomenclature) AS B ON A.prod_id=B.product_id WHERE product_type='MEUBLE' AND STR_TO_DATE(date,'%d/%m/%Y') BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY client_id) AS C 
LEFT JOIN 
(SELECT client_id, SUM(prod_price*prod_qty) as ventes_deco FROM (SELECT * FROM transactions) AS A INNER JOIN (SELECT * FROM product_nomenclature) AS B ON A.prod_id=B.product_id WHERE product_type='DECO' AND STR_TO_DATE(date,'%d/%m/%Y') BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY client_id) AS D 
ON C.client_id=D.client_id)

UNION

(SELECT COALESCE(C.client_id, D.client_id) as client_id, ventes_meuble, ventes_deco 
FROM 
(SELECT client_id, SUM(prod_price*prod_qty) as ventes_meuble FROM (SELECT * FROM transactions) AS A INNER JOIN (SELECT * FROM product_nomenclature) AS B ON A.prod_id=B.product_id WHERE product_type='MEUBLE' AND STR_TO_DATE(date,'%d/%m/%Y') BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY client_id) AS C 
RIGHT JOIN 
(SELECT client_id, SUM(prod_price*prod_qty) as ventes_deco FROM (SELECT * FROM transactions) AS A INNER JOIN (SELECT * FROM product_nomenclature) AS B ON A.prod_id=B.product_id WHERE product_type='DECO' AND STR_TO_DATE(date,'%d/%m/%Y') BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY client_id) AS D 
ON C.client_id=D.client_id)


