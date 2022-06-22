OUTPUT=$1
SAMPLES=$2

srun -p video --job-name=rt --ntasks=1 --cpus-per-task=32 --async \
    python src\main.py --output ${OUTPUT} --samples ${SAMPLES}
