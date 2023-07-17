/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...
-- SELECT c.name, COUNT(f.film_id) AS film_count
-- FROM Category c
-- JOIN film_category fc ON c.category_id = fc.category_id
-- JOIN Film f ON fc.film_id = f.film_id
-- GROUP BY c.name
-- ORDER BY film_count DESC;

SELECT
    c.name,
    COUNT(fc.film_id) AS film_count
FROM
    Category c
JOIN
    film_category fc ON c.category_id = fc.category_id
GROUP BY
    c.name
ORDER BY
    film_count DESC;


/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...
SELECT
    actor.actor_id,
    actor.first_name,
    actor.last_name,
    COUNT(rental.rental_id) AS rental_count
FROM
    actor
JOIN
    film_actor ON actor.actor_id = film_actor.actor_id
JOIN
    film ON film_actor.film_id = film.film_id
JOIN
    inventory ON film.film_id = inventory.film_id
JOIN
    rental ON inventory.inventory_id = rental.inventory_id
GROUP BY
    actor.actor_id,
    actor.first_name,
    actor.last_name
ORDER BY
    rental_count DESC
LIMIT 10;


/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...
SELECT
    c.name AS category_name,
    SUM(p.amount) AS total_amount
FROM
    Category c
JOIN
    film_category fc ON c.category_id = fc.category_id
JOIN
    film f ON fc.film_id = f.film_id
JOIN
    inventory i ON f.film_id = i.film_id
JOIN
    rental r ON i.inventory_id = r.inventory_id
JOIN
    payment p ON r.rental_id = p.rental_id
GROUP BY
    c.name
ORDER BY
    total_amount DESC
LIMIT 1;


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...
SELECT
    f.film_id,
    f.title AS film_title
FROM
    film f
LEFT JOIN
    inventory i ON f.film_id = i.film_id
WHERE
    i.inventory_id IS NULL

/*
5.
    Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
SELECT
    a.actor_id,
    a.first_name,
    a.last_name,
    COUNT(*) AS film_count
FROM
    actor a
JOIN
    film_actor fa ON a.actor_id = fa.actor_id
JOIN
    film f ON fa.film_id = f.film_id
JOIN
    film_category fc ON f.film_id = fc.film_id
JOIN
    category c ON fc.category_id = c.category_id
WHERE
    c.name = 'Children'
GROUP BY
    a.actor_id,
    a.first_name,
    a.last_name
ORDER BY
    film_count DESC
LIMIT 3;
