/**
 * Screenshot each .slide from an HTML file using dev-browser,
 * then assemble into a PPTX with pptxgenjs.
 */
import { connect } from "@/client.js";
import pptxgen from "pptxgenjs";
import fs from "fs";
import path from "path";

const INPUT_HTML = process.argv[2];
const OUTPUT_PPTX = process.argv[3];

if (!INPUT_HTML || !OUTPUT_PPTX) {
  console.error("Usage: node screenshot-slides.mjs <input.html> <output.pptx>");
  process.exit(1);
}

const TMP_DIR = "C:/Users/clown/.claude/skills/html-to-pptx/tmp";
fs.mkdirSync(TMP_DIR, { recursive: true });

const client = await connect();
const page = await client.page("slide-capture", { viewport: { width: 1280, height: 720 } });

const absPath = path.resolve(INPUT_HTML).replace(/\\/g, "/");
await page.goto(`file:///${absPath}`);
await page.waitForTimeout(2000);

// Count slides
const slideCount = await page.evaluate(() => document.querySelectorAll(".slide").length);
console.log(`Found ${slideCount} slides`);

const screenshots = [];

for (let i = 0; i < slideCount; i++) {
  // Activate slide i
  await page.evaluate((idx) => {
    const slides = document.querySelectorAll(".slide");
    slides.forEach((s, j) => {
      s.style.opacity = j === idx ? "1" : "0";
      s.style.pointerEvents = j === idx ? "all" : "none";
    });
    // Force all .r elements visible (bypass CSS animation opacity:0)
    const activeSlide = slides[idx];
    activeSlide.querySelectorAll(".r").forEach(el => {
      el.style.opacity = "1";
      el.style.transform = "none";
      el.style.animation = "none";
    });
  }, i);

  await page.waitForTimeout(600);

  const imgPath = path.join(TMP_DIR, `slide_${i}.png`);
  await page.screenshot({ path: imgPath, type: "png" });
  screenshots.push(imgPath);
  console.log(`  Captured slide ${i + 1}/${slideCount}`);
}

await client.disconnect();

// Assemble PPTX
const prs = new pptxgen();
prs.layout = "LAYOUT_16x9";

for (const imgPath of screenshots) {
  const slide = prs.addSlide();
  const data = fs.readFileSync(imgPath);
  const b64 = data.toString("base64");
  slide.addImage({
    data: `image/png;base64,${b64}`,
    x: 0, y: 0, w: "100%", h: "100%",
  });
}

await prs.writeFile({ fileName: OUTPUT_PPTX });
console.log(`\nSaved: ${OUTPUT_PPTX}`);

// Cleanup
for (const f of screenshots) fs.unlinkSync(f);
