import {
  createContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";
import type { ResolveTenantResponse } from "@/lib/types";

type TenantTheme = {
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
};

export type TenantInfo = {
  tenantId: string;
  name: string;
  dbName: string;
  layoutOption: number;
  theme: TenantTheme;
};

type TenantContextValue = {
  tenant: TenantInfo | null;
  accessToken: string | null;
  setTenantFromResolve: (data: ResolveTenantResponse) => void;
  setAccessToken: (token: string | null) => void;
};

export const TenantContext = createContext<TenantContextValue>({
  tenant: null,
  accessToken: null,
  setTenantFromResolve: () => undefined,
  setAccessToken: () => undefined,
});

const TENANT_STORAGE_KEY = "mtqa_tenant";
const TOKEN_STORAGE_KEY = "mtqa_access_token";

export function TenantProvider({ children }: { children: ReactNode }) {
  const [tenant, setTenant] = useState<TenantInfo | null>(null);
  const [accessToken, setAccessTokenState] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const storedTenant = window.localStorage.getItem(TENANT_STORAGE_KEY);
    const storedToken = window.localStorage.getItem(TOKEN_STORAGE_KEY);

    if (storedTenant) {
      try {
        const parsed: TenantInfo = JSON.parse(storedTenant);
        setTenant(parsed);
      } catch {
        // ignore parse errors
      }
    }

    if (storedToken) {
      setAccessTokenState(storedToken);
    }
  }, []);

  const setTenantFromResolve = (data: ResolveTenantResponse) => {
    const newTenant: TenantInfo = {
      tenantId: data.tenant_id,
      name: data.name,
      dbName: data.db_name,
      layoutOption: data.layout_option,
      theme: {
        primaryColor: data.primary_color,
        secondaryColor: data.secondary_color,
        accentColor: data.accent_color,
      },
    };

    setTenant(newTenant);

    if (typeof window !== "undefined") {
      window.localStorage.setItem(
        TENANT_STORAGE_KEY,
        JSON.stringify(newTenant)
      );
    }
  };

  const setAccessToken = (token: string | null) => {
    setAccessTokenState(token);

    if (typeof window === "undefined") return;

    if (token) {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
    } else {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  };

  return (
    <TenantContext.Provider
      value={{
        tenant,
        accessToken,
        setTenantFromResolve,
        setAccessToken,
      }}
    >
      {children}
    </TenantContext.Provider>
  );
}
