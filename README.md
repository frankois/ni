# NI/Ableton 11 scripts

```bash
.
├── README.md
├── midi_remote_scripts
│   ├── kk
│   │   └── kk_mk1
│   └── maschine
│       ├── maschine_jam
│       ├── maschine_mikro_mk2
│       ├── maschine_mk2
│       ├── maschine_mk3
│       └── maschine_studio
└── user_remote_scripts
    ├── InstantMappings-HowTo.txt
    ├── Komplete Kontrol A61 Macro
    │   └── UserConfiguration.txt
    ├── Komplete Kontrol M32 Macro
    │   └── UserConfiguration.txt
    └── UserConfiguration.txt
```

## User Remote Scripts

> User/Library/Preferences/Ableton/Live x.x.x/User Remote Scripts

This folder contains Ableton MIDI mappings for the following Devices:

- Komplete Kontrol M32
- Komplete Kontrol A61 

It also has Ableton factory help files.

## MIDI Remote Scripts

> Applications/Ableton/Contents/App-Ressources/MIDI Remote Scripts

Official installation guides can be found here:
- Maschine mk3 : https://support.native-instruments.com/hc/en-us/articles/360021081838
- Mashine mk2/studio/jam : https://support.native-instruments.com/hc/en-us/articles/360019645058-How-to-Install-the-MASCHINE-Ableton-Live-11-Template

This folder hosts newly released Native intruments scripts, with both the source files and the decompiled scripts, using `uncompyle6` library.

This can be used to add functionnalities, debug or just for learning purpose.

So far, the following scripts have been released:

- [x] KK MK1
- [x] Maschine Mikro MK2 
- [x] Maschine MK2
- [x] Maschine Studio
- [x] Maschine JAM
- [x] Maschine MK3

*full list comes from `https://www.native-instruments.com/forum/threads/ableton-live-11-needs-a-new-midi-scripts-for-maschine-controllers.446183/page-12#post-2087933`*

### Errors

Here are listed the files that had issues during the process. This could maybe be fixed by trying other libraries.

#### KK MK1

Everything went well :ok_hand:

#### Maschine JAM

- `EncoderComponent.py`
- `JamModes.py`

#### Maschine Mikro MK2

- `EditSection.pyc`

#### Maschine Studio

- `EditSection.pyc`

#### Maschine MK2

- `EditSection.pyc`

#### Maschine MK2

Everything went well :ok_hand: