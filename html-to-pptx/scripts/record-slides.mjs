/**
 * Record each slide transition from HTML as video frames,
 * then output a list of PNG frames for ffmpeg to compose.
 */
import { connect } from "@/client.js";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const INPUT_HTML = process.argv[2];
const OUTPUT_MP4 = process.argv[3] || "output.mp4";
const FPS = 30;
const SLIDE_DURATION = 3;    // seconds per slide
const TRANSITION_FRAMES = 20; // frames for ink transition

const TMP_DIR = "C:/Users/clown/.claude/skills/html-to-pptx/tmp/frames";
fs.mkdirSync(TMP_DIR, { recursive: true });
// clean up old frames
fs.readdirSync(TMP_DIR).forEach(f => fs.unlinkSync(path.join(TMP_DIR, f)));

const client = await connect();
const page = await client.page("recorder", { viewport: { width: 1280, height: 720 } });

const absPath = path.resolve(INPUT_HTML).replace(/\\/g, "/");
await page.goto(`file:///${absPath}`);
await page.waitForTimeout(1000);

const slideCount = await page.evaluate(() => document.querySelectorAll(".slide").length);
console.log(`Found ${slideCount} slides, recording...`);

// Helper: force show slide i with all content visible
async function showSlide(idx) {
  await page.evaluate((i) => {
    const slides = document.querySelectorAll(".slide");
    slides.forEach((s, j) => {
      s.style.opacity = j === i ? "1" : "0";
      s.style.pointerEvents = j === i ? "all" : "none";
      s.style.transition = "none";
    });
    const active = slides[i];
    active.querySelectorAll(".r").forEach(el => {
      el.style.opacity = "1";
      el.style.transform = "none";
      el.style.animation = "none";
    });
    // hide ink canvas
    const canvas = document.getElementById("ink-canvas");
    if (canvas) canvas.style.opacity = "0";
  }, idx);
  await page.waitForTimeout(100);
}

let frameIdx = 0;

async function captureFrame() {
  const p = path.join(TMP_DIR, `frame_${String(frameIdx).padStart(6, "0")}.png`);
  await page.screenshot({ path: p, type: "png" });
  frameIdx++;
}

for (let i = 0; i < slideCount; i++) {
  await showSlide(i);

  // Static frames for this slide
  const staticFrames = FPS * SLIDE_DURATION;
  for (let f = 0; f < staticFrames; f++) {
    await captureFrame();
  }

  // Transition to next slide (ink blob effect simulation)
  if (i < slideCount - 1) {
    for (let t = 0; t < TRANSITION_FRAMES; t++) {
      const progress = t / TRANSITION_FRAMES;
      await page.evaluate(({ curr, next, prog }) => {
        const slides = document.querySelectorAll(".slide");
        slides[curr].style.opacity = String(1 - prog);
        slides[next].style.opacity = String(prog);
        slides[next].style.pointerEvents = "all";
        slides[next].querySelectorAll(".r").forEach(el => {
          el.style.opacity = "1";
          el.style.transform = "none";
          el.style.animation = "none";
        });
      }, { curr: i, next: i + 1, prog: progress });
      await captureFrame();
    }
  }

  console.log(`  Slide ${i + 1}/${slideCount} done (${frameIdx} frames total)`);
}

await client.disconnect();

console.log(`\nTotal frames: ${frameIdx}`);
console.log("Composing video with ffmpeg...");

execSync(
  `ffmpeg -y -framerate ${FPS} -i "${TMP_DIR}/frame_%06d.png" -c:v libx264 -pix_fmt yuv420p -crf 18 "${OUTPUT_MP4}"`,
  { stdio: "inherit" }
);

console.log(`\nSaved: ${OUTPUT_MP4}`);
