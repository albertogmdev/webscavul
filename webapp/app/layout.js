import "@styles/globals.scss";

import Header from "@components/Header/Header"
import Footer from "@components/Footer/Footer"

export const metadata = {
  title: "Home | WebScavul",
  description: "WebScavul - Escanea y gestiona las vulnerabilidades de tu página web",
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header></Header>
        <>{children}</>
        <Footer></Footer>
      </body>
    </html>
  );
}