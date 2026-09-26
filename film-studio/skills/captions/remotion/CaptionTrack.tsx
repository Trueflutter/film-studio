/**
 * CaptionTrack: animated social captions for Remotion.
 *
 * The studio's house caption look as a reusable component: bold type, soft dark stroke
 * painted behind the fill, a two-layer drop shadow, no box. Words enter at their spoken
 * onset (a small rise and fade), the word being spoken is highlighted and lifted slightly,
 * and "signal words" get a second accent colour. Caption blocks fade in and out over a few
 * frames. Every value is derived from the frame number (Remotion renders frames in parallel).
 *
 * Usage:
 *   <AbsoluteFill>
 *     <OffthreadVideo src={staticFile("cut.mp4")} />
 *     <CaptionTrack events={events} accent="#F5C542" signalWords={["free", "today"]} />
 *   </AbsoluteFill>
 *
 * `events` is the caption list: [{start, end, words: [{text, start, end}]}] in seconds, e.g.
 * converted from the words JSON that `film captions` uses.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Poppins";

const { fontFamily: poppins } = loadFont("normal", { weights: ["700", "800"], subsets: ["latin"] });

export type CaptionWord = { text: string; start: number; end: number };
export type CaptionEvent = { start: number; end: number; words: CaptionWord[] };

export type CaptionTrackProps = {
  events: CaptionEvent[];
  /** Colour of the word being spoken. */
  accent?: string;
  /** Words (lower case, punctuation ignored) that always use `signalAccent` when spoken. */
  signalWords?: string[];
  signalAccent?: string;
  colour?: string;
  strokeColour?: string;
  fontFamily?: string;
  /** Font size as a fraction of the frame's short side (0.065 ≈ 70px at 1080). */
  size?: number;
  /** Distance of the caption block's bottom edge from the frame bottom, as a fraction of height. */
  bottom?: number;
  /** Max text width as a fraction of frame width. */
  maxWidth?: number;
  /** Scale of the spoken word (1 = no pop). */
  pop?: number;
};

const norm = (w: string) => w.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");

const Word: React.FC<{
  word: CaptionWord;
  time: number;
  accent: string;
  signal: boolean;
  signalAccent: string;
  colour: string;
  pop: number;
}> = ({ word, time, accent, signal, signalAccent, colour, pop }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const onset = word.start * fps;
  const enter = interpolate(frame, [onset - 2, onset + 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const active = time >= word.start && time < word.end;
  return (
    <span
      style={{
        display: "inline-block",
        marginRight: "0.24em",
        opacity: enter,
        color: active ? (signal ? signalAccent : accent) : colour,
        transform: `translateY(${(1 - enter) * 12}px) scale(${active ? pop : 1})`,
      }}
    >
      {word.text}
    </span>
  );
};

const Block: React.FC<{ event: CaptionEvent } & Required<Omit<CaptionTrackProps, "events">>> = ({
  event,
  accent,
  signalWords,
  signalAccent,
  colour,
  strokeColour,
  fontFamily,
  size,
  bottom,
  maxWidth,
  pop,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const start = event.start * fps;
  const end = event.end * fps;
  if (frame < start || frame >= end) return null;
  const opacity = interpolate(frame, [start, start + 4, end - 4, end], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const px = Math.round(Math.min(width, height) * size);
  const signals = new Set(signalWords.map(norm));
  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: height * bottom,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          opacity,
          fontFamily,
          fontSize: px,
          fontWeight: 800,
          lineHeight: 1.08,
          color: colour,
          maxWidth: width * maxWidth,
          textAlign: "center",
          WebkitTextStroke: `${Math.max(2, Math.round(px * 0.04))}px ${strokeColour}`,
          paintOrder: "stroke fill",
          textShadow: "0 8px 22px rgba(0,0,0,0.62), 0 2px 5px rgba(0,0,0,0.85)",
          textWrap: "balance" as React.CSSProperties["textWrap"],
        }}
      >
        {event.words.map((w, i) => (
          <Word
            key={`${event.start}-${i}`}
            word={w}
            time={frame / fps}
            accent={accent}
            signal={signals.has(norm(w.text))}
            signalAccent={signalAccent}
            colour={colour}
            pop={pop}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const CaptionTrack: React.FC<CaptionTrackProps> = ({
  events,
  accent = "#F5C542",
  signalWords = [],
  signalAccent = "#10B981",
  colour = "#FFFFFF",
  strokeColour = "rgba(0,0,0,0.62)",
  fontFamily = poppins,
  size = 0.065,
  bottom = 0.3,
  maxWidth = 0.8,
  pop = 1.075,
}) => (
  <AbsoluteFill style={{ backgroundColor: "transparent" }}>
    {events.map((e, i) => (
      <Block
        key={`${e.start}-${i}`}
        event={e}
        accent={accent}
        signalWords={signalWords}
        signalAccent={signalAccent}
        colour={colour}
        strokeColour={strokeColour}
        fontFamily={fontFamily}
        size={size}
        bottom={bottom}
        maxWidth={maxWidth}
        pop={pop}
      />
    ))}
  </AbsoluteFill>
);
