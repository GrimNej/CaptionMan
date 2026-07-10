# Official Schema Notes

The Track 2 official schema was confirmed from `extra_files/Participant Guide_ AMD Developer Hackathon (ACT II).pdf`.

- Input path: `/input/tasks.json`.
- Input top-level shape: JSON list.
- Each task includes `task_id`, `video_url`, and `styles`.
- Output path: `/output/results.json`.
- Output top-level shape: JSON list.
- Each result includes `task_id` and `captions`.
- `captions` contains the requested style keys: `formal`, `sarcastic`, `humorous_tech`, and `humorous_non_tech`.

No inference log is required for Track 2. The guide says hidden videos are 30 seconds to 2 minutes and scoring is based on caption accuracy and style match.
