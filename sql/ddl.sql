-- relate user metadata
-- SEE: https://supabase.com/docs/guides/auth/managing-user-data
create table public.profiles (
  id uuid not null references auth.users on delete cascade,
  email text not null,
  name text,
  created_at timestamp with time zone default now(),

  primary key (id)
);

alter table public.profiles enable row level security;

-- inserts a row into public.profiles
create function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, email, name, created_at)
  values (new.id, new.email, 'USER', now());
  return new;
end;
$$;

-- trigger the function every time a user is created
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
