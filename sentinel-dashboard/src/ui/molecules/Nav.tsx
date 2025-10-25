"use client";

import Link from "next/link";

export const Nav = ({ renderedAt }: { renderedAt?: "dashboard" | "home" }) => {
  return (
    <nav className="px-8 py-4 bg-white shadow-xs flex items-center justify-between z-10 relative">
      <Link href="/" className="text-xl font-bold text-gray-900 ">
        Sentinel <span className="text-primary-500">AI</span>
      </Link>

      {
        <Link
          href={renderedAt === "home" ? "/dashboard" : "/"}
          className="font-nunito bg-primary-500 text-white px-8 py-3 rounded-xl font-semibold hover:bg-primary-700 transition-colors"
        >
            {
            renderedAt === "home" ? "Dashboard" : "Home"
            }
        </Link>
      }
    </nav>
  );
};
