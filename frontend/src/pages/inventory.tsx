// src/pages/Inventory.tsx
import { Table, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';

// 1. Định nghĩa cấu trúc dữ liệu cho mỗi dòng (TypeScript)
interface InventoryItem {
  key: string;
  id_vat_tu: string;
  ten_vat_tu: string;
  so_luong: number;
  trang_thai: string;
}

// 2. Cấu hình các cột cho Bảng
const columns: ColumnsType<InventoryItem> = [
  {
    title: 'Mã Vật Tư',
    dataIndex: 'id_vat_tu',
    key: 'id_vat_tu',
    className: 'font-semibold text-gray-600', // Dùng Tailwind làm mờ nhẹ màu chữ
  },
  {
    title: 'Tên Vật Tư',
    dataIndex: 'ten_vat_tu',
    key: 'ten_vat_tu',
  },
  {
    title: 'Số Lượng Tồn',
    dataIndex: 'so_luong',
    key: 'so_luong',
    // Tô màu xanh và làm đậm số lượng
    render: (so_luong: number) => <span className="font-bold text-blue-600">{so_luong}</span>,
  },
  {
    title: 'Trạng Thái',
    dataIndex: 'trang_thai',
    key: 'trang_thai',
    // Tự động đổi màu nhãn dán (Tag) dựa theo chữ "Sắp hết" hay "Đầy đủ"
    render: (trang_thai: string) => {
      let color = trang_thai === 'Sắp hết' ? 'volcano' : 'green';
      return (
        <Tag color={color} key={trang_thai}>
          {trang_thai.toUpperCase()}
        </Tag>
      );
    },
  },
];

// 3. Dữ liệu giả lập (Sau này sẽ gọi từ Python API)
const dataFake: InventoryItem[] = [
  {
    key: '1',
    id_vat_tu: 'VT001',
    ten_vat_tu: 'Màn hình LCD 5 inch',
    so_luong: 1500,
    trang_thai: 'Đầy đủ',
  },
  {
    key: '2',
    id_vat_tu: 'VT002',
    ten_vat_tu: 'Pin Lithium 3000mAh',
    so_luong: 20,
    trang_thai: 'Sắp hết',
  },
  {
    key: '3',
    id_vat_tu: 'VT003',
    ten_vat_tu: 'Vỏ nhựa Case A',
    so_luong: 800,
    trang_thai: 'Đầy đủ',
  },
  {
    key: '4',
    id_vat_tu: 'VT004',
    ten_vat_tu: 'Cáp kết nối Type-C',
    so_luong: 50,
    trang_thai: 'Sắp hết',
  },
];

// 4. Component chính
const Inventory = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Quản lý Kho hàng (Inventory)</h1>
      
      {/* Khung trắng bọc ngoài cái bảng cho đẹp */}
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <Table 
          columns={columns} 
          dataSource={dataFake} 
          pagination={{ pageSize: 5 }} // Tự động chia 5 dòng 1 trang
        />
      </div>
    </div>
  );
};

export default Inventory;