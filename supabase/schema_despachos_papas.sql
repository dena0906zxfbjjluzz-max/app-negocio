-- ============================================================
-- Control de Papas y Pollerías — tabla de despachos
-- Pegar en Supabase → SQL Editor → Run
-- Proyecto: puede ser el mismo trazabilidad-prod u otro nuevo
-- ============================================================

CREATE TABLE IF NOT EXISTS public.despachos_papas (
    id              BIGSERIAL PRIMARY KEY,
    semana          TEXT NOT NULL,
    dia             TEXT NOT NULL,
    cliente         TEXT NOT NULL,
    kilos           NUMERIC(12, 2) NOT NULL CHECK (kilos > 0),
    precio          NUMERIC(12, 2) NOT NULL DEFAULT 0,
    estado          TEXT NOT NULL DEFAULT 'Pagado en efectivo',
    creado_en       TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    actualizado_en  TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- Índices útiles para filtros semanales
CREATE INDEX IF NOT EXISTS idx_despachos_papas_semana
    ON public.despachos_papas (semana);

CREATE INDEX IF NOT EXISTS idx_despachos_papas_semana_dia
    ON public.despachos_papas (semana, dia);

-- MVP: Streamlit inserta/actualiza con la key del proyecto
-- (si luego quiere seguridad por usuario, se activa RLS y políticas)
ALTER TABLE public.despachos_papas DISABLE ROW LEVEL SECURITY;

-- Comprobar que la tabla quedó bien
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'despachos_papas'
ORDER BY ordinal_position;
