-- Si la tabla ya existía con columna "sacos", ejecuta esto en Supabase SQL Editor:
ALTER TABLE public.despachos_papas
    RENAME COLUMN sacos TO kilos;

-- Permitir decimales (ej. 12.5 kg)
ALTER TABLE public.despachos_papas
    ALTER COLUMN kilos TYPE NUMERIC(12, 2)
    USING kilos::numeric;
