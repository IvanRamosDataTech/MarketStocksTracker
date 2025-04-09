-- Postgresql comes with dateformat as MDY by default (US style)
-- Specify euro style for date formats to avoid "values out of range". Format changes to ISO, DMY
SET datestyle = "ISO, DMY";
-- You could also specify by running:
-- set datestyle = euro;

-- Table: public.ppr

DROP TABLE IF EXISTS public.ppr;


CREATE TABLE public.ppr
(
    "Number" character varying(10) NOT NULL,
    "Name" character varying(70),
    "Ticker" character varying(10),
    "Shares" real,
    "Average Unit Cost" real,
    "Current Unit Cost" real,
    "Purchased Value" numeric(15,2) NOT NULL,
    "Market Value" numeric(15,2) NOT NULL,
    "Balance" numeric(15,2) NOT NULL,
    "Balance %" numeric(5,4) NOT NULL,
    "Current Weight %" numeric(5,4) NOT NULL,
    "Target Weight %" numeric(5,4) NOT NULL,
    "Statement Date" date,
    "Snapshot ID" integer NOT NULL,
    "Snapshot Timestamp" Timestamp
);

ALTER TABLE IF EXISTS public.ppr
    OWNER to admin;

COMMENT ON TABLE public.ppr
    IS 'All history of capital contributions to Private pension Plan';

-- Table: public.indexed

DROP TABLE IF EXISTS public.indexed;


CREATE TABLE public.indexed
(
    "Number" character varying(10) NOT NULL,
    "Name" character varying(70),
    "Ticker" character varying(10),
    "Shares" real,
    "To Buy" real,
    "Average Unit Cost" real,
    "Potential Average Unit Cost" real,
    "Current Unit Cost" real,
    "Unit Cost Diff %" numeric(5,4),
    "Purchased Value" numeric(15,2) NOT NULL,
    "Market Value" numeric(15,2) NOT NULL,
    "Potential Market Value" numeric(15,2) NOT NULL,
    "Balance" numeric(15,2) NOT NULL,
    "Balance %" numeric(5,4) NOT NULL,
    "Current Weight %" numeric(5,4) NOT NULL,
    "Potential Weight %" numeric(5,4),
    "Target Weight %" numeric(5,4) NOT NULL,
    "Snapshot ID" integer NOT NULL,
    "Snapshot Timestamp" Timestamp
);

ALTER TABLE IF EXISTS public.indexed
    OWNER to admin;

COMMENT ON TABLE public.indexed
    IS 'All history of capital contributions to Indexed based investment strategy';