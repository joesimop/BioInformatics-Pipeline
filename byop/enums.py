from enum import Enum

class FileType(Enum):
    FASTA = ".fasta"
    FASTQ = ".fastq"
    SAM = ".sam"
    BAM = ".bam"
    GFF = ".gff"
    GTF = ".gtf"
    TXT = ".txt"
    CSV = ".csv"
    TSV = ".tsv"
    DEFAULT = ".txt"

class PipleineStage(Enum):
    RAW = "Raw"
    BASECALL = "Basecalling"
    TRIM = "Trimming"
    ALIGN = "Alignment"
    COUNT = "Counting"
    NORMALIZE = "Normalization"
    MERGE = "Merging"
    ANNOTATE = "Annotation"
    ANALYZE = "Analyzing"
    DEFAULT = "raw"