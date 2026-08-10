-- ============================================================
-- AGREGAR / RENOMBRAR a kilos (ejecutar en Supabase → SQL Editor)
-- Corrige: Could not find the 'kilos' column of 'despachos_papas'
-- ============================================================

-- Opción A (recomendada): renombrar la columna antigua "sacos" → "kilos"
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'despachos_papas'
      AND column_name = 'sacos'
  ) AND NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'despachos_papas'
      AND column_name = 'kilos'
  ) THEN
    ALTER TABLE public.despachos_papas RENAME COLUMN sacos TO kilos;
  END IF;
END $$;

-- Si no existía ni sacos ni kilos, crear kilos
ALTER TABLE public.despachos_papas
  ADD COLUMN IF NOT EXISTS kilos NUMERIC(12, 2);

-- Ajustar tipo y rellenar desde sacos si aún existiera las dos
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'despachos_papas'
      AND column_name = 'sacos'
  ) AND EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'despachos_papas'
      AND column_name = 'kilos'
  ) THEN
    UPDATE public.despachos_papas
    SET kilos = sacos::numeric
    WHERE kilos IS NULL AND sacos IS NOT NULL;
  END IF;
END $$;

-- Permitir decimales en kilos
ALTER TABLE public.despachos_papas
  ALTER COLUMN kilos TYPE NUMERIC(12, 2)
  USING COALESCE(kilos, 0)::numeric;

-- Comprobar columnas
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'despachos_papas'
ORDER BY ordinal_position;
