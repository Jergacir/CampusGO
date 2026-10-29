ALTER TABLE usuario
    ADD COLUMN foto_url VARCHAR(500) NULL,
    ADD COLUMN foto_public_id VARCHAR(255) NULL;

ALTER TABLE conductor
    ADD COLUMN marca_auto VARCHAR(80) NULL,
    ADD COLUMN modelo_auto VARCHAR(80) NULL,
    ADD COLUMN placa_auto VARCHAR(20) NULL,
    ADD COLUMN color_auto VARCHAR(40) NULL,
    ADD COLUMN foto_auto_url VARCHAR(500) NULL,
    ADD COLUMN foto_auto_public_id VARCHAR(255) NULL;

ALTER TABLE viaje
    ADD COLUMN marca_auto VARCHAR(80) NULL,
    ADD COLUMN modelo_auto VARCHAR(80) NULL,
    ADD COLUMN placa_auto VARCHAR(20) NULL,
    ADD COLUMN color_auto VARCHAR(40) NULL,
    ADD COLUMN foto_auto_url VARCHAR(500) NULL;