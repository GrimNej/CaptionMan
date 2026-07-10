const frames = ["00", "04", "08", "12", "16", "20", "24", "28"];

export function FrameTimeline() {
  return (
    <ul className="timeline" aria-label="Sampled frame timeline">
      {frames.map((frame) => (
        <li className="frame" key={frame} />
      ))}
    </ul>
  );
}
