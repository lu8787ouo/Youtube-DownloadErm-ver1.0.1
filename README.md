# Youtube DownloadErm ver1.0.1

**此應用程式僅適用於 Windows 系統**

## 使用說明

1. 輸入 YouTube 連結。
2. 點擊「Search Resolution」按鈕。
3. 選擇所需的解析度（Resolution）。
4. 選擇 MP4 或 MP3 格式。
5. 選擇檔案的儲存位置。
6. 選擇下載方式。
7. 點擊「Download Video」按鈕以開始下載。

## 下載方式說明

1. **No Processing**:  
   直接下載完整影片，這是速度最快的選項。

2. **Quick Cut**:  
   先下載完整影片，再根據用戶選擇的時間段進行剪輯，該過程使用 ffmpeg 工具。最終生成的影片可能會比用戶選擇的時間段稍長一些。  
   例：若設定「開始時間」為 "00:05:20"，結束時間為 "00:06:20"，最終生成的影片可能範圍為 "00:05:18" 至 "00:06:22"，總長度約為 1 分 4 秒。

3. **Detailed Cut**:  
   在進行 Quick Cut 後，影片將進行解碼與重新編碼，最終生成的影片將完全符合用戶選擇的時間段。

**執行時間 (MP4)**: No Processing < Quick Cut < Detailed Cut  
**執行時間 (MP3)**: No Processing < Quick Cut = Detailed Cut  

**補充說明**: 若選擇下載 MP3，Quick Cut 和 Detailed Cut 的執行速度與結果相同。

## 優點

1. **無廣告**：完全沒有內置廣告，使用體驗更加順暢。
2. **高畫質**：支持高畫質下載(4k)，並且畫質穩定。
3. **無限速**：下載速度完全取決於用戶自身的網速。
4. **微剪輯**：提供對於下載後的影片進行初步剪輯。

---

**This application is for Windows systems only**

## Usage Instructions

1. Enter the YouTube link.
2. Click the "Search Resolution" button.
3. Select the desired resolution.
4. Choose either MP4 or MP3 format.
5. Select the file save location.
6. Choose the download method.
7. Click the "Download Video" button to start downloading.

## Download Method Descriptions

1. **No Processing**:  
   Downloads the entire video without any modifications, providing the fastest speed.

2. **Quick Cut**:  
   Downloads the entire video first and then trims it based on the user's selected time range using the ffmpeg tool. The resulting video may be slightly longer than the specified time range.  
   Example: If the "Start Time" is set to "00:05:20" and the "End Time" is "00:06:20", the final video might range from "00:05:18" to "00:06:22", with a total length of approximately 1 minute and 4 seconds.

3. **Detailed Cut**:  
   After performing a Quick Cut, the video is further decoded and re-encoded, ensuring the final output matches the exact time range selected by the user.

**Execution Time (MP4)**: No Processing < Quick Cut < Detailed Cut  
**Execution Time (MP3)**: No Processing < Quick Cut = Detailed Cut  

**Note**: When downloading in MP3 format, the execution time and result for Quick Cut and Detailed Cut are the same.

## Advantages

1. **No Ads**: Completely ad-free, providing a smoother user experience.
2. **High Quality**: Supports high-quality downloads (up to 4K), with stable resolution.
3. **Unlimited Speed**: Download speed is entirely dependent on the user's internet connection.
4. **Basic Editing**: Offers basic editing features for videos after downloading.
