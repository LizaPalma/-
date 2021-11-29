CREATE TABLE if NOT EXISTS clients (
  client_id integer PRIMARY KEY,
  firstname text NOT NULL,
  lastname text NOT NULL,
  middlename text NOT NULL,
  city text NOT NULL,
  flag integer NOT NULL DEFAULT 0,
  UNIQUE (firstname, lastname, middlename, city));