import { defaultMetaConfig } from "@shared/meta";
import { Metadata } from "next";
import Dashboard from "./Dashboard";

export const metadata: Metadata = {
  ...defaultMetaConfig,
};
export default function Page() {
  return <Dashboard />;
}
