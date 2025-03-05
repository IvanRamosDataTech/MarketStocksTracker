-- Postgresql comes with dateformat as MDY by default (US style)
-- Specify euro style for date formats to avoid "values out of range". Format changes to ISO, DMY
SET datestyle = "ISO, DMY";
-- You could also specify by running:
-- set datestyle = euro;

-- Table: public.ppr

DROP TABLE IF EXISTS public.ppr;


CREATE TABLE public.ppr
(
    "Number" smallint NOT NULL,
    "Name" character varying(70) NOT NULL,
    "Ticker" character varying(10) NOT NULL,
    "Shares" real NOT NULL,
    "AverageUnitCost" real NOT NULL,
    "CurrentUnitCost" real NOT NULL,
    "PurchaseValue" real NOT NULL,
    "MarketValue" real NOT NULL,
    "ValueDifference" real NOT NULL,
    "ValueDifference%" real NOT NULL,
    "CurrentWeight" real NOT NULL,
    "DesiredWeight" real NOT NULL,
    "UploadDate" date,
    PRIMARY KEY ("Number")
);

ALTER TABLE IF EXISTS public.ppr
    OWNER to admin;

COMMENT ON TABLE public.ppr
    IS 'All history of capital contributions to Private pension Plan';

-- Table: public.indexed

DROP TABLE IF EXISTS public.indexed;


CREATE TABLE public.indexed
(
    "Number" smallint NOT NULL,
    "Name" character varying(70) NOT NULL,
    "Ticker" character varying(10) NOT NULL,
    "Shares" real NOT NULL,
    "AverageUnitCost" real NOT NULL,
    "CurrentUnitCost" real NOT NULL,
    "PurchaseValue" real NOT NULL,
    "MarketValue" real NOT NULL,
    "ValueDifference" real NOT NULL,
    "ValueDifference%" real NOT NULL,
    "CurrentWeight" real NOT NULL,
    "DesiredWeight" real NOT NULL,
    "UploadDate" date,
    PRIMARY KEY ("Number")
);

ALTER TABLE IF EXISTS public.indexed
    OWNER to admin;

COMMENT ON TABLE public.indexed
    IS 'All history of capital contributions to Indexed based investment strategy';