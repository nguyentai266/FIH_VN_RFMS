// src/components/MainLayout.tsx
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
  DatabaseOutlined
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const role = localStorage.getItem('role') || 'user';
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.clear(); // Xóa sạch mọi thứ cho nhanh
    navigate('/login');
  };

  const userDropdownItems: MenuProps['items'] = [
    { key: 'profile', icon: <UserOutlined />, label: 'Thông tin cá nhân' },
    { type: 'divider' },
    { key: 'logout', icon: <LogoutOutlined />, label: 'Đăng xuất', danger: true, onClick: handleLogout },
  ];

  // ==========================================
  // LOGIC PHÂN CHIA TOP BAR VÀ SIDEBAR
  // ==========================================

  // 1. Nhận diện người dùng đang ở Phân hệ nào dựa trên URL (Đường dẫn)
  const isWarehouseModule = location.pathname.startsWith('/inventory');
  const activeTopMenu = isWarehouseModule ? 'warehouse' : 'production';

  // 2. Khai báo 2 nút bấm to trên Top Bar
  const topMenuItems = [
    { key: 'production', icon: <AppstoreOutlined />, label: 'Yield Rate' },
    { key: 'warehouse', icon: <DatabaseOutlined />, label: 'Warehouse' },
  ];

  // 3. Khai báo Menu bên trái SẼ THAY ĐỔI tùy theo Phân hệ đang chọn
  const productionSideMenuItems = [
    { key: '/', icon: <BarChartOutlined />, label: 'Dashboard Tỷ lệ' },
    { key: '/audit', icon: <CheckSquareOutlined />, label: 'Quản lý Audit', requiredRole: 'admin' },
    { key: '/alarm', icon: <WarningOutlined />, label: 'Cảnh báo Worker', danger: true, requiredRole: 'admin' },
  ];

  const warehouseSideMenuItems = [
    { key: '/inventory', icon: <TableOutlined />, label: 'Quản lý Tồn kho' },
    // Sau này bạn có thể thêm: Quản lý Nhập kho, Xuất kho, Báo cáo... vào đây
  ];

  // 4. Quyết định xem Sidebar hiện cái gì & Lọc theo Quyền (Role)
  const currentSideMenuRaw = activeTopMenu === 'production' ? productionSideMenuItems : warehouseSideMenuItems;
  const allowedSideMenuItems = currentSideMenuRaw.filter(item => !item.requiredRole || item.requiredRole === role);

  // 5. Xử lý khi bấm vào Top Bar
  const handleTopMenuClick = (key: string) => {
    if (key === 'production') navigate('/'); // Nhảy về Dashboard Sản xuất
    if (key === 'warehouse') navigate('/inventory'); // Nhảy về trang Tồn kho
  };

  return (
    <Layout className="min-h-screen">
      
      {/* ================= THAY ĐỔI LỚN: TOP BAR CHUYỂN LÊN TRÊN CÙNG ================= */}
      <Header className="bg-white px-6 shadow-md flex items-center justify-between sticky top-0 z-50">
        {/* LOGO */}
        <div className="flex items-center gap-3 w-48">
          <div className="text-2xl font-black tracking-widest text-indigo-700">FIH VN</div>
        </div>

        {/* TOP BAR MENU (CĂN GIỮA) */}
        <Menu 
          mode="horizontal" 
          selectedKeys={[activeTopMenu]} 
          items={topMenuItems}
          onClick={(e) => handleTopMenuClick(e.key)}
          className="flex-1 justify-center border-b-0 text-base font-bold text-gray-600"
        />

        {/* KHU VỰC TÀI KHOẢN */}
        <div className="w-48 flex justify-end">
          <Dropdown menu={{ items: userDropdownItems }} placement="bottomRight" arrow>
            <div className="flex items-center gap-3 cursor-pointer hover:bg-gray-100 px-3 py-1.5 rounded-lg transition-all">
              <div className="text-right">
                <div className="text-[12px] font-semibold text-indigo-600 uppercase tracking-wider">{role} {username}</div>
              </div>
              <Avatar className="bg-indigo-600" icon={<UserOutlined />} size="large" />
            </div>
          </Dropdown>
        </div>
      </Header>

      <Layout>
        {/* SIDEBAR BÊN TRÁI SẼ THAY ĐỔI THEO TOP BAR */}
        <Sider width={240} theme="dark" className="shadow-inner pt-4">
          <Menu 
            theme="dark" 
            mode="inline" 
            selectedKeys={[location.pathname]} 
            items={allowedSideMenuItems}
            onClick={(e) => navigate(e.key)}
            className="bg-transparent"
          />
        </Sider>

        {/* NỘI DUNG CHÍNH */}
        <Content className="bg-gray-50 overflow-auto p-6">
          {children}
        </Content>
      </Layout>

    </Layout>
  );
};

export default MainLayout;