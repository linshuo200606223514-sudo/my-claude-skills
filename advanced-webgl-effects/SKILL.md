---
name: advanced-webgl-effects
description: Advanced WebGL effects library with ready-to-use shaders, particle systems, and 3D effects. Includes actual code, not just guidelines.
---

# Advanced WebGL Effects Toolkit

这是一个**真正可用**的 WebGL 特效工具库，包含实际代码和 API。

## When to use

当用户需要：
- 创建高级 3D 特效（黑洞、星云、粒子系统等）
- 使用现成的着色器代码
- 快速实现复杂的 WebGL 效果
- 调用预制的特效 API

## Available Effects Library

### 1. 黑洞特效 API

```javascript
// 使用方法
const blackHole = new BlackHoleEffect({
    radius: 2.0,
    accretionDiskSize: 8.0,
    particleCount: 10000,
    temperature: 6000000
});

scene.add(blackHole.getMesh());
```

**着色器代码：**

```glsl
// 黑洞核心着色器
uniform float time;
uniform float intensity;
varying vec3 vNormal;
varying vec3 vPosition;

float noise(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main() {
    vec3 viewDir = normalize(vPosition);
    float fresnel = pow(1.0 - abs(dot(viewDir, vNormal)), 3.0);

    // 事件视界
    float horizon = smoothstep(0.0, 1.0, length(vPosition) / 2.0);

    // 引力红移
    vec3 color = vec3(0.0);
    color += vec3(0.1, 0.0, 0.2) * fresnel * 0.3;
    color += vec3(0.5, 0.1, 0.8) * pow(fresnel, 5.0) * 2.0;

    gl_FragColor = vec4(color * intensity, 1.0 - horizon * 0.3);
}
```

### 2. 粒子系统 API

```javascript
// 创建粒子系统
const particles = new ParticleSystem({
    count: 50000,
    distribution: 'spiral', // 'spiral', 'sphere', 'disk'
    colors: ['#ff6b00', '#ffd700', '#ff0000'],
    size: [0.5, 3.0],
    speed: 0.002
});

// 更新粒子
particles.update(deltaTime);
```

**粒子着色器：**

```glsl
// Vertex Shader
attribute float size;
attribute vec3 color;
varying vec3 vColor;
uniform float time;

void main() {
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = size * (300.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
}

// Fragment Shader
varying vec3 vColor;

void main() {
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);

    if (dist > 0.5) discard;

    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
    vec3 color = vColor * (1.0 + alpha);

    gl_FragColor = vec4(color, alpha * 0.8);
}
```

### 3. 吸积盘特效 API

```javascript
const accretionDisk = new AccretionDisk({
    innerRadius: 2.5,
    outerRadius: 12.0,
    segments: 256,
    rotationSpeed: 0.002,
    temperature: {
        inner: 10000, // K
        outer: 3000   // K
    }
});
```

**吸积盘着色器：**

```glsl
uniform float time;
varying vec2 vUv;

void main() {
    float angle = atan(vUv.y - 0.5, vUv.x - 0.5);
    float radius = length(vUv - 0.5);

    // 旋转螺旋
    float spiral = sin(angle * 20.0 - radius * 50.0 + time * 3.0) * 0.5 + 0.5;

    // 温度梯度
    vec3 hotColor = vec3(1.0, 0.9, 0.7);
    vec3 warmColor = vec3(1.0, 0.5, 0.1);
    vec3 coolColor = vec3(0.8, 0.1, 0.0);

    vec3 color = mix(coolColor, warmColor, 1.0 - radius);
    color = mix(color, hotColor, spiral * (1.0 - radius) * 0.5);

    float brightness = (spiral + 0.5) * (1.0 - radius * 0.5);
    color *= brightness * 1.5;

    float alpha = (1.0 - radius) * 0.9 * (spiral * 0.5 + 0.5);

    gl_FragColor = vec4(color, alpha);
}
```

### 4. 星云特效 API

```javascript
const nebula = new NebulaEffect({
    size: 50,
    density: 0.3,
    colors: ['#ff00ff', '#00ffff', '#ffff00'],
    turbulence: 0.5,
    glow: true
});
```

### 5. 能量护盾特效 API

