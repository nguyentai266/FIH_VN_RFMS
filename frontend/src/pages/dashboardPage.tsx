// src/pages/Dashboard.tsx
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  LineChart, Line 
} from 'recharts';

// 1. Giả lập dữ liệu Test Rate trong 7 ngày gần nhất
const data = [
  { name: 'Thứ 2', pass: 400, fail: 20, rate: 95.2 },
  { name: 'Thứ 3', pass: 300, fail: 15, rate: 95.2 },
  { name: 'Thứ 4', pass: 500, fail: 10, rate: 98.0 },
  { name: 'Thứ 5', pass: 450, fail: 40, rate: 91.8 },
  { name: 'Thứ 6', pass: 470, fail: 5, rate: 98.9 },
  { name: 'Thứ 7', pass: 520, fail: 12, rate: 97.7 },
  { name: 'Chủ Nhật', pass: 380, fail: 8, rate: 97.9 },
];

const Dashboard = () => {
  return (
    <div className="p-6 space-y-8">
      {/* PHẦN 1: CÁC THẺ THỐNG KÊ NHANH (KPI CARDS) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border-b-4 border-blue-500">
          <p className="text-gray-500 text-sm font-semibold uppercase tracking-wider">Tổng sản lượng</p>
          <p className="text-3xl font-black text-slate-800 mt-2">3,020</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border-b-4 border-green-500">
          <p className="text-gray-500 text-sm font-semibold uppercase tracking-wider">Tổng PASS</p>
          <p className="text-3xl font-black text-green-600 mt-2">2,910</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border-b-4 border-red-500">
          <p className="text-gray-500 text-sm font-semibold uppercase tracking-wider">Tổng FAIL</p>
          <p className="text-3xl font-black text-red-600 mt-2">110</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border-b-4 border-indigo-500">
          <p className="text-gray-500 text-sm font-semibold uppercase tracking-wider">Yield Rate</p>
          <p className="text-3xl font-black text-indigo-600 mt-2">96.3%</p>
        </div>
      </div>

      {/* PHẦN 2: KHU VỰC BIỂU ĐỒ */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* BIỂU ĐỒ CỘT: SẢN LƯỢNG PASS/FAIL */}
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Thống kê sản lượng Pass/Fail (7 ngày)</h3>
          <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#9ca3af'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#9ca3af'}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                />
                <Legend iconType="circle" />
                <Bar dataKey="pass" name="Số lượng Pass" fill="#22c55e" radius={[4, 4, 0, 0]} />
                <Bar dataKey="fail" name="Số lượng Fail" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* BIỂU ĐỒ ĐƯỜNG: BIẾN ĐỘNG TỈ LỆ % */}
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Xu hướng Tỉ lệ Pass (%)</h3>
          <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#9ca3af'}} />
                <YAxis domain={[80, 100]} axisLine={false} tickLine={false} tick={{fill: '#9ca3af'}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                />
                <Legend iconType="circle" />
                <Line 
                  type="monotone" 
                  dataKey="rate" 
                  name="Tỉ lệ Pass (%)" 
                  stroke="#6366f1" 
                  strokeWidth={4}
                  dot={{ r: 6, fill: '#6366f1', strokeWidth: 2, stroke: '#fff' }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;