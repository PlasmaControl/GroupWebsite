import os
from datetime import datetime
from moviepy.editor import VideoFileClip

def get_media_files(directory):
    # Create the thumbnails directory if it doesn't exist
    thumbnail_dir = os.path.join(directory, 'thumbnails')
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    # Get list of all media files (both images and videos) in the directory
    media_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Sort files by their creation time (or modification time)
    media_files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=False)

    # Generate Markdown with HTML-like syntax
    media_markdown = []
    media_markdown.append("---\n")
    media_markdown.append("toc_depth: 0\n")
    media_markdown.append("hide:\n")
    media_markdown.append("- navigation\n")
    media_markdown.append("- toc\n")
    media_markdown.append("disable_comments: true\n")
    media_markdown.append("---\n")
    media_markdown.append("# Media Gallery\n")
    media_markdown.append("<style>")
    media_markdown.append(".media-grid {")
    media_markdown.append("  column-count: 3;")  # Number of columns in the masonry layout
    media_markdown.append("  column-gap: 1em;")  # Gap between columns
    media_markdown.append("}")
    media_markdown.append(".media-grid img,")
    media_markdown.append(".media-grid video {")
    media_markdown.append("  width: 100%;")  # Each item takes the full width of the column
    media_markdown.append("  margin-bottom: 1em;")  # Vertical space between items
    media_markdown.append("  display: block;")  # Make sure images and videos are block elements
    media_markdown.append("  break-inside: avoid;")  # Avoid breaking items between columns
    media_markdown.append("}")
    media_markdown.append("@media (max-width: 800px) {")
    media_markdown.append("  .media-grid {")
    media_markdown.append("    column-count: 2;")  # Adjust to 2 columns for medium screens
    media_markdown.append("  }")
    media_markdown.append("}")
    media_markdown.append("@media (max-width: 500px) {")
    media_markdown.append("  .media-grid {")
    media_markdown.append("    column-count: 1;")  # Adjust to 1 column for small screens
    media_markdown.append("  }")
    media_markdown.append("}")
    media_markdown.append("</style>\n")
    media_markdown.append('<div class="media-grid">\n')


    # Add media elements (mixed images and videos based on date order)
    for file in media_files:
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Image formats
            media_markdown.append(f'  <img src="../gallerymedia/{file}" alt="{file}">\n')
        elif file.endswith('.mp4'):  # Video formats
            video_path = os.path.join(directory, file)
            thumbnail_path = os.path.join(thumbnail_dir, f'{os.path.splitext(file)[0]}.png')

            # Extract a frame from the middle of the video to use as a thumbnail
            try:
                clip = VideoFileClip(video_path)
                duration = clip.duration
                midpoint = duration / 2
                clip.save_frame(thumbnail_path, t=midpoint)
                clip.close()

                # Add the video with the thumbnail as the poster
                media_markdown.append(f'  <video src="../gallerymedia/{file}" controls poster="../gallerymedia/thumbnails/{os.path.basename(thumbnail_path)}"></video>\n')

            except Exception as e:
                print(f"Error processing {file}: {e}")
                media_markdown.append(f'  <video src="../gallerymedia/{file}" controls></video>\n')

    media_markdown.append("</div>\n")

    return ''.join(media_markdown)

# Get media files from the gallerymedia directory
media_markdown = get_media_files('src/gallerymedia')

# Save the generated Markdown to the media.md file
with open('src/media.md', 'w') as f:
    f.write(media_markdown)

print("Markdown file generated: src/media.md")
