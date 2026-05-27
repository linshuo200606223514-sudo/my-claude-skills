#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frame Calculator for Remotion TransitionSeries compositions.

Computes absolute frame ranges for every scene and transition, detects dead air,
and analyses spring damping ratios so problems are caught before code is written.

Usage examples:

  # Basic timeline (6 scenes, 15f transitions)
  python scripts/frame_calculator.py \\
    --fps 30 \\
    --durations 150 180 150 210 200 120 \\
    --transition 15 \\
    --names "Hook" "Definition" "Solution" "Demo" "Processing" "Dialogue"

  # With spring analysis
  python scripts/frame_calculator.py \\
    --fps 30 \\
    --durations 150 180 150 210 200 120 \\
    --transition 15 \\
    --springs "staccatoPop:28:400" "brokenPop:8:400" "titleSpring:10:300"

  # With dead-air detection (pass the last animation end frame per scene, local)
  python scripts/frame_calculator.py \\
    --fps 30 \\
    --durations 150 180 150 210 200 120 \\
    --transition 15 \\
    --last-anim 125 158 130 178 177 95

Output:
  - Absolute frame map with transition overlap windows
  - Absolute ↔ local frame conversions for every scene
  - Dead air warnings if a scene holds idle for > MAX_IDLE_FRAMES after its last animation
  - Spring ζ (damping ratio) and estimated settle time for every config supplied
