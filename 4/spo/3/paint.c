#include <windows.h>
#include <commdlg.h>
#include <stdio.h>

#define ID_FILE_SAVE 1
#define ID_FILE_EXIT 2

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void CreateMenus(HWND hwnd);
void SaveBitmap(HWND hwnd, HBITMAP hBitmap);
void DrawLine(HDC hdc, int x1, int y1, int x2, int y2);

POINT lastPoint;
BOOL drawing = FALSE;
HBITMAP hBitmap;
HDC hdcMem;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd) {
    const char CLASS_NAME[] = "DrawingAppClass";

    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        "Simple Drawing Application",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    ShowWindow(hwnd, nShowCmd);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Освобождение ресурсов перед выходом
    DeleteObject(hBitmap);
    DeleteDC(hdcMem);

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CREATE:
            CreateMenus(hwnd);
            // Создание контекста устройства и битмапа
            hdcMem = CreateCompatibleDC(GetDC(hwnd));
            hBitmap = CreateCompatibleBitmap(GetDC(hwnd), 800, 600);
            SelectObject(hdcMem, hBitmap);
            // Заполнение битмапа белым цветом
            HBRUSH hBrush = CreateSolidBrush(RGB(255, 255, 255));
            FillRect(hdcMem, &((RECT){0, 0, 800, 600}), hBrush);
            DeleteObject(hBrush);
            break;

        case WM_LBUTTONDOWN:
            lastPoint.x = LOWORD(lParam);
            lastPoint.y = HIWORD(lParam);
            drawing = TRUE;
            break;

        case WM_MOUSEMOVE:
            if (drawing) {
                DrawLine(hdcMem, lastPoint.x, lastPoint.y, LOWORD(lParam), HIWORD(lParam));
                lastPoint.x = LOWORD(lParam);
                lastPoint.y = HIWORD(lParam);
                InvalidateRect(hwnd, NULL, FALSE);
            }
            break;

        case WM_LBUTTONUP:
            drawing = FALSE;
            break;

        case WM_COMMAND:
            switch (LOWORD(wParam)) {
                case ID_FILE_SAVE:
                    SaveBitmap(hwnd, hBitmap);
                    break;
                case ID_FILE_EXIT:
                    DestroyWindow(hwnd);
                    break;
                default:
                    break;
            }
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            BitBlt(hdc, 0, 0, 800, 600, hdcMem, 0, 0, SRCCOPY);
            EndPaint(hwnd, &ps);
            break;
        }

        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

void CreateMenus(HWND hwnd) {
    HMENU hMenu = CreateMenu();
    HMENU hFileMenu = CreatePopupMenu();

    AppendMenu(hFileMenu, MF_STRING, ID_FILE_SAVE, "Save");
    AppendMenu(hFileMenu, MF_STRING, ID_FILE_EXIT, "Exit");

    AppendMenu(hMenu, MF_POPUP, (UINT_PTR)hFileMenu, "File");

    SetMenu(hwnd, hMenu);
}

void DrawLine(HDC hdc, int x1, int y1, int x2, int y2) {
    MoveToEx(hdc, x1, y1, NULL);
    LineTo(hdc, x2, y2);
}

void SaveBitmap(HWND hwnd, HBITMAP hBitmap) {
    OPENFILENAME ofn;
    char szFile[260];

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFile = szFile;
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = "Bitmap Files (*.bmp)\0*.bmp\0All Files (*.*)\0*.*\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_OVERWRITEPROMPT;

    if (GetSaveFileName(&ofn)) {
        BITMAP bmp;
        GetObject(hBitmap, sizeof(BITMAP), &bmp);

        HANDLE hFile = CreateFile(ofn.lpstrFile, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hFile != INVALID_HANDLE_VALUE) {
            BITMAPFILEHEADER bmfHeader;
            BITMAPINFOHEADER bi;

            bi.biSize = sizeof(BITMAPINFOHEADER);
            bi.biWidth = bmp.bmWidth;
            bi.biHeight = bmp.bmHeight;
            bi.biPlanes = 1;
            bi.biBitCount = 24; // 24-битный цвет
            bi.biCompression = BI_RGB;
            bi.biSizeImage = 0;
            bi.biXPelsPerMeter = 0;
            bi.biYPelsPerMeter = 0;
            bi.biClrUsed = 0;
            bi.biClrImportant = 0;

            DWORD dwDIBSize = ((bmp.bmWidth * 3 + 3) & ~3) * bmp.bmHeight;
            DWORD dwBmpSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + dwDIBSize;

            bmfHeader.bfType = 0x4D42;
            bmfHeader.bfSize = dwBmpSize;
            bmfHeader.bfReserved1 = 0;
            bmfHeader.bfReserved2 = 0;
            bmfHeader.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

            DWORD dwWritten;
            WriteFile(hFile, &bmfHeader, sizeof(BITMAPFILEHEADER), &dwWritten, NULL);
            WriteFile(hFile, &bi, sizeof(BITMAPINFOHEADER), &dwWritten, NULL);

            BYTE *pPixels = (BYTE *)GlobalAlloc(GPTR, dwDIBSize);
            GetDIBits(hdcMem, hBitmap, 0, bmp.bmHeight, pPixels, (BITMAPINFO *)&bi, DIB_RGB_COLORS);
            WriteFile(hFile, pPixels, dwDIBSize, &dwWritten, NULL);
            GlobalFree(pPixels);

            CloseHandle(hFile);
        }
    }
}
