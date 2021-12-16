use tempdata;
delimiter $$
CREATE TRIGGER H1N1_alert BEFORE INSERT ON tempdata.flu_vaccines
FOR EACH ROW
BEGIN
IF NEW.h1n1_concern <= 3 THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'ERROR: H1N1 concern should be a numerical value between 0 and 3. Please try again.';
END IF ;
END ; $$
delimiter ;