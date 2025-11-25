import Head from "next/head";
import { TenantRegisterForm } from "../components/forms/TenantRegisterForm";
export default function RegisterTenantPage() {
  return (
    <>
      <Head> 
        <title>Register company | Multi-tenant app</title>
      </Head>
      <main className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="w-full max-w-lg bg-white rounded-xl shadow-md p-8">
          <h1 className="text-2xl font-semibold mb-4 text-center">
            Register a new company
          </h1>
          <p className="text-sm text-slate-600 mb-6 text-center">
            This form is used to register a new tenant (company) in the system.
          </p>
          <TenantRegisterForm />
        </div>
      </main>
    </>
  );
}
