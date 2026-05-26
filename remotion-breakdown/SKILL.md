---
name: remotion-breakdown
description: Use when asked about Remotion framework architecture, implementation principles, how it works internally, or how to use it. Covers frame-driven rendering, Composition API, interpolate/spring animations, Sequence timeline, rendering pipeline (Webpack→Chromium→FFmpeg), and project structure.
---

# Remotion 项目拆解

## 是什么

用 React 代码写视频动画的框架。核心思想：**把视频每一帧当成 React 组件的一次渲染**。

## 技术架构（渲染管线）

```
React 代码
  → @remotion/bundler (Webpack 打包)
  → @remotion/renderer (无头 Chromium 逐帧截图)
  → @remotion/compositor (Rust 原生模块调 FFmpeg 合成)
  → mp4 / webm / gif
```

开发时：`@remotion/studio` 提供本地预览 UI，拖进度条 = 改帧号实时重渲染。

**关键包：**

| 包 | 职责 |
|---|---|
| `remotion` | 核心 API：`useCurrentFrame` `interpolate` `Sequence` |
| `@remotion/cli` | 命令行：`remotion studio` / `render` / `bundle` |
| `@remotion/bundler` | Webpack 打包 React 代码 |
| `@remotion/renderer` | 无头 Chromium 逐帧截图 |
| `@remotion/compositor-*` | Rust 编译，调 FFmpeg 合成视频 |
| `@remotion/player` | 可嵌入网页的播放器组件 |

## 实现原理

### 帧驱动渲染

渲染时 Chromium 被控制循环：设置 `window.remotion_frame = N` → 触发 React 重渲染 → 截图 → N++

```tsx
const frame = useCurrentFrame(); // 0 ~ durationInFrames-1
const opacity = interpolate(frame, [0, 30], [0, 1]); // 0~30帧透明度 0→1
```

### Composition = 视频元数据

```tsx
<Composition
  id="MyComp"
  component={MyComp}
  durationInFrames={60}  // 总帧数 = 2秒（30fps×2）
  fps={30}
  width={1280}
  height={720}
/>
```

### interpolate = 动画核心

```tsx
// 线性插值
const x = interpolate(frame, [0, 60], [0, 500]);

// 加缓动 + 边界限制
const x = interpolate(frame, [0, 60], [0, 500], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

### Sequence = 时间轴分段

```tsx
<Sequence from={0} durationInFrames={30}><Title /></Sequence>
<Sequence from={20} durationInFrames={40}><Subtitle /></Sequence>
// from=20 时两者重叠10帧
```

## 项目结构

```
src/
  index.ts        # registerRoot() 注册入口
  Root.tsx        # 注册所有 Composition
  Composition.tsx # 实际动画内容（主要改这里）
remotion.config.ts  # 输出格式、Webpack 插件配置
```

## 使用方法

```bash
npm run dev          # 启动 Studio 预览 http://localhost:3000
npx remotion render  # 渲染成视频
npx remotion render MyComp out/video.mp4 --width=1920 --height=1080
```

## 常用 API

```tsx
useCurrentFrame()        // 当前帧号
useVideoConfig()         // fps / width / height / durationInFrames
interpolate(v, in, out)  // 插值动画
spring({ frame, fps })   // 弹簧物理动画
<AbsoluteFill>           // 全屏绝对定位容器
<Audio src={...}>        // 嵌入音频
<Video src={...}>        // 嵌入视频
```

## 核心设计思想

| 传统视频工具 | Remotion |
|---|---|
| 时间轴拖拽 | 代码控制 |
| 关键帧手动打 | `interpolate()` 数学描述 |
| 导出不可复现 | 代码即资产，Git 管理 |
| 动态数据难集成 | 直接 fetch API / props 传数据 |

本质：视频 = 数据驱动的函数 `frame → pixels`
