import ffmpeg
import argparse
import os

allowed_extensions = ['mp4', 'avi', 'mkv', 'mov', 'flv', 'wmv', 'webm', 'mpg', 'mpeg', '3gp', 'ts', 'vob', 'ogv', 'rmvb']

def main():
    try:
        parser = argparse.ArgumentParser(description="Video file union tool using ffmpeg" \
        "Usage: python union.py -o output.mp4 input1.mp4 input2.avi input3.mkv")
        parser.add_argument('-o', '--output', required=True, help='Output video file path')
        parser.add_argument('videos', nargs='+', help='Input video file paths to be merged')
        args = parser.parse_args()

        output_file = args.output
        videos = args.videos

        for video in videos:
            if not os.path.exists(video):
                print(f"Error: The file '{video}' does not exist.")
                return
            if not any(video.lower().endswith(ext) for ext in allowed_extensions):
                print(f"Error: The file '{video}' has an unsupported extension.")
                return

        video_inputs = [ffmpeg.input(video) for video in videos]
        streams = []

        for video_stream in video_inputs:
            streams.append(video_stream.video)
            streams.append(video_stream.audio)

        joined = ffmpeg.concat(*streams, v=1, a=1).node
        output = ffmpeg.output(joined[0], joined[1], output_file, **{'c:v': 'libx264', 'c:a': 'aac'})

        print("Merging videos...")
        ffmpeg.run(output, overwrite_output=True)
        print(f"Videos merged successfully into: {output_file}")

    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if hasattr(e, 'stderr') and e.stderr else str(e)
        print(f"Error merging videos: {stderr}")
    # except TypeError:
    #     print("Error: No output defined or videos provided.")
    #     return



if __name__ == "__main__":
    main()