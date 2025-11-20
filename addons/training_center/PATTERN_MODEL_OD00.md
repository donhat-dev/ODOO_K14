# Hướng dẫn tạo model Odoo chuẩn (pattern)

1. Tạo file model trong thư mục `models/`, ví dụ: `training_course.py`.
2. Định nghĩa class kế thừa `models.Model`, đặt `_name` và các trường cần thiết.
3. Tạo file view trong `views/`, ví dụ: `training_course_view.xml` với tree, form, menu, action.
4. Khai báo quyền truy cập trong `security/ir.model.access.csv`.
5. Thêm các file view, security vào trường `data` của `__manifest__.py`.
6. Đảm bảo có trường `name` (hoặc tương đương) để hiển thị.
7. (Tùy chọn) Thêm các hàm compute, button, logic nghiệp vụ nếu cần.

Ví dụ cho model `training.course` đã thực hiện:
- File model: `models/training_course.py`
- File view: `views/training_course_view.xml`
- File security: `security/ir.model.access.csv`
- Đã cập nhật `__manifest__.py`.

Lưu ý: Luôn kiểm tra kỹ tên file, id, và cập nhật đầy đủ các file liên quan khi thêm model mới.
