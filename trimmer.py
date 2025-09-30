import ffmpeg
import argparse

def parse_time(time_str):
    """
    Parse time string in format 'HH:MM:SS' or 'MM:SS' or 'SS' into seconds
    """
    if not time_str:
        return None
    parts = time_str.split(':')
    if len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    elif len(parts) == 2:  # MM:SS
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    elif len(parts) == 1:  # SS
        return float(parts[0])
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def main():
    parser = argparse.ArgumentParser(description="Video trimmer using ffmpeg")
    parser.add_argument('-i', '--input', required=True, help='Input video file path')
    parser.add_argument('-o', '--output', required=True, help='Output video file path')
    parser.add_argument('-ss', '--start', help='Start time (e.g., 00:01:30 for 1 min 30 sec)')
    parser.add_argument('-to', '--end', help='End time (e.g., 00:02:30 for 2 min 30 sec)')
    parser.add_argument('-ds', '--durationstart', help='Duration from start time (e.g., 00:01:00 for 1 min)')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    start_time = args.start
    end_time = args.end
    duration_start = args.durationstart

    if not start_time and not end_time and not duration_start:
        print("Error: At least one of start time, end time, or duration must be specified.")
        return
    if (start_time or end_time):
        if not (start_time and end_time):
            print("Error: Both start time and end time must be specified together.")
            return
    if duration_start and (start_time or end_time):
        print("Error: Duration parameters cannot be used with start/end time parameters.")
        return

    if start_time:
        start_time = parse_time(start_time)
    if end_time:
        end_time = parse_time(end_time)
    if duration_start:
        duration_start = parse_time(duration_start)

    try:
        stream = ffmpeg.input(input_file, ss=start_time if start_time else 0)
        output_options = {
            'c:v': 'copy',
            'c:a': 'copy'
        }

        if end_time is not None:
            output_options['to'] = end_time - (start_time if start_time else 0)
        elif duration_start is not None:
            output_options['t'] = duration_start

        stream = ffmpeg.output(stream, output_file, **output_options)

        ffmpeg.run(stream, overwrite_output=True)
        print(f"Video trimmed successfully: {output_file}")

    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if hasattr(e, 'stderr') and e.stderr else str(e)
        print(f"Error trimming video: {stderr}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()