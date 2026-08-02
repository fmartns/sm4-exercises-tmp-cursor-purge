# SM4: Python exercises

Optional exercises for the blog post on implementing SM4 from scratch in
Python, following the same building blocks as OpenSSL's `crypto/sm4/sm4.c`.

Constants and the S-box are already in `sm4.py`. You implement the functions
indicated in each notebook exercise. Tests live in the same file and use the
official GB/T 32907-2016 / OpenSSL test vector, so the work is about
implementing the algorithm rather than copying examples from the post.

Every exercise has an automated test. Move on only when the test passes.

## Setup

```bash
git clone https://github.com/fmartns/sm4-exercises.git
cd sm4-exercises
python3 -m venv .venv
```

Activate the virtual environment:

```bash
# Linux or macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Open the notebook:

```bash
jupyter notebook sm4_exercises.ipynb
```

For the Portuguese blog post, use `sm4_exercises_pt_br.ipynb`.

## How to work through the exercises

1. Read the matching section of the blog post up to the **Exercise** block.
2. Open the notebook at the exercise you are on (Exercises 1-8).
3. Implement the code in the cell below the instructions.
4. Run the test cell (the same cell calls `run(...)`).
5. Move on only when all tests pass.

If you get stuck, check `answers.py` only after trying on your own.

## License

Free to use for study.
