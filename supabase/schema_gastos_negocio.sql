-- Tabla de gastos del negocio (papas, transporte, personal, etc.)
-- Ejecutar en Supabase → SQL Editor (después de schema_despachos_papas.sql)

create table if not exists public.gastos_negocio (
  id bigserial primary key,
  semana text not null,
  dia text not null,
  categoria text not null,
  concepto text not null default '',
  monto numeric(12, 2) not null check (monto > 0),
  creado_en timestamptz not null default timezone('utc', now())
);

create index if not exists gastos_negocio_semana_idx
  on public.gastos_negocio (semana);

create index if not exists gastos_negocio_semana_dia_idx
  on public.gastos_negocio (semana, dia);

alter table public.gastos_negocio disable row level security;
