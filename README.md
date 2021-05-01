# NI/Ableton 11 scripts

This repository hosts newly released Native intruments scripts, with both the source files and the decompiled scripts, using `uncompyle6` library.

This can be used to add functionnalities, debug or just for learning purpose.

So far, the following scripts have been released:

- [x] KK MK1
- [x] Maschine Mikro MK2 
- [x] Maschine MK2
- [x] Maschine Studio
- [x] Maschine JAM
- [ ] Maschine MK3

*full list comes from `https://www.native-instruments.com/forum/threads/ableton-live-11-needs-a-new-midi-scripts-for-maschine-controllers.446183/page-12#post-2087933`*

```bash
.
├── README.md
├── kk
│   └── kk_mk1
│       ├── scripts
│       └── src
└── maschine
    ├── maschine_jam
    │   ├── scripts
    │   └── src
    ├── maschine_mikro_mk2
    │   ├── scripts
    │   └── src
    ├── maschine_mk2
    │   ├── scripts
    │   └── src
    └── maschine_studio
        ├── scripts
        └── src
```

## Errors

Here are listed the files that had issues during the process. This could maybe be fixed by trying other libraries.

### KK MK1

Everything went well :ok_hand:

### Maschine JAM

- `EncoderComponent.py`
- `JamModes.py`

### Maschine Mikro MK2

- `EditSection.pyc`

### Maschine Studio

- `EditSection.pyc`

### Maschine MK2

- `EditSection.pyc`