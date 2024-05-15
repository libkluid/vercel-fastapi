-- relate user metadata
-- SEE: https://supabase.com/docs/guides/auth/managing-user-data
CREATE TABLE public.profiles (
  id UUID NOT NULL REFERENCES auth.users on delete cascade,
  email TEXT NOT NULL,
  name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  valid_until TIMESTAMP WITH TIME ZONE,

  PRIMARY KEY (id)
);

alter table public.profiles enable row level security;

-- inserts a row into public.profiles
CREATE FUNCTION public.handle_new_user()
returns trigger
language plpgsql
security definer SET search_path = ''
AS $$
BEGIN
  INSERT INTO public.profiles (id, email, name, created_at)
  VALUES (new.id, new.email, 'USER', now());
  RETURN new;
END;
$$;

-- trigger the function every time a user is created
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  for each row execute procedure public.handle_new_user();

CREATE TABLE public.user_logs (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  uid TEXT NOT NULL,
  email TEXT NOT NULL,
  action TEXT NOT NULL,
  data JSON,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