"""

import argparse
import math
import sys

# Force UTF-8 output so Unicode symbols print correctly on all terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Maximum acceptable idle frames at the end of a scene before the transition
# begins. Beyond this the scene feels static and loses the viewer.
MAX_IDLE_FRAMES = 22


# ─── Timeline maths ───────────────────────────────────────────────────────────

def compute_timeline(durations: list[int], transition_duration: int):
    """
    Compute absolute start/end for every scene and every transition window.

    TransitionSeries maths:
      - Each transition OVERLAPS the tail of the exiting scene and the head of
        the entering scene by `transition_duration` frames.
      - Scene N+1's local frame 0 starts at the same absolute frame as the
        start of transition N.
      - TOTAL = sum(durations) - (num_scenes - 1) * transition_duration

    Returns:
      scene_starts  : list[int]  absolute start of each scene
      scene_ends    : list[int]  absolute end of each scene (inclusive)
      transitions   : list[tuple[int,int]]  (abs_start, abs_end) of each transition window
      total         : int  total composition frames
    """
    n = len(durations)
    scene_starts = []
    scene_ends = []
    transitions = []

    abs_start = 0
    for i, dur in enumerate(durations):
        scene_starts.append(abs_start)
        scene_ends.append(abs_start + dur - 1)

        if i < n - 1:
            # Transition window = last `transition_duration` frames of this scene
            # = first `transition_duration` frames of the next scene (overlap)
            trans_abs_start = abs_start + dur - transition_duration
            trans_abs_end   = abs_start + dur - 1
            transitions.append((trans_abs_start, trans_abs_end))
            # Next scene's local-0 = abs frame where the transition starts
            abs_start = trans_abs_start

    total = sum(durations) - (n - 1) * transition_duration
    return scene_starts, scene_ends, transitions, total


def abs_to_local(abs_frame: int, scene_abs_start: int) -> int:
    return abs_frame - scene_abs_start


def local_to_abs(local_frame: int, scene_abs_start: int) -> int:
    return local_frame + scene_abs_start


# ─── Spring physics ───────────────────────────────────────────────────────────

def damping_ratio(damping: float, stiffness: float, mass: float = 1.0) -> float:
    """
    ζ = c / (2 * sqrt(k * m))

    Interpretation:
      ζ < 0.5   Heavily underdamped — continuous bouncing, never settles cleanly.
                Wrong for staccato pops or slide entrances. Looks amateurish.
      0.5–0.85  Lightly underdamped — single clean overshoot then settles.
                The sweet spot for staccato pops and energetic entrances.
      0.85–1.0  Near-critically damped — minimal overshoot, smooth settle.
                Good for slides and magnetic-click moments.
      > 1.0     Overdamped — no overshoot, slow creep to target.
                Good for deliberate heavy-object entrance, not for snappy pops.
    """
    return damping / (2.0 * math.sqrt(stiffness * mass))


def spring_settle_frames(
    damping: float,
    stiffness: float,
    fps: int = 30,
    mass: float = 1.0,
    threshold: float = 0.01,
    max_seconds: int = 8,
) -> int:
    """
    Simulate a Remotion-style spring (semi-implicit Euler) and return the
    frame at which the output is within `threshold` of the target (1.0) and
    velocity is also below `threshold`.

    Returns max_seconds * fps if the spring never settles within that window.
    """
    dt = 1.0 / fps
    pos, vel = 0.0, 0.0
    for frame in range(fps * max_seconds):
        acc = -stiffness * (pos - 1.0) - damping * vel
        vel += acc * dt
        pos += vel * dt
        if abs(pos - 1.0) < threshold and abs(vel) < threshold:
            return frame
    return fps * max_seconds


def spring_behavior_label(zeta: float) -> str:
    if zeta < 0.5:
        return "UNDERDAMPED — continuous oscillation. WRONG for pops/slides."
    elif zeta < 0.85:
        return "LIGHTLY UNDERDAMPED — single overshoot, snappy settle. Good."
    elif zeta <= 1.0:
        return "NEAR-CRITICAL — smooth settle, no overshoot. Good for slides."
    else:
        return "OVERDAMPED — slow creep, no overshoot. Use for heavy entrances."


# ─── Dead air detection ───────────────────────────────────────────────────────

def dead_air_frames(scene_duration: int, last_anim_local: int, transition_duration: int) -> int:
    """
    Returns the number of idle frames between the last authored animation end
    and the start of the outgoing transition.

    idle = (scene_duration - transition_duration) - last_anim_local
    If the last animation ends after the transition start, returns 0
    (the scene is still animating during the exit — which is fine, just note it).
    """
    transition_start_local = scene_duration - transition_duration
    idle = transition_start_local - last_anim_local
    return max(0, idle)


# ─── Formatters ───────────────────────────────────────────────────────────────

def print_timeline(
    durations: list[int],
    transition_duration: int,
    fps: int,
    scene_names: list[str] | None = None,
    last_anim_locals: list[int] | None = None,
):
    n = len(durations)
    if scene_names is None:
        scene_names = [f"Scene {i + 1}" for i in range(n)]

    scene_starts, scene_ends, transitions, total = compute_timeline(durations, transition_duration)

    W = 70
    print("=" * W)
    print("  ABSOLUTE FRAME TIMELINE")
    print(f"  FPS: {fps}  |  Transition: {transition_duration}f each  |  Total: {total}f = {total / fps:.2f}s")
    print("=" * W)

    for i, (name, dur) in enumerate(zip(scene_names, durations)):
        s = scene_starts[i]
        e = scene_ends[i]
        print(f"\n  [{s:>4}-{e:>4}]  SCENE {i + 1}: {name}  ({dur}f = {dur / fps:.1f}s)")
        print(f"              local 0 = absolute {s}  |  local {dur - 1} = absolute {e}")

        # Dead air check
        if last_anim_locals is not None:
            lal = last_anim_locals[i]
            idle = dead_air_frames(dur, lal, transition_duration)
            trans_start_local = dur - transition_duration
            if idle > MAX_IDLE_FRAMES:
                print(f"              [!] DEAD AIR: last animation ends local {lal},")
                print(f"                  transition exit starts local {trans_start_local}.")
                print(f"                  {idle}f of idle frames -- shorten scene by ~{idle - MAX_IDLE_FRAMES}f.")
            elif idle > 0:
                print(f"              [ok] Hold: local {lal}-{trans_start_local - 1} ({idle}f idle -- within {MAX_IDLE_FRAMES}f budget)")
            else:
                print(f"              [ok] Still animating through transition exit (local {lal} >= {trans_start_local})")

        if i < n - 1:
            ts, te = transitions[i]
            next_name = scene_names[i + 1]
            next_start = scene_starts[i + 1]
            s1_local_start = abs_to_local(ts, s)
            s1_local_end   = abs_to_local(te, s)
            s2_local_end   = transition_duration - 1
            print(f"\n  [{ts:>4}-{te:>4}]  -- TRANSITION {i + 1}->{i + 2}  ({transition_duration}f) --")
            print(f"              {name:<20}  local {s1_local_start}-{s1_local_end}  [exiting]")
            print(f"              {next_name:<20}  local 0-{s2_local_end}  [entering]")
            print(f"              Scene {i + 2} local 0 = absolute {next_start}")

    print(f"\n{'=' * W}")
    print(f"  TOTAL: {total} frames = {total / fps:.2f}s")
    print(f"  Verify: sum({' + '.join(str(d) for d in durations)}) - ({n - 1} x {transition_duration}) = {sum(durations)} - {(n - 1) * transition_duration} = {total}")
    print(f"{'=' * W}\n")


def print_spring_analysis(configs: list[tuple[str, float, float, float]], fps: int):
    W = 70
    print("=" * W)
    print("  SPRING ANALYSIS")
    print("=" * W)
    for label, d, s, m in configs:
        z = damping_ratio(d, s, m)
        settle = spring_settle_frames(d, s, fps, m)
        behavior = spring_behavior_label(z)
        print(f"\n  {label}")
        print(f"    damping={d}  stiffness={s}  mass={m}")
        print(f"    zeta = {z:.3f}  ->  {behavior}")
        print(f"    Settles in ~{settle}f ({settle / fps:.2f}s)")
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Remotion frame calculator — timeline, transitions, springs, dead air",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--fps", type=int, default=30,
                        help="Frames per second (default: 30)")
    parser.add_argument("--durations", nargs="+", type=int, required=True,
                        help="Scene durations in frames, space-separated")
    parser.add_argument("--transition", type=int, default=15,
                        help="Shared transition duration in frames (default: 15)")
    parser.add_argument("--names", nargs="+", type=str,
                        help="Optional scene names (must match count of --durations)")
    parser.add_argument("--last-anim", nargs="+", type=int,
                        dest="last_anim",
                        help="Local frame of last authored animation per scene (for dead-air check)")
    parser.add_argument("--springs", nargs="+", type=str,
                        help="Spring configs: 'label:damping:stiffness[:mass]'")

    args = parser.parse_args()

    # Validate
    n = len(args.durations)
    if args.names and len(args.names) != n:
        print(f"ERROR: --names count ({len(args.names)}) must match --durations count ({n})", file=sys.stderr)
        sys.exit(1)
    if args.last_anim and len(args.last_anim) != n:
        print(f"ERROR: --last-anim count ({len(args.last_anim)}) must match --durations count ({n})", file=sys.stderr)
        sys.exit(1)
    if args.transition >= min(args.durations):
        print(f"WARNING: transition ({args.transition}f) is >= the shortest scene duration "
              f"({min(args.durations)}f). This will produce unexpected results.", file=sys.stderr)

    print_timeline(args.durations, args.transition, args.fps, args.names, args.last_anim)

    if args.springs:
        configs = []
        for spec in args.springs:
            parts = spec.split(":")
            if len(parts) < 3:
                print(f"WARNING: Skipping malformed spring spec '{spec}' (expected label:damping:stiffness[:mass])",
                      file=sys.stderr)
                continue
            label     = parts[0]
            damping   = float(parts[1])
            stiffness = float(parts[2])
            mass      = float(parts[3]) if len(parts) > 3 else 1.0
            configs.append((label, damping, stiffness, mass))
        if configs:
            print_spring_analysis(configs, args.fps)


if __name__ == "__main__":
    main()
