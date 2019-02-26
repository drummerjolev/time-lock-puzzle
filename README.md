# Time Lock Puzzle Implementation

## Getting Started

This repository is a Python implementation of the excellent paper [Time-lock puzzles and timed-release Crypto](https://people.csail.mit.edu/rivest/pubs/RSW96.pdf)
by Shamir and Rivest.

**Instructions:**

1. Download 🐍 [Python 3.7](https://www.python.org/downloads/)

2. Setup the environment. I recommend using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
Run : `mkvirtualenv -p $(which python3) {YOUR_ENV_NAME}`. Then `workon {YOUR_ENV_NAME}`.

3. Install packages/dependencies: `pip install -r requirements.txt`

4. Run the main function: `python puzzle.py {SECONDS} {SQUARINGS_PER_SECOND} {REPEATS}`.
All three arguments are `int`s and all are required.

## Production

🛑 DO NOT USE IN PRODUCTION ✋. This code is very experimental and is part of a bigger project which will be linked here soon.
Security is not guaranteed, assume it is unsafe.
In the meantime, feel free to play around. PRs are very welcome. 

## Built With

* [pyca/cryptography](https://github.com/pyca/cryptography)

## Versioning

**Version 0.9** (using [SemVer](https://semver.org/))

This version is in Alpha. Breaking changes might occur.

## Authors

* **Jonathan Levi** - @drummerjolev

Thanks to [Myrto Arapinis](https://www.inf.ed.ac.uk/people/staff/Myrto_Arapinis.html), my project supervisor.

## License

Free to use, re-distribute with attribution. Basically, be nice and don't be a jerk.