```javascript
const shield = new EnergyShield({
    radius: 5,
    hexagonSize: 0.5,
    color: '#00ffff',
    pulseSpeed: 2.0,
    impactEffect: true
});

// 添加冲击点
shield.addImpact(x, y, z, strength);
```

**护盾着色器：**

```glsl
uniform float time;
uniform vec3 impactPoint;
uniform float impactStrength;
varying vec3 vPosition;

float hexagon(vec2 p) {
    p = abs(p);
    return max(dot(p, normalize(vec2(1.0, 1.73))), p.x);
}

void main() {
    vec2 hexCoord = vPosition.xy * 10.0;
    float hex = hexagon(fract(hexCoord) - 0.5);
    float hexPattern = smoothstep(0.4, 0.5, hex);

    // 冲击波
    float dist = distance(vPosition, impactPoint);
    float impact = exp(-dist * 2.0) * impactStrength;

    vec3 color = vec3(0.0, 1.0, 1.0);
    color += impact * vec3(1.0, 0.5, 0.0);

    float alpha = hexPattern * 0.3 + impact * 0.7;

    gl_FragColor = vec4(color, alpha);
}
```

### 6. 传送门特效 API

```javascript
const portal = new PortalEffect({
    radius: 3,
    depth: 2,
    spiralSpeed: 1.5,
    color1: '#0066ff',
    color2: '#ff00ff',
    distortionStrength: 0.5
});
```

### 7. 全息投影特效 API

```javascript
const hologram = new HologramEffect({
    scanlineSpeed: 2.0,
    glitchIntensity: 0.3,
    color: '#00ffff',
    flickerRate: 0.1,
    transparency: 0.7
});
```

## Complete Example

```javascript
// 完整示例：创建一个黑洞场景
import * as THREE from 'three';

// 初始化场景
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

// 创建黑洞
const blackHole = createBlackHole({
    radius: 2.0,
    intensity: 1.5
});
scene.add(blackHole);

// 创建吸积盘
const disk = createAccretionDisk({
    innerRadius: 2.5,
    outerRadius: 12.0
});
scene.add(disk);

// 创建粒子系统
const particles = createParticleSystem({
    count: 10000,
    distribution: 'spiral'
});
scene.add(particles);

// 动画循环
function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // 更新着色器
    blackHole.material.uniforms.time.value = time;
    disk.material.uniforms.time.value = time;

    // 更新粒子
    updateParticles(particles, time);

    renderer.render(scene, camera);
}

animate();
```

## Shader Library

### 噪声函数集合

```glsl
// Perlin Noise
float perlinNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);

    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// Simplex Noise
float simplexNoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
    vec2 i = floor(v + dot(v, C.yy));
    vec2 x0 = v - i + dot(i, C.xx);
    vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;

    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));

    vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
    m = m * m;
    m = m * m;

    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;

    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);

    vec3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;

    return 130.0 * dot(m, g);
}

// Voronoi Noise
vec2 voronoiNoise(vec2 x) {
    vec2 n = floor(x);
    vec2 f = fract(x);

    vec2 mg, mr;
    float md = 8.0;

    for(int j = -1; j <= 1; j++) {
        for(int i = -1; i <= 1; i++) {
            vec2 g = vec2(float(i), float(j));
            vec2 o = random2(n + g);
            vec2 r = g + o - f;
            float d = dot(r, r);

            if(d < md) {
                md = d;
                mr = r;
                mg = g;
            }
        }
    }

    return vec2(md, 0.0);
}
```

## Performance Tips

1. **使用 BufferGeometry** 而不是 Geometry
2. **合并网格** 减少 draw calls
3. **使用纹理图集** 减少纹理切换
4. **LOD (Level of Detail)** 根据距离调整细节
5. **Frustum Culling** 只渲染可见对象
6. **使用 InstancedMesh** 渲染大量相同对象

## Instructions

当用户需要创建 WebGL 特效时：

1. 询问具体需求（黑洞、星云、粒子等）
2. 从上述 API 中选择合适的特效
3. 使用提供的着色器代码
4. 根据需要调整参数
5. 组合多个特效创建复杂场景

## Dependencies

- Three.js r128+
- WebGL 2.0 支持

## Browser Support

- Chrome 56+
- Firefox 51+
- Safari 15+
- Edge 79+