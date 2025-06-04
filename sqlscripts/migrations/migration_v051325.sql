-- Migration 051325
-- Date: 2023-10-25


-- Add column "Current Unit Cost (Original)" to table "indexed"
ALTER TABLE public.indexed ADD column "Current Unit Cost (Original)" real;

-- Rename potential market value to Potential purchased value
ALTER TABLE public.indexed RENAME COLUMN "Potential Market Value" TO "Potential Purchased Value";
