# Event Management System

## Tổng quan
Event Management System là một ứng dụng Python được xây dựng để quản lý sự kiện với các vai trò người dùng khác nhau và tích hợp sự kiện từ web. Ứng dụng sử dụng thư viện customtkinter để tạo giao diện người dùng hiện đại và dễ sử dụng.

## Cài đặt
1. Đảm bảo bạn đã cài đặt Python 3.6 trở lên.
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy ứng dụng:
   ```bash
   python src/main.py
   ```

## Cấu trúc dự án
- `src/`: Thư mục chứa mã nguồn chính
  - `model/`: Chứa các lớp dữ liệu (User, Event)
  - `repository/`: Chứa các lớp truy xuất dữ liệu (UserRepository, EventRepository)
  - `service/`: Chứa các lớp dịch vụ nghiệp vụ (UserService, EventService)
  - `ui/`: Chứa các thành phần giao diện người dùng
  - `main.py`: Điểm khởi đầu của ứng dụng
- `events.json`: Lưu trữ dữ liệu sự kiện
- `users.json`: Lưu trữ dữ liệu người dùng
- `web_events.json`: Lưu trữ dữ liệu sự kiện từ web
- `requirements.txt`: Danh sách các thư viện phụ thuộc

## Tính năng
### Quản lý người dùng
- Đăng nhập với vai trò admin hoặc user
- Đăng ký tài khoản mới
- Quản lý người dùng (thêm, sửa, xóa) cho admin
- Phân quyền người dùng (admin/user)

### Quản lý sự kiện
- Tạo, sửa, xóa sự kiện
- Gán người dùng vào sự kiện
- Xem danh sách sự kiện
- Tìm kiếm sự kiện theo tiêu đề

### Tích hợp sự kiện web
- Tự động cập nhật sự kiện từ web
- Xem danh sách sự kiện web

## Hướng dẫn sử dụng
1. Khởi động ứng dụng và đăng nhập với tài khoản admin mặc định:
   - Username: admin
   - Password: admin123
2. Sử dụng các chức năng quản lý người dùng và sự kiện theo vai trò của bạn.
3. Để thoát ứng dụng, nhấn nút Logout hoặc đóng cửa sổ.

## Đóng gói ứng dụng
Để tạo file thực thi, sử dụng PyInstaller:
```bash
pyinstaller EventManager.spec
```
File thực thi sẽ được tạo trong thư mục `dist/`. 