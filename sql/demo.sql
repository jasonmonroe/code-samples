
/* ----------:::  Scripts for PostgreSQL DATABASE  :::---------- */
DROP DATABASE IF EXISTS demo;
CREATE DATABASE demo;
USE demo;


drop table IF EXISTS warehouse;
CREATE TABLE warehouse
(
	id 						VARCHAR(10),
	on_hand_quantity			INT,
	on_hand_quantity_delta		INT,
	event_type				VARCHAR(10),
	event_datetime			TIMESTAMP
);

INSERT INTO warehouse VALUES
('SH0013', 278,   99 ,   'OutBound', '2020-05-25 0:25'),
('SH0012', 377,   31 ,   'InBound',  '2020-05-24 22:00'),
('SH0011', 346,   1  ,   'OutBound', '2020-05-24 15:01'),
('SH0010', 346,   1  ,   'OutBound', '2020-05-23 5:00'),
('SH009',  348,   102,   'InBound',  '2020-04-25 18:00'),
('SH008',  246,   43 ,   'InBound',  '2020-04-25 2:00'),
('SH007',  203,   2  ,   'OutBound', '2020-02-25 9:00'),
('SH006',  205,   129,   'OutBound', '2020-02-18 7:00'),
('SH005',  334,   1  ,   'OutBound', '2020-02-18 8:00'),
('SH004',  335,   27 ,   'OutBound', '2020-01-29 5:00'),
('SH003',  362,   120,   'InBound',  '2019-12-31 2:00'),
('SH002',  242,   8  ,   'OutBound', '2019-05-22 0:50'),
('SH001',  250,   250,   'InBound',  '2019-05-20 0:45');
COMMIT;


WITH WH AS
    (
        SELECT *
        FROM warehouse
        ORDER BY event_datetime DESC
    ),
	days AS
		(
		    SELECT event_datetime, on_hand_quantity,
            DATE_SUB(event_datetime, INTERVAL 90 DAY) AS day90,
            DATE_SUB(event_datetime, INTERVAL 180 DAY) AS day180,
            DATE_SUB(event_datetime, INTERVAL 270 DAY) AS day270,
            DATE_SUB(event_datetime, INTERVAL 365 DAY) AS day365
            FROM WH
            LIMIT 1
        ),
	inv_90_days AS
		(
		    SELECT COALESCE(SUM(WH.on_hand_quantity_delta), 0) AS days_old_90  /* Get the total InBound inventories in the last 90 days */
		    FROM WH CROSS JOIN days
		    WHERE WH.event_datetime >= days.day90
		    AND event_type = 'InBound'
        ),
	inv_90_days_final AS
		(
		    SELECT CASE WHEN days_old_90 > on_hand_quantity THEN on_hand_quantity  /* If InBound inventories is greater than curent total inventories THEN curent total inventories is the remaining inventories */
			ELSE days_old_90
	   		END AS days_old_90
		    FROM inv_90_days x
		    CROSS JOIN days
        ),
	inv_180_days AS
		(
		    SELECT COALESCE(SUM(WH.on_hand_quantity_delta), 0) AS days_old_180  /* Get the total InBound inventories BETWEEN the last 90 AND 180 days */
		    FROM WH CROSS JOIN days
		    WHERE WH.event_datetime BETWEEN days.day180 AND days.day90
		    AND event_type = 'InBound'
        ),
	inv_180_days_final as
		(
		    SELECT CASE WHEN days_old_180 > (on_hand_quantity - days_old_90) THEN (on_hand_quantity - days_old_90)
			ELSE days_old_180
	   		END AS days_old_180
            FROM inv_180_days x
            CROSS JOIN days
            CROSS JOIN inv_90_days_final
        ),
	inv_270_days AS
		(
		    SELECT COALESCE(SUM(WH.on_hand_quantity_delta), 0) AS days_old_270  /* Get the total InBound inventories BETWEEN the last 180 AND 270 days */
		    FROM WH CROSS JOIN days
		    WHERE WH.event_datetime BETWEEN days.day270 AND days.day180
 		    AND event_type = 'InBound'
        ),
	inv_270_days_final AS
		(
		    SELECT CASE
		        WHEN days_old_270 > (on_hand_quantity - (days_old_90 + days_old_180))
                THEN (on_hand_quantity - (days_old_90 + days_old_180))
			ELSE days_old_270
	   		    END AS days_old_270
            FROM inv_270_days x
            CROSS JOIN days
            CROSS JOIN inv_90_days_final
            CROSS JOIN inv_180_days_final
        ),
	inv_365_days AS
		(
		    SELECT COALESCE(SUM(WH.on_hand_quantity_delta), 0) AS days_old_365  /* Get the total InBound inventories BETWEEN the last 270 AND 365 days */
		    FROM WH CROSS JOIN days
		    WHERE WH.event_datetime BETWEEN days.day365 AND days.day270
		    AND event_type = 'InBound'
        ),
	inv_365_days_final AS
		(
		    SELECT CASE WHEN days_old_365 > (on_hand_quantity - (days_old_90 + days_old_180 + days_old_270)) THEN (on_hand_quantity - (days_old_90 + days_old_180 + days_old_270))
			ELSE days_old_365
	   		END AS days_old_365
            FROM inv_365_days x
            CROSS JOIN days
            CROSS JOIN inv_90_days_final
            CROSS JOIN inv_180_days_final
            CROSS JOIN inv_270_days_final
        )

SELECT days_old_90 AS 0_to_90_days_old, days_old_180 AS 91_180_days_old, days_old_270 AS 181_270_days_old, days_old_365 AS 271_365_days_old
FROM inv_90_days_final
CROSS JOIN inv_180_days_final
CROSS JOIN inv_270_days_final
CROSS JOIN inv_365_days_final
CROSS JOIN days;


