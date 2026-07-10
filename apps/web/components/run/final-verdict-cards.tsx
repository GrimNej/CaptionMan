const captions = [
  [
    "Formal",
    "A short clip with a visible subject and simple action is presented in a concise video scene.",
  ],
  [
    "Sarcastic",
    "A short clip with a visible subject and simple action, because subtlety clearly wanted a camera crew.",
  ],
  [
    "Humorous Tech",
    "A short clip with a visible subject and simple action compiles into a surprisingly watchable visual event.",
  ],
  [
    "Humorous Non-Tech",
    "A short clip with a visible subject and simple action takes a tiny victory lap on screen.",
  ],
];

export function FinalVerdictCards() {
  return (
    <div className="caption-grid">
      {captions.map(([label, text]) => (
        <article className="caption-card" key={label}>
          <h3>{label}</h3>
          <p>{text}</p>
        </article>
      ))}
    </div>
  );
}
