import ffmpeg
import argparse

def main():
    parser = argparse.ArgumentParser(description="Video Compressor using ffmpeg")
    parser.add_argument('-i', '--input', required=True, help='Input video file path')
    parser.add_argument('-o', '--output', required=True, help='Output video file path')
    parser.add_argument('-b', '--bitrate', help='Target video bitrate (e.g., 1000k for 1000 kbps or just 1000 for 1000 kbps)')
    parser.add_argument('-fs', '--filesize', type=float, help='Target file size in MB (overrides bitrate if specified)')
    parser.add_argument('-v', '--version', action='version', version='Video Compressor 1.0')

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    target_bitrate = args.bitrate
    target_filesize = args.filesize

    if not target_bitrate and not target_filesize:
        print("Error: Either bitrate or filesize must be specified.")
        return
    if target_bitrate and target_filesize:
        print("Warning: Both bitrate and filesize specified. Filesize will take precedence.")

    if target_bitrate and not target_bitrate.endswith(('k', 'K', 'm', 'M')):
        try:
            bitrate_value = int(target_bitrate)
            target_bitrate = f"{bitrate_value}k"
            print(f"Interpreting bitrate as {target_bitrate}")
        except ValueError:
            print(f"Error: Bitrate value '{target_bitrate}' is not valid. Use format like '1000' or '1000k'.")
            return

    if target_filesize:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        audio_bitrate = 128000  # 128 kbps standard audio bitrate (low btw xd)
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
        if audio_streams:
            if 'bit_rate' in audio_streams[0]:
                audio_bitrate = int(audio_streams[0]['bit_rate'])
            elif 'channels' in audio_streams[0]:
                channels = int(audio_streams[0]['channels'])
                audio_bitrate = 64000 * channels  # Estimate based on channels

        audio_size_mb = (audio_bitrate * duration) / (8 * 1024 * 1024)

        overhead_factor = 0.08  # 8% overhead
        available_size_mb = target_filesize - audio_size_mb - (target_filesize * overhead_factor)

        if available_size_mb <= 0:
            print(f"Error: Target size {target_filesize}MB too small for this video")
            return

        video_bitrate = int((available_size_mb * 8 * 1024 * 1024) / duration)

        MIN_BITRATE = 100000
        if video_bitrate < MIN_BITRATE:
            print(f"Warning: Calculated bitrate ({video_bitrate//1000}k) is too low for reasonable quality.")
            print(f"Setting to minimum bitrate of {MIN_BITRATE//1000}k")
            video_bitrate = MIN_BITRATE
        target_bitrate = f"{video_bitrate // 1000}k"

        print(f"Calculated bitrate for {target_filesize}MB target: {target_bitrate}")

    if not target_bitrate:
        print("Error: Either bitrate or filesize must be specified.")
        return

    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, video_bitrate=target_bitrate, audio_bitrate='128k')
            .run(overwrite_output=True)
        )
        print(f"Compression completed: {output_file} with bitrate {target_bitrate}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")


if __name__ == "__main__":
    main()