import { defaultMetaConfig } from "@shared/meta";
import { Metadata } from "next";
import Home from "./Home";

export const metadata: Metadata = {
  ...defaultMetaConfig,
};
export default function Page() {
  return <Home />;
}
