// src/pages/Login.tsx
import { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { loginApi } from '../api/loginApi'; // Import API Service đã tách
import logo from '../assets/fushan.png';
const Login = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: any) => {
    try {
      setLoading(true); 
      
      
      const response: any = await loginApi.login(values.username, values.password);

      
      if (response.success === true) {
        message.success(response.message_id || 'Đăng nhập thành công!');
        
        
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('role', response.role);
        localStorage.setItem('username', response.username);
        if (response.token) {
          localStorage.setItem('token', response.token);
        }
        
        navigate('/');
      }
    } catch (error: any) {
      
      const errorMsg = error.response?.data?.detail || 'Lỗi không thể kết nối tới Server';
      message.error(errorMsg);
    } finally {
      
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="w-full max-w-md rounded-2xl bg-white p-10 shadow-2xl">
       
        <div className="mb-8 text-center">
          <img src={logo} alt="Fushan logo" className="w-30 h-auto mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-indigo-800 tracking-wider">DMS-VN TEST ENGINEERING</h1>
          <p className="mt-2 text-slate-500">Vui lòng đăng nhập để tiếp tục</p>
        </div>

        <Form 
          name="login_form" 
          onFinish={onFinish} 
          layout="vertical" 
          size="large"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Vui lòng nhập mã nhân viên (Tài khoản)!' }]}
          >
            <Input prefix={<UserOutlined className="text-gray-400" />} placeholder="Mã nhân viên (VD: V1531673)" />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Vui lòng nhập mật khẩu!' }]}
          >
            <Input.Password prefix={<LockOutlined className="text-gray-400" />} placeholder="Mật khẩu" />
          </Form.Item>

          <Form.Item className="mt-6">
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading} // Gắn biến loading vào đây để Ant Design tự tạo hiệu ứng
              className="w-full font-bold h-12 bg-indigo-600 hover:bg-indigo-500"
            >
              ĐĂNG NHẬP
            </Button>
          </Form.Item>
        </Form>
        
        <div className="mt-6 text-center text-xs text-slate-400">
          © 2026 FIH VN - DMS TE - RFMS System
        </div>
      </div>
    </div>
  );
};

export default Login;