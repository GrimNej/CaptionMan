const stages = ["Load", "Evidence", "Generate", "Judge", "Repair", "Export"];

export function PipelineProgress() {
  return (
    <div className="court">
      {stages.map((stage) => (
        <div className="court-row" key={stage}>
          <span>{stage}</span>
          <span className="score">pass</span>
        </div>
      ))}
    </div>
  );
}
