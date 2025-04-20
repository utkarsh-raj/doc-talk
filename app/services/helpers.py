import os

def transcript_to_string(transcript: str) -> str:
    lines = transcript.splitlines()
    output = []
    
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            speaker = parts[0].strip()
            statement = parts[1].strip()
            if statement:  # Ignore empty lines or music cues
                output.append(f"{speaker}:{statement}")
    
    return ".".join(output) + "."

def get_directory_size(directory_path):
    total_size = 0
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        return 0
        
    for path, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
                
    return total_size