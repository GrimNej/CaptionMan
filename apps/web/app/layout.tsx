import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "sonner";
import { QueryProvider } from "@/components/layout/query-provider";

export const metadata: Metadata = {
  title: "CaptionMan",
  description: "Captions With Receipts",
  icons: {
    icon: "/captionman-frame.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html data-scroll-behavior="smooth" lang="en">
      <body>
        <QueryProvider>{children}</QueryProvider>
        <Toaster position="bottom-left" richColors theme="dark" />
      </body>
    </html>
  );
}
