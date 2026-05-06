// src/components/MainLayout.tsx
import { useState } from 'react';
import { Layout, Menu, Dropdown, Avatar } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import type { MenuProps } from 'antd';
import { 
  BarChartOutlined, 
  TableOutlined, 
  WarningOutlined, 
  CheckSquareOutlined,
  UserOutlined,      
  LogoutOutlined,
  AppstoreOutlined,
  DatabaseOutlined,
  MenuOutlined,
  FieldTimeOutlined,
  AlertOutlined
} from '@ant-design/icons';
import { loginApi } from '../api/loginApi';

const { Header, Sider, Content } = Layout;

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const [collapsed, setCollapsed] = useState(false);
  
  const role = localStorage.getItem('role') || 'user';
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    loginApi.logout(); 
    navigate('/login');
  };

  const userDropdownItems: MenuProps['items'] = [
    { key: 'profile', icon: <UserOutlined />, label: 'Thông tin cá nhân' },
    { type: 'divider' },
    { key: 'logout', icon: <LogoutOutlined />, label: 'Đăng xuất', danger: true, onClick: handleLogout },
  ];

  const isWarehouseModule = location.pathname.startsWith('/inventory');
  const activeTopMenu = isWarehouseModule ? 'warehouse' : 'production';

  const topMenuItems = [
    { key: 'production', icon: <AppstoreOutlined />, label: 'Yield Rate' },
    { key: 'warehouse', icon: <DatabaseOutlined />, label: 'Inventory' },
    { key: 'overtime', icon: <FieldTimeOutlined />, label: 'Overtime & Leave' },
    { key: 'botcontrol', icon: <AlertOutlined />, label: 'Alarm Chatbot' ,danger: true,requiredRole: 'admin'},
  ];

  const productionSideMenuItems = [
    { key: '/', icon: <BarChartOutlined />, label: 'Dashboard Tỷ lệ' },
    { key: '/audit', icon: <CheckSquareOutlined />, label: 'Quản lý Audit', requiredRole: 'admin' },
    { key: '/alarm', icon: <WarningOutlined />, label: 'Cảnh báo Worker', danger: true, requiredRole: 'admin' },
  ];

  const warehouseSideMenuItems = [
    { key: '/inventory', icon: <TableOutlined />, label: 'Quản lý Tồn kho' },
  ];

  const allowedHeaderMenuItems = topMenuItems.filter(item => !item.requiredRole || item.requiredRole === role);
  const currentSideMenuRaw = activeTopMenu === 'production' ? productionSideMenuItems : warehouseSideMenuItems;
  const allowedSideMenuItems = currentSideMenuRaw.filter(item => !item.requiredRole || item.requiredRole === role);


  const handleTopMenuClick = (key: string) => {
    if (key === 'production') navigate('/'); 
    if (key === 'warehouse') navigate('/inventory'); 
  };

  return (
    <Layout className="min-h-screen">
      
      {/* CSS ÉP TRỤC DỌC BÊN TRONG SIDEBAR */}
      {/* CSS ÉP TRỤC DỌC BÊN TRONG SIDEBAR */}
      <style>{`
        /* Ép lề trái chính xác 16px cho cả trạng thái MỞ và ĐÓNG */
        .perfect-align-menu .ant-menu-item,
        .perfect-align-menu.ant-menu-inline-collapsed .ant-menu-item {
          padding-left: 16px !important;
          justify-content: flex-start !important; /* Cấm AntD tự động center khi thu nhỏ */
          margin-inline: 0 !important;
          width: 100% !important;
          border-radius: 0 24px 24px 0 !important;
        }

        /* Khung icon cố định 40px */
        .perfect-align-menu .ant-menu-item-icon {
          min-width: 40px !important;
          width: 40px !important;
          height: 40px !important;
          display: inline-flex !important;
          align-items: center;
          justify-content: center;
          font-size: 18px !important;
          margin-right: 0 !important;
        }
        
        .perfect-align-menu .ant-menu-title-content {
          margin-left: 12px !important;
        }
      `}</style>

      {/* ========================================================= */}
      {/* SIDEBAR: CHỨA LUÔN NÚT 3 GẠCH Ở TRÊN CÙNG */}
      {/* ========================================================= */}
      <Sider 
        trigger={null}
        collapsible 
        collapsed={collapsed} 
        collapsedWidth={80} 
        width={240} 
        theme="dark" 
        className="bg-[#001529] shadow-xl z-50 transition-all duration-300 ease-in-out"
      >
        {/* KHU VỰC NÚT 3 GẠCH */}
        <div className="h-16 flex items-center pl-[19px]">
          <div 
            onClick={() => setCollapsed(!collapsed)}
            className="w-10 h-10 rounded-full hover:bg-white/10 flex items-center justify-center cursor-pointer transition-all active:bg-white/20 active:scale-95 shrink-0"
          >
            <MenuOutlined style={{ color: 'white', fontSize: '18px' }} />
          </div>
        </div>

        {/* MENU CHÍNH CỦA SIDEBAR */}
        <Menu 
          theme="dark" 
          mode="inline" 
          selectedKeys={[location.pathname]} 
          items={allowedSideMenuItems}
          onClick={(e) => navigate(e.key)}
          className="bg-transparent border-none pl-20px perfect-align-menu mt-2" 
        />
      </Sider>

      {/* ========================================================= */}
      {/* CỘT BÊN PHẢI: CHỨA HEADER VÀ NỘI DUNG CHÍNH */}
      {/* ========================================================= */}
      <Layout>
        {/* HEADER: Bây giờ chỉ còn chứa Logo, Tabs và Profile */}
        <Header className="bg-[#001529] px-6 shadow-md flex items-center justify-between sticky top-0 z-40 border-l border-white/10">
          
          {/* LOGO */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/')}>
         
            <div className="text-xl font-black tracking-widest text-white hidden sm:block">
              FIH-VN RFMS
            </div>
          </div>

          {/* TOP BAR MENU (CÁC TAB PHÂN HỆ) */}
          <Menu 
            theme="dark" 
            mode="horizontal" 
            selectedKeys={[activeTopMenu]} 
            items={allowedHeaderMenuItems}
            onClick={(e) => handleTopMenuClick(e.key)}
            className="flex-1 justify-center border-b-0 text-base font-bold bg-transparent"
          />

          {/* KHU VỰC TÀI KHOẢN */}
          <div className="w-60 flex justify-end">
            <Dropdown menu={{ items: userDropdownItems }} placement="bottomRight" arrow>
              <div className="flex items-center gap-3 cursor-pointer hover:bg-white/10 px-3 py-1.5 rounded-lg transition-all">
                <div className="text-right hidden md:block">
                  <div className="text-[12px] font-semibold text-blue-200 uppercase tracking-wider">
                    {role} {username}
                  </div>
                </div>
                <Avatar className="bg-blue-600 border-none" icon={<UserOutlined />} size="large" />
              </div>
            </Dropdown>
          </div>
        </Header>

        {/* NỘI DUNG CHÍNH */}
        <Content className="bg-gray-50 overflow-auto p-6 transition-all duration-300 ease-in-out">
          {children}
        </Content>
      </Layout>

    </Layout>
  );
};

export default MainLayout;