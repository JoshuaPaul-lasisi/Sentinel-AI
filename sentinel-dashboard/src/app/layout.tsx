/* eslint-disable @next/next/no-page-custom-font */
import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "react-hot-toast";
import QueryClientProvider from "@ui/templates/QueryClientProvider";
import { defaultMetaConfig } from "@shared/meta";
import NextTopLoader from "nextjs-toploader";

export const metadata: Metadata = {
  ...defaultMetaConfig,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* load google font  */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossOrigin="anonymous"
      />
      <link
        href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=Gabriela&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Manrope:wght@200..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&family=Nunito:ital,wght@0,200..1000;1,200..1000&family=Port+Lligat+Sans&family=Quicksand:wght@300..700&family=Roboto:ital,wght@0,100..900;1,100..900&family=Rubik+Puddles&family=Space+Grotesk:wght@300..700&display=swap"
        rel="stylesheet"
      />
      {/* end loading of fonts */}
      <body className={``}>
        <NextTopLoader color="#808080" height={4} showSpinner={true} />

        <QueryClientProvider>
          {children}
          <Toaster />
        </QueryClientProvider>
      </body>
    </html>
  );
}
