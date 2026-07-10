const result = {
  task_id: "clip-001",
  captions: {
    formal:
      "A short clip with a visible subject and simple action is presented in a concise video scene.",
    sarcastic:
      "A short clip with a visible subject and simple action, because subtlety clearly wanted a camera crew.",
    humorous_tech:
      "A short clip with a visible subject and simple action compiles into a surprisingly watchable visual event.",
    humorous_non_tech:
      "A short clip with a visible subject and simple action takes a tiny victory lap on screen.",
  },
};

export function ResultsJsonPanel() {
  return <pre className="json-panel">{JSON.stringify([result], null, 2)}</pre>;
}
