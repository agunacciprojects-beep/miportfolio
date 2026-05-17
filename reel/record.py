"""Record reel.html as a 16-second 1080x1920 video using Playwright,
then convert to MP4 with ffmpeg."""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REEL_HTML = HERE / "reel.html"
OUT_DIR = HERE / "_video_raw"
FINAL_MP4 = HERE / "naccitech-reel.mp4"

ANIMATION_DURATION = 16.0  # seconds
EXTRA_BUFFER = 1.0          # extra time after animation completes

VIEWPORT = {"width": 1080, "height": 1920}

def clean_output_dir():
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

def record():
    clean_output_dir()
    file_url = "file:///" + str(REEL_HTML).replace("\\", "/")
    print(f"[record] opening {file_url}")
    print(f"[record] viewport {VIEWPORT['width']}x{VIEWPORT['height']}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--disable-web-security",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--force-device-scale-factor=1",
        ])
        context = browser.new_context(
            viewport=VIEWPORT,
            record_video_dir=str(OUT_DIR),
            record_video_size=VIEWPORT,
            device_scale_factor=1,
        )
        page = context.new_page()
        page.goto(file_url)

        # Wait for body.start class (set after fonts.ready)
        print("[record] waiting for fonts to load (body.start) ...")
        page.wait_for_function(
            "document.body.classList.contains('start')",
            timeout=30000
        )
        print("[record] animations started, recording for {} seconds".format(
            ANIMATION_DURATION + EXTRA_BUFFER
        ))

        # Wait for the full animation duration + small buffer
        page.wait_for_timeout(int((ANIMATION_DURATION + EXTRA_BUFFER) * 1000))

        context.close()
        browser.close()

    # Find generated .webm file
    webm_files = list(OUT_DIR.glob("*.webm"))
    if not webm_files:
        print("[error] no webm video was produced")
        return None
    webm = webm_files[0]
    print(f"[record] raw video: {webm}")
    return webm

def convert_to_mp4(webm_path):
    """Convert webm -> mp4 with H.264/AAC, IG-compatible."""
    if FINAL_MP4.exists():
        FINAL_MP4.unlink()

    # Trim first 0.8s (font-load flash + initial blank frames before body.start)
    # and limit total duration to 16 seconds to match the animation timeline.
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", "0.8",
        "-i", str(webm_path),
        "-t", "16",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30",
        "-movflags", "+faststart",
        "-an",  # no audio
        str(FINAL_MP4),
    ]
    print("[ffmpeg] converting ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[ffmpeg ERROR]")
        print(result.stderr[-2000:])
        return False
    print(f"[ffmpeg] done: {FINAL_MP4}")
    return True

def main():
    if not REEL_HTML.exists():
        print(f"[error] not found: {REEL_HTML}")
        sys.exit(1)
    webm = record()
    if webm is None:
        sys.exit(1)
    ok = convert_to_mp4(webm)
    if not ok:
        sys.exit(1)
    size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
    print(f"\nFINAL: {FINAL_MP4}  ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
