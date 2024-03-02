BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categoria" (
	"id"	INTEGER NOT NULL,
	"nombre"	VARCHAR NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "cliente" (
	"id"	INTEGER NOT NULL,
	"nombre"	VARCHAR NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "categoriacliente" (
	"id_categoria"	INTEGER NOT NULL,
	"id_cliente"	INTEGER NOT NULL,
	FOREIGN KEY("id_cliente") REFERENCES "cliente"("id"),
	FOREIGN KEY("id_categoria") REFERENCES "categoria"("id"),
	PRIMARY KEY("id_categoria","id_cliente")
);
CREATE TABLE IF NOT EXISTS "cuenta" (
	"id"	INTEGER NOT NULL,
	"id_cliente"	INTEGER NOT NULL,
	FOREIGN KEY("id_cliente") REFERENCES "cliente"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "movimiento" (
	"id"	INTEGER NOT NULL,
	"id_cuenta"	INTEGER NOT NULL,
	"tipo"	VARCHAR NOT NULL,
	"importe"	INTEGER NOT NULL,
	"fecha"	DATETIME NOT NULL,
	FOREIGN KEY("id_cuenta") REFERENCES "cuenta"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "categoria" VALUES (1,'Categoria 1');
INSERT INTO "categoria" VALUES (2,'Categoria 2');
INSERT INTO "categoria" VALUES (3,'Categoria 3');
INSERT INTO "categoria" VALUES (4,'Categoria 4');
INSERT INTO "categoria" VALUES (5,'Categoria 5');
INSERT INTO "cliente" VALUES (1,'Banza Root');
INSERT INTO "cliente" VALUES (2,'Viviana');
INSERT INTO "cliente" VALUES (3,'Estaban');
INSERT INTO "cliente" VALUES (4,'Nero');
INSERT INTO "cuenta" VALUES (1,1);
INSERT INTO "cuenta" VALUES (2,1);
INSERT INTO "cuenta" VALUES (3,2);
INSERT INTO "cuenta" VALUES (4,2);
INSERT INTO "cuenta" VALUES (5,3);
INSERT INTO "cuenta" VALUES (6,4);
INSERT INTO "cuenta" VALUES (7,4);
COMMIT;
