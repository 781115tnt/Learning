@echo off
chcp 65001
echo "Batch xóa nền + tăng đậm cho file hình TIF PNG JPG JPEG"
set /p "fuzz=Nhập giá trị xóa nền từ 0->99 (giá trị càng lớn càng xóa nền nhiều; không sử dụng chọn 0; mặc định nên chọn 15): "
set /p "lowLev=Nhập giá trị tăng đậm hình từ 0->99 (giá trị càng lớn hình càng đậm; không sử dụng chọn 0; mặc định nên chọn 15): "
set /p "scl=Nhập giá trị dưới chỉnh contrast thông minh (giá trị từ 1->25, gt càng nhỏ điểm ảnh càng nhạt sẽ được làm đậm; không sử dụng chọn 0; mặc định nên chọn 15): "
set /p "sch=Nhập giá trị trên chỉnh contrast thông minh (giá trị từ 50->85, gt càng lớn hình càng đậm; không sử dụng chọn 50; mặc định nên chọn 75): "
set /p "bt=Nhập giá trị nét đen (giá trị từ 0->20, gt càng lớn càng nhiều điểm ảnh được chuyển sang đen; không sử dụng chọn 0; mặc định nên chọn 5): "




set outdir=.\_out_N%fuzz%_Đ%lowLev%_SC_%scl%x%sch%_BT_%bt%
mkdir "%outdir%"

@echo on
for %%i in (*.tif *.png *.jpg *.jpeg) do convert "%%i" -fuzz "%fuzz%%%" -fill White -opaque White -level %lowLev%%%,100%% -sigmoidal-contrast %scl%,%sch%%% -black-threshold %bt%%% -compress Group4 "%outdir%\%%i"
