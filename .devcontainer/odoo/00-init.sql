CREATE ROLE openerp PASSWORD 'S3GT1mbC0XdqQONOzO4HP8XdUXuy0jwx-NMZuBS6QUE79E7AoYMPLnDpOCuAOHxy' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;

CREATE database openerp;

ALTER DATABASE openerp OWNER TO openerp;

CREATE database giustizia;

ALTER DATABASE giustizia OWNER TO openerp;
