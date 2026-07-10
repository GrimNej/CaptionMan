const rows = [
  ["Formal", "0.94"],
  ["Sarcastic", "0.88"],
  ["Humorous Tech", "0.91"],
  ["Humorous Non-Tech", "0.90"],
];

export function CaptionCourtPanel() {
  return (
    <div className="court">
      {rows.map(([style, score]) => (
        <div className="court-row" key={style}>
          <span>{style}</span>
          <span className="score">{score}</span>
        </div>
      ))}
    </div>
  );
}
