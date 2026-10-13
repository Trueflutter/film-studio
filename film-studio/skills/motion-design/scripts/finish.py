#!/usr/bin/env python3
"""Cinematic finishing for a generated take: speed ramps, flash frames, zoom punches, whip blurs,
light leaks, halation and grain. ffmpeg only (needs ffmpeg 6+ on PATH). Standard library only.

  python3 finish.py TAKE.mp4 OUT.mp4 [--ramp 4.2-5.8:0.45] [--flash 8.0] [--zoom 3.0] [--whip 6.0]
                   [--leak 8.0:0.8] [--halation 0.2] [--grain 5] [--fps 24] [--no-audio] [--dry-run]

Every time is in the TAKE's own seconds (read them off the take); the script maps them onto the
output after ramps change the timeline. Repeat --ramp/--flash/--zoom/--whip/--leak as needed.

  --ramp A-B:S   play source A..B at speed S (0.25-4). Eased in and out so it never jerks.
                 Slow segments are motion-interpolated (smooth slow motion, not repeated frames).
  --flash T      a 2-frame white flash at T (put it on the music drop or a hard cut).
  --zoom T       a zoom punch into a cut at T: pushes 1.0 to 1.14 over 0.25 s, lands on the cut, eases back.
  --whip T       a horizontal motion-blur whip across T (about 0.12 s), hides a cut in movement.
  --leak T:D     a warm light leak that blooms at T for D seconds.
  --halation K   red-orange glow around highlights (0.1 subtle to 0.35 strong).
  --grain N      film grain strength (3 subtle to 8 visible).
"""
import argparse, json, subprocess, sys
from pathlib import Path


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True)
    d = json.loads(out.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    has_a = any(s["codec_type"] == "audio" for s in d["streams"])
    return int(v["width"]), int(v["height"]), float(d["format"]["duration"]), has_a


def segments(duration, ramps):
    """Split the source into (start, end, speed) pieces. Each ramp gets eased edges."""
    ramps = sorted(ramps)
    pieces, cur = [], 0.0
    for a, b, s in ramps:
        if a < cur or b > duration + 1e-6 or b <= a:
            sys.exit(f"ramp {a}-{b} overlaps another or runs past the take ({duration:.2f}s)")
        if a > cur:
            pieces.append((cur, a, 1.0))
        edge = min(0.2, (b - a) / 4)
        mid = (1.0 + s) / 2
        pieces += [(a, a + edge, mid), (a + edge, b - edge, s), (b - edge, b, mid)]
        cur = b
    if cur < duration:
        pieces.append((cur, duration, 1.0))
    return [p for p in pieces if p[1] - p[0] > 1e-3]


def mapper(pieces):
    def out_t(t):
        acc = 0.0
        for a, b, s in pieces:
            if t <= b:
                return acc + (max(t, a) - a) / s
            acc += (b - a) / s
        return acc
    return out_t


def atempo_chain(speed):
    parts, s = [], speed
    while s < 0.5:
        parts.append("atempo=0.5"); s /= 0.5
    while s > 2.0:
        parts.append("atempo=2.0"); s /= 2.0
    parts.append(f"atempo={s:.4f}")
    return ",".join(parts)


def build(a):
    W, H, dur, has_a = probe(a.take)
    audio = has_a and not a.no_audio
    fps = a.fps
    ramps = []
    for r in a.ramp:
        span, s = r.split(":")
        x, y = span.split("-")
        s = float(s)
        if not 0.25 <= s <= 4:
            sys.exit("ramp speed must be between 0.25 and 4")
        ramps.append((float(x), float(y), s))
    pieces = segments(dur, ramps)
    T = mapper(pieces)

    g, vlabels, alabels = [], [], []
    for i, (s0, s1, sp) in enumerate(pieces):
        chain = f"[0:v]trim=start={s0:.4f}:end={s1:.4f},setpts=(PTS-STARTPTS)/{sp:.4f}"
        if sp < 0.95:
            chain += f",minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
        chain += f",fps={fps}[v{i}]"
        g.append(chain); vlabels.append(f"[v{i}]")
        if audio:
            g.append(f"[0:a]atrim=start={s0:.4f}:end={s1:.4f},asetpts=PTS-STARTPTS,{atempo_chain(sp)}[a{i}]")
            alabels.append(f"[a{i}]")
    n = len(pieces)
    if audio:
        g.append("".join(v + al for v, al in zip(vlabels, alabels)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    else:
        g.append("".join(vlabels) + f"concat=n={n}:v=1:a=0[vc]")

    post = ["format=yuv420p"]
    # zoom punches: z(t) = 1 + bumps; zoompan works per input frame (in / fps = output seconds)
    if a.zoom:
        bumps = []
        for z in a.zoom:
            c = T(z)
            bumps.append(f"if(between(in/{fps},{c-0.25:.3f},{c:.3f}),0.14*pow((in/{fps}-{c-0.25:.3f})/0.25,2),"
                         f"if(between(in/{fps},{c:.3f},{c+0.3:.3f}),0.14*pow(1-(in/{fps}-{c:.3f})/0.3,2),0))")
        z_expr = "1+" + "+".join(bumps)
        post.append(f"zoompan=z='{z_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={fps}")
    for w in a.whip:
        c = T(w)
        post.append(f"dblur=angle=0:radius=48:enable='between(t,{c-0.06:.3f},{c+0.06:.3f})'")
        post.append(f"dblur=angle=0:radius=20:enable='between(t,{c-0.12:.3f},{c+0.12:.3f})'")
    for f in a.flash:
        c = T(f)
        post.append(f"eq=brightness=0.55:contrast=0.7:enable='between(t,{c:.3f},{c + 2.0/fps - 0.001:.3f})'")
    g.append("[vc]" + ",".join(post) + "[vp]")
    last = "[vp]"

    if a.halation > 0:
        g.append(f"{last}format=gbrp,split[hm][hh]")
        g.append("[hh]curves=all='0/0 0.72/0 1/1',gblur=sigma=24,"
                 "colorchannelmixer=rr=1:gg=0.38:bb=0.22[hglow]")
        g.append(f"[hm][hglow]blend=all_mode=screen:all_opacity={a.halation:.3f}[vh]")
        last = "[vh]"
    for i, l in enumerate(a.leak):
        t, d = (float(x) for x in l.split(":"))
        s, e = T(t), T(t) + d
        g.append(f"gradients=s={W}x{H}:c0=0xff7a2a:c1=0x000000:x0={int(W*0.85)}:y0={int(H*0.2)}:"
                 f"x1={int(W*0.2)}:y1={int(H*0.9)}:type=radial:r={fps},format=gbrp[lk{i}]")
        env = f"(clip((T-{s:.3f})/0.18,0,1)*clip(({e:.3f}-T)/0.4,0,1)*0.55)"
        g.append(f"{last}format=gbrp[lb{i}]")
        g.append(f"[lb{i}][lk{i}]blend=shortest=1:all_expr='A+B*{env}-A*B*{env}/255'[vl{i}]")
        last = f"[vl{i}]"
    if a.grain > 0:
        g.append(f"{last}noise=alls={a.grain}:allf=t,format=yuv420p[vg]")
        last = "[vg]"
    else:
        g.append(f"{last}format=yuv420p[vg]")
        last = "[vg]"

    cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(a.take),
           "-filter_complex", ";".join(g), "-map", last]
    if audio:
        cmd += ["-map", "[ac]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-crf", "16", "-preset", "slow", "-r", str(fps),
            "-movflags", "+faststart", str(a.out)]
    total = sum((b - x) / s for x, b, s in pieces)
    return cmd, total, {k: [round(T(x), 3) for x in getattr(a, k)] for k in ("flash", "zoom", "whip")}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("take", type=Path); p.add_argument("out", type=Path)
    p.add_argument("--ramp", action="append", default=[])
    p.add_argument("--flash", action="append", type=float, default=[])
    p.add_argument("--zoom", action="append", type=float, default=[])
    p.add_argument("--whip", action="append", type=float, default=[])
    p.add_argument("--leak", action="append", default=[])
    p.add_argument("--halation", type=float, default=0.0)
    p.add_argument("--grain", type=float, default=0.0)
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--no-audio", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    cmd, total, marks = build(a)
    print(f"output length {total:.2f}s; effect times in the output: {marks}")
    if a.dry_run:
        print(" ".join(f"'{c}'" if " " in c or ";" in c else c for c in cmd)); return
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit("ffmpeg failed (run with --dry-run to see the command)")
    print(f"wrote {a.out}  (note the output times above for graphics and sound cues)")


if __name__ == "__main__":
    main()
