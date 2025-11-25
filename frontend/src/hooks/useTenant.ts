import { useContext } from "react";
import { TenantContext } from "../context/TenantContext";

export function useTenant() {
  return useContext(TenantContext);
}
