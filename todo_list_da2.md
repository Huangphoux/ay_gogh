# Báo cáo

- NCKH→Báo cáo
- Chương 1, 2, 3 từ các mục B1, B2, B2.3
- Chương 4 bổ sung dần số liệu thực nghiệm theo tiến độ làm sản phẩm.

# Đồ án 2

- Bug: Streak, read 2 book in one day count as 0

# My Todo list

- Using `transition-delay` for `data-indicator`
- Sidebar
- Read, Filter
- Refactor `chapter_main` function

# Bug list

- Bug, search Enter close popup
- `a cold`: đoán `cold` là tính từ
- Search for `didn't`: SQL Injection

# Using `transition-delay` for `data-indicator`

```html
<button data-on:click="@post('/endpoint')" data-indicator:fetching>
    Submit
</button>
<div data-class:active="$fetching" class="loading-indicator">Loading...</div>
```

```css
.loading-indicator {
    visibility: hidden;
    opacity: 0;

    &.active {
        visibility: visible;
        opacity: 1;
        transition: opacity 0s 300ms;
        /* transition: name | duration | delay */
    }
}
```
