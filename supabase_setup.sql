-- Run this once in Supabase -> SQL Editor -> New query -> Run.
-- It creates the table your bot writes into. Each note becomes one row.

create table brain_files (
  path text primary key,
  content text not null,
  updated_at timestamptz default now()
);
