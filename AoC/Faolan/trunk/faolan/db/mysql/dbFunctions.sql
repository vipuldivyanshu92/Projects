delimiter //
Create function LoginConnect (pusername VARCHAR(50), pcookie INT) returns BOOL
BEGIN
  DECLARE NbCompte TINYINT;
  SELECT Count(*) INTO NbCompte FROM Accounts WHERE username = pusername;
  IF (NbCompte > 0) THEN
    UPDATE Accounts SET last_connection = NOW(), cookie = pcookie WHERE username = pusername;
    RETURN TRUE;
  ELSE
    RETURN FALSE;
  END IF;
END;
//