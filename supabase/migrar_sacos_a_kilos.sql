-- ============================================================
-- Quitar error: invalid input syntax for type integer: "4.0"
-- y renombrar a kilos (Supabase → SQL Editor → Run)
-- ============================================================

-- 1) Pasar la cantidad a decimal (permite 4.5 kg etc.)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'despachos_papas'
      AND column_name = 'sacos'
  ) THEN
    ALTER TABLE public.despachos_papas
      ALTER COLUMN sacos TYPE NUMERIC(12, 2)
      USING sacos::numeric;
  END IF;

  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'despachos_papas'
      AND column_name = 'kilos'
  ) THEN
    ALTER TABLE public.despachos_papas
      ALTER COLUMN kilos TYPE NUMERIC(12, 2)
      USING kilos::numeric;
  END IF;
END $$;

-- 2) Renombrar sacos → kilos si aún no existe kilos
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'despachos_papas'
      AND column_name = 'sacos'
  ) AND NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'despachos_papas'
      AND column_name = 'kilos'
  ) THEN
    ALTER TABLE public.despachos_papas RENAME COLUMN sacos TO kilos;
  END IF;
END $$;

-- 3) Si no hay columna de cantidad, crear kilos
ALTER TABLE public.despachos_papas
  ADD COLUMN IF NOT EXISTS kilos NUMERIC(12, 2);

-- Comprobar
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'despachos_papas'
ORDER BY ordinal_position;
