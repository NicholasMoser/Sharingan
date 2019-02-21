# Sharingan

*Sharingan* allows you to read and write real-time memory in the Dolphin Emulator for Naruto GNT4. The writing to memory is done through a virtual controller, allowing you to declare controller movements programmatically. *Sharingan* is a fork of [spxtr/p3](https://github.com/spxtr/p3) but changed to interact with Naruto GNT4 instead of Super Smash Bros. Melee. This library's main use is to aid in the development of an AI for Naruto GNT4.

## Getting Started

Download this repository and run with `python -m p3` before opening Dolphin. Stop with ^C. Please see [Prerequisites](#Prerequisites) and [Installing](#Installing) before attempting to run.

### Prerequisites

```
UNIX-like Operating System (e.g. Linux)
Python 3
Dolphin Emulator
```

Note, Windows is not supported until Dolphin adds Windows MemoryWatcher support. Follow progress of that here: https://github.com/dolphin-emu/dolphin/pull/6138

### Installing

Download the [Dolphin Emulator](https://dolphin-emu.org/) and configure the [pipe input](https://wiki.dolphin-emu.org/index.php?title=Pipe_Input) in Dolphin for player 3.

See `example_gc_config.ini` for an example Dolphin profile.

## Running the tests

Test with `python -m unittest discover -p "*_test.py"`.

## Authors

* **Joe Finney** - *Initial work* - [spxtr](https://github.com/spxtr)
* **Nick Moser** - *Change to work with GNT4* - [NicholasMoser](https://github.com/NicholasMoser/)

## License

This project is licensed under GPL version 3. - see the [LICENSE](LICENSE) file for details
