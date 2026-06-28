# Supabase setup

Cloud accounts and progress sync are optional. With no Supabase configuration, the app starts immediately in guest mode and saves progress in browser local storage.

## 1. Create and configure a project

1. Create a Supabase project.
2. Open **SQL Editor** and run [supabase/schema.sql](../supabase/schema.sql).
3. Under **Authentication → URL Configuration**, add the live app URL as a redirect URL.
4. Enable Email authentication. Email/password and magic-link flows use Supabase Auth.
5. Copy the project URL and the public anon key from the project API settings.
6. Put only those two public values in `supabase-config.js`.

```js
window.FRCPathSupabaseConfig = Object.freeze({
  url: "https://YOUR_PROJECT_REF.supabase.co",
  anonKey: "YOUR_PUBLIC_ANON_KEY"
});
```

A blank configuration is valid and leaves the app in guest-only mode.

## 2. Security model

Progress is stored in `public.user_progress` with `user_id uuid` as the primary key. The value comes from the authenticated Supabase user ID. Email addresses are not used as row identifiers and are not written into the progress or analytics tables.

Row Level Security is enabled on:

- `user_progress`: authenticated users can select, insert, update, or delete only their own row.
- `question_attempts`: authenticated users can select, insert, or update only rows matching their own user ID.
- `app_admins`: users can only see whether their own UUID is an administrator.

The frontend records aggregate question attempts through `record_question_attempt`. The admin dashboard calls `get_admin_dashboard`, a guarded database function that rejects every authenticated user whose UUID is absent from `app_admins`.

## 3. Assign the administrator

Create your own account through the app, then copy its user UUID from **Authentication → Users**. Run this in the SQL editor, replacing the placeholder UUID:

```sql
insert into public.app_admins (user_id)
values ('00000000-0000-0000-0000-000000000000');
```

Use the UUID only. Do not put an administrator email address in the repository or frontend configuration.

## 4. Guest import and sync behavior

- Guests can use the full app without an account.
- Guest progress remains in browser local storage.
- At first sign-in, the app offers to merge local guest progress into the cloud row.
- Bookmarks, study answers, exam history, notes, and sound preference are synchronized.
- Signing out restores the guest snapshot for that browser session when one is available.
- Admin analytics count attempts recorded while users are signed in.

## Safe and unsafe values

Safe to commit publicly:

- Supabase project URL.
- Supabase public anon key.
- Table names, SQL migrations, and RLS policies.
- Placeholder UUIDs and configuration examples.

Never commit:

- Service-role keys.
- Supabase secret keys.
- Database passwords or connection strings containing passwords.
- User passwords, magic-link tokens, access tokens, refresh tokens, private API keys, or personal email addresses.

The anon key is intentionally restricted by RLS. Never weaken the policies to compensate for a frontend error.
