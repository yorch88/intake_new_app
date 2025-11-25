import { FormEvent, useState } from "react";
import { apiClient } from "../../lib/apiClient";

type RegisterResponse = {
  tenant_id: string;
  client_number: number;
  db_name: string;
};

export function TenantRegisterForm() {
  const [name, setName] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RegisterResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      setLoading(true);
      const res = await apiClient.post<RegisterResponse>(
        "/api/v1/tenants/register",
        {
          name,
          contact_email: contactEmail,
        }
      );
      setResult(res.data);
    } catch (err: any) {
      console.error(err);
      const msg =
        err?.response?.data?.detail ?? "Failed to register tenant.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Company name
          </label>
          <input
            type="text"
            className="w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Contact email
          </label>
          <input
            type="email"
            className="w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={contactEmail}
            onChange={(e) => setContactEmail(e.target.value)}
            required
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-emerald-600 text-white py-2 font-semibold hover:bg-emerald-700 disabled:opacity-60"
        >
          {loading ? "Registering..." : "Register company"}
        </button>
      </form>

      {result && (
        <div className="rounded-md bg-emerald-50 border border-emerald-200 p-4 text-sm text-emerald-800">
          <p className="font-semibold mb-1">Tenant registered successfully!</p>
          <p>Tenant ID: {result.tenant_id}</p>
          <p>Client number: {result.client_number}</p>
          <p>DB name: {result.db_name}</p>
          <p className="mt-2">
            Use the <strong>client number</strong> on the home page (/) to
            access the login flow.
          </p>
        </div>
      )}
    </>
  );
}
