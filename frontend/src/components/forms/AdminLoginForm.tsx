import { FormEvent, useState } from "react";
import { useRouter } from "next/router";
import { apiClient } from "../../lib/apiClient";
import { useTenant } from "../../hooks/useTenant";

export function AdminLoginForm() {
  const { tenant, setAccessToken } = useTenant();
  const router = useRouter();

  const [username, setUsername] = useState("admin"); // default for convenience
  const [password, setPassword] = useState("admin123"); // default for convenience
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!tenant) {
    // If there is no tenant resolved, do not render the form
    return null;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      setLoading(true);

      const response = await apiClient.post("/api/v1/auth/login", {
        tenant_id: tenant.tenantId,
        username,
        password,
      });

      const token = response.data.access_token as string;
      setAccessToken(token);

      router.push("/admin/dashboard");
    } catch (err: any) {
      console.error(err);
      const msg =
        err?.response?.data?.detail ??
        "Login failed. Please check your credentials.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">
          Username
        </label>
        <input
          type="text"
          className="w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">
          Password
        </label>
        <input
          type="password"
          className="w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-md bg-slate-900 text-white py-2 font-semibold hover:bg-slate-800 disabled:opacity-60"
      >
        {loading ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
