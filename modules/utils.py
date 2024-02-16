import os

def append_texts(first_file_path, second_file_path):
    """
    Appends the content of the second file to the first file's content.
    """
    with open(first_file_path, 'r', encoding='utf-8') as first_file:
        first_content = first_file.read()

    with open(second_file_path, 'r', encoding='utf-8') as second_file:
        second_content = second_file.read()

    combined_content = f"{first_content}\n{second_content}"
    return combined_content

def save_transcript_to_file(transcripts, file_path):
    """
    Saves a list of transcript entries to a file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in transcripts:
            line = f"{entry['speaker']}({entry['start_time']} – {entry['end_time']}): {entry['transcript']}\n"
            file.write(line)

    print(f"Transcript saved to {file_path}")

def save_report(report):
    """
    Saves a report string to a uniquely named file within the 'results' directory.
    """
    try:
        count_reports = len(os.listdir('results'))
    except FileNotFoundError:
        os.makedirs('results')
        count_reports = 0

    report_file_path = f'results/report_{count_reports}.txt'
    with open(report_file_path, 'w', encoding='utf-8') as report_file:
        report_file.write(report)

def convert_time(seconds):
    """
    Converts seconds to a more readable format (hours, minutes, seconds).
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_parts = []
    if hours > 0:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_parts.append(f"{minutes} min")
    if seconds > 0 or not time_parts:
        time_parts.append(f"{seconds} sec")

    return ' '.join(time_parts)