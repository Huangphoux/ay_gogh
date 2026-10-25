# Báo cáo

- NCKH→Báo cáo
- Chương 1, 2, 3 từ các mục B1, B2, B2.3
- Chương 4 bổ sung dần số liệu thực nghiệm theo tiến độ làm sản phẩm.

# Bug list

- Bug, search Enter close popup
- Tính năng cho người dùng tự click chỉnh lại loại từ trên UI
- Highlight words in user's weakest level
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis

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
