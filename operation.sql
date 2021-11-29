CREATE TABLE if NOT EXISTS operation (
  client_id INT NOT NULL,
  type INTEGER NOT NULL,
  description TEXT NOT NULL,
  shet_from INT,
  shet_to INT,
  value REAL NOT NULL,
  op_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);