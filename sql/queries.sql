-- 1. Список студий
SELECT id, name, area, price_per_hour FROM studios ORDER BY name;

-- 2. Студии с площадью не меньше заданной
SELECT id, name, area FROM studios WHERE area >= ? ORDER BY area;

-- 3. Студии дешевле заданной цены
SELECT id, name, price_per_hour FROM studios
WHERE price_per_hour <= ? ORDER BY price_per_hour;

-- 4. Активные бронирования
SELECT id, studio_id, user_id, booking_date, start_hour, end_hour
FROM bookings WHERE is_cancelled = 0 ORDER BY booking_date;

-- 5. Подробности активных бронирований с JOIN
SELECT b.id, b.booking_date, b.start_hour, b.end_hour,
       s.name AS studio_name, s.area, u.login AS user_login
FROM bookings AS b JOIN studios AS s ON b.studio_id = s.id
JOIN users AS u ON b.user_id = u.id
WHERE b.is_cancelled = 0 ORDER BY b.booking_date;

-- 6. Бронирования выбранной студии с JOIN
SELECT b.id, b.booking_date, s.name AS studio_name, u.login AS user_login
FROM bookings AS b JOIN studios AS s ON b.studio_id = s.id
JOIN users AS u ON b.user_id = u.id WHERE s.id = ?;

-- 7. Свободные студии на выбранную дату
SELECT s.id, s.name, s.area FROM studios AS s
WHERE NOT EXISTS (SELECT 1 FROM bookings AS b
  WHERE b.studio_id = s.id AND b.booking_date = ? AND b.is_cancelled = 0)
ORDER BY s.name;

-- 8. Свободные студии на дату с минимальной площадью
SELECT s.id, s.name, s.area FROM studios AS s
WHERE s.area >= ? AND NOT EXISTS (SELECT 1 FROM bookings AS b
  WHERE b.studio_id = s.id AND b.booking_date = ? AND b.is_cancelled = 0)
ORDER BY s.area;

-- 9. Общее число активных бронирований
SELECT COUNT(*) AS bookings_count FROM bookings WHERE is_cancelled = 0;

-- 10. Количество активных бронирований по студиям
SELECT s.name AS studio_name, COUNT(b.id) AS bookings_count
FROM studios AS s LEFT JOIN bookings AS b
ON s.id = b.studio_id AND b.is_cancelled = 0
GROUP BY s.id, s.name ORDER BY bookings_count DESC, s.name;

-- 11. Студии, где бронирований больше заданного количества
SELECT s.name AS studio_name, COUNT(b.id) AS bookings_count
FROM studios AS s LEFT JOIN bookings AS b
ON s.id = b.studio_id AND b.is_cancelled = 0
GROUP BY s.id, s.name HAVING COUNT(b.id) > ?;

-- 12. Средняя стоимость активной брони по студиям
SELECT s.name AS studio_name, AVG(b.total_price) AS average_price
FROM studios AS s JOIN bookings AS b ON s.id = b.studio_id
WHERE b.is_cancelled = 0 GROUP BY s.id, s.name;
