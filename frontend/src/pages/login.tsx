// src/pages/Login.tsx
import axios from 'axios';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  const onFinish = async (values: any) => {
    try {
      // 1. Dùng axios gửi POST request mang theo username/password sang FastAPI
      const response = await axios.post('http://localhost:8000/api/login', {
        username: values.username,
        password: values.password
      });

      // 2. Nếu FastAPI trả về success
      if (response.data.status === 'success') {
        message.success('Đăng nhập thành công!');
        
        // Lưu cờ đăng nhập và Token bảo mật vào trình duyệt
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('token', response.data.token); 
        
        // Chuyển vào trong
        navigate('/');
      }
    } catch (error: any) {
      // 3. Nếu gõ sai pass hoặc server sập, FastAPI sẽ ném lỗi về đây
      // error.response.data.detail chính là cái dòng chữ chúng ta cấu hình bên Python
      const errorMsg = error.response?.data?.detail || 'Lỗi không thể kết nối tới Server';
      message.error(errorMsg);
    }
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="w-full max-w-md rounded-2xl bg-white p-10 shadow-2xl">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-black text-slate-800">FIH VN - RFMS</h1>
          <p className="mt-2 text-slate-500">Vui lòng đăng nhập để tiếp tục</p>
        </div>

        <Form name="login_form" onFinish={onFinish} layout="vertical" size="large">
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Vui lòng nhập tài khoản!' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="Tài khoản" />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Vui lòng nhập mật khẩu!' }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="Mật khẩu" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" className="w-full font-bold h-12 bg-indigo-600">
              ĐĂNG NHẬP
            </Button>
          </Form.Item>
        </Form>
        
        <div className="mt-4 text-center text-sm text-slate-400">
          © 2026 FIH VN Smart Factory
        </div>
      </div>
    </div>
  );
};

export default Login;