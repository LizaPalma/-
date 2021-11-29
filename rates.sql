CREATE TABLE if NOT EXISTS rates (
  cod_iso integer NOT NULL,
  iso text not null,
  unit integer NOT NULL,
  cur_name text NOT NULL,
  rate real NOT NULL,
  UNIQUE (cod_iso, iso));