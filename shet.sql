CREATE TABLE if NOT EXISTS sheta (
  client_id integer NOT NULL,
  balance real not NULL DEFAULT 0.0,
  shet_num integer NOT NULL,
  iso text NOT NULL,
  block integer NOT NULL DEFAULT 0,
  FOREIGN KEY(client_id) REFERENCES clients(client_id)
  UNIQUE (client_id, shet_num, iso));