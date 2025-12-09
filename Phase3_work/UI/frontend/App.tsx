// App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./components/LandingPage";
import { HomePage } from "./components/HomePage";
import { GrantApplyPage } from "./components/GrantApplyPage.tsx";
import { GrantsSearchPage } from "./components/GrantsSearchPage";
import { GrantDetailsPage } from "./components/GrantDetailsPage";
import { ApplicationEditPage } from "./components/ApplicationEditPage";
import { ThemeProvider } from "./components/ThemeProvider";
import  UserPage from "./components/UserPage";
import SearchGrants from "./components/SearchGrants";

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/homepage" element={<HomePage />} />
          <Route path="/user" element={<UserPage />} />
          <Route path="/grantApply" element={<GrantApplyPage/>} />
          <Route path="/searchGrants" element={<GrantsSearchPage/>} />
          <Route path="/grant/:id" element={<GrantDetailsPage/>} />
          <Route path="/application/:applicationId" element={<ApplicationEditPage/>} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
