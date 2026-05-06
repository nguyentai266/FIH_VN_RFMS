// src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/mainLayoutPage';
import Dashboard from './pages/dashboardPage';
import Inventory from './pages/warehousePage';
import Login from './pages/loginPage';

// Component bảo vệ đường dẫn (Hỏi xem đã đăng nhập chưa?)
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  return isLoggedIn ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 1. Trang Login đứng độc lập, không nằm trong MainLayout */}
        <Route path="/login" element={<Login />} />

        {/* 2. Các trang còn lại được bảo vệ và nằm trong MainLayout */}
        <Route
          path="/*"
          element={
            <PrivateRoute>
              <MainLayout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/inventory" element={<Inventory />} />
                  <Route path="/audit" element={<div className="p-6">Trang Audit...</div>} />
                  <Route path="/alarm" element={<div className="p-6 text-red-500">Trang Alarm...</div>} />
                </Routes>
              </MainLayout>
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;