-- REVERSE
-- Migration 051325
-- Date: 2023-10-25


-- Drop column "Current Unit Cost (Original)" from table "indexed"
ALTER TABLE public.indexed DROP COLUMN "Current Unit Cost (Original)";

-- Rename potential purchased value to Potential market value
ALTER TABLE public.indexed RENAME COLUMN "Potential Purchased Value" TO "Potential Market Value";