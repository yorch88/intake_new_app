import { useEffect } from "react";
import Head from "next/head";
import { useRouter } from "next/router";
import { useTenant } from "../hooks/useTenant";
import { AdminLoginForm } from "../components/forms/AdminLoginForm";

export default function LoginPage() {
  const { tenant } = useTenant();
  const router = useRouter();

  useEffect(() => {
    if (!tenant) {
      router.replace("/");
    }
  }, [tenant, router]);

  if (!tenant) {
    return null;
  }

  return (
    <>
      <Head>
        <title>Admin login | {tenant.name}</title>
      </Head>
      <main className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="w-full max-w-md bg-white rounded-xl shadow-md p-8">
          <h1 className="text-2xl font-semibold mb-4 text-center">
            Admin login for {tenant.name}
          </h1>
          <AdminLoginForm />
        </div>
      </main>
    </>
  );
}
