export const captionStyles = ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"] as const;

export type CaptionStyle = (typeof captionStyles)[number];
