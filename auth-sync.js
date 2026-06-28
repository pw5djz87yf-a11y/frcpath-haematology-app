(function () {
  "use strict";

  const LOCAL_STATE_KEY = "frcpath_haem_state";
  const GUEST_BACKUP_KEY = "frcpath_guest_progress_backup";
  const IMPORT_OFFER_PREFIX = "frcpath_import_offered_";
  let client = null;
  let currentUser = null;
  let syncTimer = null;
  let applyingCloudState = false;

  function isConfigured() {
    const config = window.FRCPathSupabaseConfig || {};
    return Boolean(
      window.supabase &&
      typeof config.url === "string" &&
      /^https:\/\/[^/]+\.supabase\.co$/i.test(config.url) &&
      typeof config.anonKey === "string" &&
      config.anonKey.length > 20
    );
  }

  function currentProgress() {
    return {
      bookmarks: Array.isArray(appState.bookmarks) ? appState.bookmarks : [],
      studyProgress: appState.studyProgress || {},
      examHistory: Array.isArray(appState.examHistory) ? appState.examHistory : [],
      notes: appState.notes || {},
      soundEnabled: appState.soundEnabled !== false
    };
  }

  function hasMeaningfulProgress(progress) {
    if (!progress) return false;
    return Boolean(
      (progress.bookmarks || []).length ||
      Object.keys(progress.studyProgress || {}).length ||
      (progress.examHistory || []).length ||
      Object.values(progress.notes || {}).some(note => String(note).trim())
    );
  }

  function parseLocalProgress() {
    try {
      return JSON.parse(localStorage.getItem(LOCAL_STATE_KEY) || "null");
    } catch (error) {
      console.warn("Local progress could not be read:", error);
      return null;
    }
  }

  function blankProgress() {
    return {
      bookmarks: [],
      studyProgress: {},
      examHistory: [],
      notes: {},
      soundEnabled: appState.soundEnabled !== false
    };
  }

  function mergeProgress(cloud, local) {
    const examByDate = new Map();
    [...(cloud?.examHistory || []), ...(local?.examHistory || [])].forEach(exam => {
      examByDate.set(String(exam.date || JSON.stringify(exam)), exam);
    });

    return {
      bookmarks: [...new Set([...(cloud?.bookmarks || []), ...(local?.bookmarks || [])])],
      studyProgress: { ...(cloud?.studyProgress || {}), ...(local?.studyProgress || {}) },
      examHistory: [...examByDate.values()].sort((a, b) => (a.date || 0) - (b.date || 0)),
      notes: { ...(cloud?.notes || {}), ...(local?.notes || {}) },
      soundEnabled: local?.soundEnabled ?? cloud?.soundEnabled ?? true
    };
  }

  function applyProgress(progress) {
    const safe = progress || blankProgress();
    applyingCloudState = true;
    appState.bookmarks = Array.isArray(safe.bookmarks) ? safe.bookmarks : [];
    appState.studyProgress = safe.studyProgress || {};
    appState.examHistory = Array.isArray(safe.examHistory) ? safe.examHistory : [];
    appState.notes = safe.notes || {};
    appState.soundEnabled = safe.soundEnabled !== false;
    localStorage.setItem(LOCAL_STATE_KEY, JSON.stringify(currentProgress()));
    applyingCloudState = false;

    updateSoundToggle();
    if (appState.currentTab === "dashboard") renderDashboard();
    if (appState.currentTab === "study") renderStudyQuestion();
    if (appState.currentTab === "qbank") renderQBank();
    if (appState.currentTab === "bookmarks") renderBookmarks();
  }

  function updateAccountUi() {
    const accountButton = document.getElementById("account-button");
    const guestPanel = document.getElementById("auth-guest-panel");
    const userPanel = document.getElementById("auth-user-panel");
    const syncStatus = document.getElementById("user-sync-status");
    if (!accountButton || !guestPanel || !userPanel) return;

    const configured = isConfigured();
    document.getElementById("auth-config-message").classList.toggle("hidden", configured);
    guestPanel.classList.toggle("hidden", Boolean(currentUser));
    userPanel.classList.toggle("hidden", !currentUser);

    if (currentUser) {
      accountButton.textContent = "Cloud Account";
      accountButton.classList.add("border-emerald-400/60", "text-emerald-200");
      document.getElementById("auth-user-id").textContent =
        currentUser.id.slice(0, 8) + "…" + currentUser.id.slice(-4);
      if (syncStatus) syncStatus.textContent = "Cloud sync active";
    } else {
      accountButton.textContent = "Guest Mode";
      accountButton.classList.remove("border-emerald-400/60", "text-emerald-200");
      if (syncStatus) syncStatus.textContent = configured ? "Saved on this device" : "Local guest storage";
    }
  }

  function setAuthMessage(message, isError) {
    const element = document.getElementById("auth-message");
    if (!element) return;
    element.textContent = message || "";
    element.className = isError
      ? "text-xs text-rose-600 min-h-5"
      : "text-xs text-emerald-700 min-h-5";
  }

  function credentials() {
    return {
      email: document.getElementById("auth-email").value.trim(),
      password: document.getElementById("auth-password").value
    };
  }

  function requireConfigured() {
    if (client) return true;
    setAuthMessage("Cloud login is not configured yet. Guest mode remains fully available.", true);
    return false;
  }

  async function fetchCloudProgress() {
    const { data, error } = await client
      .from("user_progress")
      .select("progress")
      .eq("user_id", currentUser.id)
      .maybeSingle();
    if (error) throw error;
    return data?.progress || null;
  }

  async function uploadProgress(progress) {
    if (!client || !currentUser) return;
    const { error } = await client.from("user_progress").upsert({
      user_id: currentUser.id,
      progress,
      updated_at: new Date().toISOString()
    });
    if (error) throw error;
  }

  async function handleSignedInUser(user) {
    currentUser = user;
    updateAccountUi();

    const local = parseLocalProgress();
    const cloud = await fetchCloudProgress();
    const offeredKey = IMPORT_OFFER_PREFIX + user.id;
    const shouldOffer = hasMeaningfulProgress(local) && localStorage.getItem(offeredKey) !== "yes";

    if (shouldOffer) {
      const importGuest = window.confirm(
        "Import and merge the progress saved in this browser into your cloud account? " +
        "Choose Cancel to use existing cloud progress instead."
      );
      localStorage.setItem(offeredKey, "yes");
      if (importGuest) {
        const merged = mergeProgress(cloud, local);
        await uploadProgress(merged);
        applyProgress(merged);
        showToast("Local progress imported into your cloud account.", "success");
      } else {
        applyProgress(cloud || blankProgress());
      }
    } else if (cloud) {
      applyProgress(cloud);
    } else {
      await uploadProgress(currentProgress());
    }

    await loadAdminDashboard();
  }

  async function init() {
    updateAccountUi();
    if (!isConfigured()) return;

    const config = window.FRCPathSupabaseConfig;
    client = window.supabase.createClient(config.url, config.anonKey, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true
      }
    });

    const { data, error } = await client.auth.getSession();
    if (error) {
      setAuthMessage(error.message, true);
      return;
    }

    client.auth.onAuthStateChange((_event, session) => {
      window.setTimeout(async () => {
        try {
          if (session?.user && session.user.id !== currentUser?.id) {
            await handleSignedInUser(session.user);
          } else if (!session?.user) {
            currentUser = null;
            updateAccountUi();
          }
        } catch (authError) {
          console.error("Auth state update failed:", authError);
          setAuthMessage(authError.message, true);
        }
      }, 0);
    });

    if (data.session?.user) {
      await handleSignedInUser(data.session.user);
    }
  }

  async function signUp() {
    if (!requireConfigured()) return;
    const { email, password } = credentials();
    if (!email || password.length < 8) {
      setAuthMessage("Enter a valid email and a password of at least 8 characters.", true);
      return;
    }
    sessionStorage.setItem(GUEST_BACKUP_KEY, localStorage.getItem(LOCAL_STATE_KEY) || "");
    const { error } = await client.auth.signUp({ email, password });
    if (error) return setAuthMessage(error.message, true);
    setAuthMessage("Sign-up received. Check your inbox if email confirmation is enabled.", false);
  }

  async function signIn() {
    if (!requireConfigured()) return;
    const { email, password } = credentials();
    if (!email || !password) {
      setAuthMessage("Enter your email and password.", true);
      return;
    }
    sessionStorage.setItem(GUEST_BACKUP_KEY, localStorage.getItem(LOCAL_STATE_KEY) || "");
    const { error } = await client.auth.signInWithPassword({ email, password });
    if (error) return setAuthMessage(error.message, true);
    setAuthMessage("Signed in. Loading cloud progress…", false);
  }

  async function sendMagicLink() {
    if (!requireConfigured()) return;
    const { email } = credentials();
    if (!email) {
      setAuthMessage("Enter your email address first.", true);
      return;
    }
    sessionStorage.setItem(GUEST_BACKUP_KEY, localStorage.getItem(LOCAL_STATE_KEY) || "");
    const redirectTo = window.location.origin + window.location.pathname;
    const { error } = await client.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: redirectTo }
    });
    if (error) return setAuthMessage(error.message, true);
    setAuthMessage("Magic link sent. Check your inbox.", false);
  }

  async function signOut() {
    if (!client) return;
    const { error } = await client.auth.signOut();
    if (error) return setAuthMessage(error.message, true);

    currentUser = null;
    const guestBackup = sessionStorage.getItem(GUEST_BACKUP_KEY);
    if (guestBackup) {
      localStorage.setItem(LOCAL_STATE_KEY, guestBackup);
      sessionStorage.removeItem(GUEST_BACKUP_KEY);
      applyProgress(parseLocalProgress() || blankProgress());
    }
    updateAccountUi();
    closeAccountModal();
    showToast("Signed out. Guest mode is active.", "info");
  }

  function queueProgressSync(progress) {
    if (!client || !currentUser || applyingCloudState) return;
    window.clearTimeout(syncTimer);
    syncTimer = window.setTimeout(async () => {
      try {
        await uploadProgress(progress);
        const status = document.getElementById("user-sync-status");
        if (status) status.textContent = "Synced just now";
      } catch (error) {
        console.error("Cloud sync failed:", error);
        const status = document.getElementById("user-sync-status");
        if (status) status.textContent = "Cloud sync needs attention";
      }
    }, 800);
  }

  async function syncNow() {
    if (!currentUser) {
      showToast("Sign in to use cloud sync.", "info");
      return;
    }
    try {
      await uploadProgress(currentProgress());
      showToast("Progress synced to the cloud.", "success");
      updateAccountUi();
    } catch (error) {
      setAuthMessage(error.message, true);
    }
  }

  async function recordAttempt(questionCode, wasCorrect) {
    if (!client || !currentUser) return;
    const { error } = await client.rpc("record_question_attempt", {
      p_question_code: questionCode,
      p_was_correct: Boolean(wasCorrect)
    });
    if (error) console.warn("Question analytics could not be recorded:", error);
  }

  async function loadAdminDashboard() {
    const panel = document.getElementById("admin-dashboard");
    if (!panel || !client || !currentUser) return;

    const { data, error } = await client.rpc("get_admin_dashboard");
    if (error || !data) {
      panel.classList.add("hidden");
      return;
    }

    panel.classList.remove("hidden");
    document.getElementById("admin-total-users").textContent = data.total_users ?? 0;
    document.getElementById("admin-total-answers").textContent = data.total_questions_answered ?? 0;
    document.getElementById("admin-active-users").textContent = data.active_users ?? 0;
    const difficult = Array.isArray(data.difficult_questions) ? data.difficult_questions : [];
    document.getElementById("admin-difficult-questions").innerHTML = difficult.length
      ? difficult.map(item =>
          '<li class="flex justify-between gap-3"><span>' +
          escapeHtml(item.question_code) +
          '</span><span>' +
          Number(item.accuracy_percent || 0).toFixed(1) +
          '% (' + Number(item.attempts || 0) + ' attempts)</span></li>'
        ).join("")
      : '<li>No signed-in attempts yet.</li>';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    })[character]);
  }

  function openAccountModal() {
    document.getElementById("account-modal").classList.remove("hidden");
    updateAccountUi();
  }

  function closeAccountModal() {
    document.getElementById("account-modal").classList.add("hidden");
    setAuthMessage("", false);
  }

  window.CloudSync = {
    init,
    isConfigured,
    isSignedIn: () => Boolean(currentUser),
    queueProgressSync,
    recordAttempt,
    syncNow,
    signUp,
    signIn,
    sendMagicLink,
    signOut,
    loadAdminDashboard,
    openAccountModal,
    closeAccountModal
  };
})();
