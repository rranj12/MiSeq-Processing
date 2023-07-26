import os
import subprocess

# -----------------------------------------------------------------------
# Variables and paths
# -----------------------------------------------------------------------

# Change working directory
if pipeline == 1 or pipeline == 2:
    if POOL_SAMPLE == "yes":
        dir = os.path.join(DRIVE_DIR, "processed_data", f"{RUN_NAME}_pooled_{STRINGENCY}")
    else:
        dir = os.path.join(DRIVE_DIR, "processed_data", f"{RUN_NAME}_{STRINGENCY}")

    folder = f"{RUN_NAME}_pooled_{STRINGENCY}" if POOL_SAMPLE == "yes" else f"{RUN_NAME}_{STRINGENCY}"
    os.makedirs(dir, exist_ok=True)

    # Save the log into a file
    log_file = os.path.join(dir, "printout.log")
    with open(log_file, "w"):
        pass

    sys.stdout = open(log_file, "a")
    sys.stderr = sys.stdout

    # Copy the samples list from the raw file folder
    shutil.copy(os.path.join(PATH_RAW_FILES, "sample_list.txt"), dir)
    shutil.copy(os.path.join(PATH_RAW_FILES, "amplicon_list.bed"), dir)

    # Define path to files and packages
    PATH_BOWTIE = os.path.join(DRIVE_DIR, "genomics-packages", "bowtie2-2.1.0")
    PATH_REF_GENOME = REF_GENOME
    PATH_CPG_REF = REF_GENOME
    PATH_BISMARK = os.path.join(DRIVE_DIR, "genomics-packages", "bismark_v0.8.2")

    # Export paths
    os.environ["PATH"] += os.pathsep + os.path.join(DRIVE_DIR, "genomics-packages/FastQC")
    os.environ["PATH"] += os.pathsep + os.path.join(DRIVE_DIR, "genomics-packages/cutadapt-1.4.2/bin")
    os.environ["PATH"] += os.pathsep + os.path.join(DRIVE_DIR, "genomics-packages")
    PATH_FASTQC = os.path.join(DRIVE_DIR, "genomics-packages", "FastQC")
    PATH_TRIM = os.path.join(DRIVE_DIR, "genomics-packages", "TrimGalore-0.4.5")

    # Convert files into LINUX format (usually they're created on Windows)
    shutil.copyfile(os.path.join(dir, "sample_list.txt"), os.path.join(dir, "tmp_file"))
    os.remove(os.path.join(dir, "sample_list.txt"))
    os.rename(os.path.join(dir, "tmp_file"), os.path.join(dir, "sample_list.txt"))

    shutil.copyfile(os.path.join(dir, "amplicon_list.bed"), os.path.join(dir, "tmp_file"))
    os.remove(os.path.join(dir, "amplicon_list.bed"))
    os.rename(os.path.join(dir, "tmp_file"), os.path.join(dir, "amplicon_list.bed"))

    # Convert spaces into underscores
    with open(os.path.join(dir, "amplicon_list.bed"), "r") as file:
        content = file.read().replace(" ", "_")
    with open(os.path.join(dir, "amplicon_list.bed"), "w") as file:
        file.write(content)

    with open(os.path.join(dir, "sample_list.txt"), "r") as file:
        content = file.read().replace(" ", "").replace("_", "-")
    with open(os.path.join(dir, "sample_list.txt"), "w") as file:
        file.write(content)

    print("*******************************************")
    print("*******************************************")
    print("PRINTING SAMPLE LIST FILE")
    with open(os.path.join(dir, "sample_list.txt"), "r") as file:
        print(file.read())
    print("*******************************************")
    print("*******************************************")

    # Create directories within the run folder in the processed folder
    os.makedirs(os.path.join(dir, "fastqc_pretrimming"), exist_ok=True)
    os.makedirs(os.path.join(dir, "fastqc_posttrimming"), exist_ok=True)
    os.makedirs(os.path.join(dir, "trimmed"), exist_ok=True)
    os.makedirs(os.path.join(dir, "aligned"), exist_ok=True)

