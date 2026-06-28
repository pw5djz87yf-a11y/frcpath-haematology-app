-- Run this file in the Supabase SQL editor.
-- The browser uses only the public anon key. Never expose a service-role or secret key.

create table if not exists public.user_progress (
  user_id uuid primary key references auth.users(id) on delete cascade,
  progress jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.question_attempts (
  user_id uuid not null references auth.users(id) on delete cascade,
  question_code text not null check (question_code ~ '^AML[0-9]{3,}$'),
  attempts integer not null default 0 check (attempts >= 0),
  correct integer not null default 0 check (correct >= 0 and correct <= attempts),
  last_attempt_at timestamptz not null default now(),
  primary key (user_id, question_code)
);

create table if not exists public.app_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public.user_progress enable row level security;
alter table public.question_attempts enable row level security;
alter table public.app_admins enable row level security;

drop policy if exists "Users read own progress" on public.user_progress;
create policy "Users read own progress"
on public.user_progress for select
to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users insert own progress" on public.user_progress;
create policy "Users insert own progress"
on public.user_progress for insert
to authenticated
with check ((select auth.uid()) = user_id);

drop policy if exists "Users update own progress" on public.user_progress;
create policy "Users update own progress"
on public.user_progress for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

drop policy if exists "Users delete own progress" on public.user_progress;
create policy "Users delete own progress"
on public.user_progress for delete
to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users read own attempts" on public.question_attempts;
create policy "Users read own attempts"
on public.question_attempts for select
to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "Users insert own attempts" on public.question_attempts;
create policy "Users insert own attempts"
on public.question_attempts for insert
to authenticated
with check ((select auth.uid()) = user_id);

drop policy if exists "Users update own attempts" on public.question_attempts;
create policy "Users update own attempts"
on public.question_attempts for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

drop policy if exists "Users see own admin membership" on public.app_admins;
create policy "Users see own admin membership"
on public.app_admins for select
to authenticated
using ((select auth.uid()) = user_id);

create or replace function public.record_question_attempt(
  p_question_code text,
  p_was_correct boolean
)
returns void
language plpgsql
security invoker
set search_path = public
as $$
declare
  requesting_user uuid := auth.uid();
begin
  if requesting_user is null then
    raise exception 'Authentication required';
  end if;
  if p_question_code !~ '^AML[0-9]{3,}$' then
    raise exception 'Invalid question code';
  end if;

  insert into public.question_attempts (
    user_id,
    question_code,
    attempts,
    correct,
    last_attempt_at
  )
  values (
    requesting_user,
    upper(p_question_code),
    1,
    case when p_was_correct then 1 else 0 end,
    now()
  )
  on conflict (user_id, question_code) do update
  set attempts = public.question_attempts.attempts + 1,
      correct = public.question_attempts.correct +
        case when excluded.correct = 1 then 1 else 0 end,
      last_attempt_at = now();
end;
$$;

revoke all on function public.record_question_attempt(text, boolean) from public;
revoke all on function public.record_question_attempt(text, boolean) from anon;
grant execute on function public.record_question_attempt(text, boolean) to authenticated;

create or replace function public.get_admin_dashboard()
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, public, auth
as $$
declare
  requesting_user uuid := auth.uid();
  result jsonb;
begin
  if requesting_user is null or not exists (
    select 1 from public.app_admins where user_id = requesting_user
  ) then
    raise exception 'Administrator access required';
  end if;

  select jsonb_build_object(
    'total_users', (select count(*) from auth.users),
    'total_questions_answered', (
      select coalesce(sum(attempts), 0) from public.question_attempts
    ),
    'active_users', (
      select count(distinct user_id)
      from public.question_attempts
      where last_attempt_at >= now() - interval '30 days'
    ),
    'difficult_questions', coalesce((
      select jsonb_agg(to_jsonb(difficult) order by difficult.accuracy_percent, difficult.attempts desc)
      from (
        select
          question_code,
          sum(attempts)::integer as attempts,
          round(100.0 * sum(correct) / nullif(sum(attempts), 0), 1) as accuracy_percent
        from public.question_attempts
        group by question_code
        order by accuracy_percent asc, attempts desc
        limit 10
      ) difficult
    ), '[]'::jsonb)
  )
  into result;

  return result;
end;
$$;

revoke all on function public.get_admin_dashboard() from public;
revoke all on function public.get_admin_dashboard() from anon;
grant execute on function public.get_admin_dashboard() to authenticated;

-- After creating your own Auth account, copy its UUID from Authentication > Users.
-- Replace the placeholder below with that UUID. Do not use an email address.
-- insert into public.app_admins (user_id)
-- values ('00000000-0000-0000-0000-000000000000');
