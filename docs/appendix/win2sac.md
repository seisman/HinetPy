# win2sac

Data converter from WIN32 format to SAC format. It also supports BINARY/ASCII
outputs.

## Usage

```console
win2sac_32 winfile ch_no sacfile [outdir] [-p(prmfile)]
           [-Y] [-e] [-b[BIN]] [-a[ASC]] [-r(RATIO)] [-m(PMAX)]
```

Arguments and options:

| Argument/option | Description |
| --- | --- |
| `winfile` | **One** win32 file to be converted. |
| `ch_no` | Channel numbers to be extracted. It can be a channel number such as `3345`, a comma-separated list such as `3345,3f65,4f75`, or a file containing channel numbers. See details below. |
| `sacfile` | Extension of output SAC files. |
| `outdir` | Output directory. Default is current directory if not specified or is `-`. The output directory must exist. |
| `-p(prmfile)` | Specify parameter file. Default name is `win.prm`. See details below. |
| `-Y` | Use wild channel code, i.e. organization id + network id + channel id. |
| `-e` | Specify SAC/BIN output to use endian of current machine. Defaults to use big endian. |
| `-b[BIN]` | Extension of BIN format. Defaults to `bin`. |
| `-a[ASC]` | Extension of ASC format. Defaults to `asc`. |
| `-r(RATIO)` | The ratio to multiply for BIN/ASC format. Defaults to 1.0. |
| `-m(PMAX)` | Maximum number of data points. Defaults to `2000000`. If your data has more data points, you must increase this value. |

## Examples

```console
win2sac_32 2000082404000101VM.cnt 4c55,4c65 SAC DATA -e > junk.log
```

## Notes

### Output Unit

```{important}
The SAC files extracted by `win2sac_32` are always in physical quality, not in
digital counts.
```

The raw data saved in win32 format is in digital counts. When extracting data
from win32 format, `win2sac_32` always convert digital counts to the
corresponding physical quantity by remove sensitivity from waveform data, and
multiply by 1.0e9 to convert unit from meter to nanometer.

The output SAC files are in `nm/s`, `nm/s/s` or `micro radian`.

### Filename Format

The default filename format is `STATION.COMPONENT.EXTENSION` (e.g.
`N.NABC.U.SAC`). You can only modify the extensions.

### Channel Number File Format

You can save all channel numbers you want to extract into one file.

1. Lines starting with `#` are comment lines and skipped.
2. Blank lines are skipped.
3. Channel numbers can be separated by spaces, tabs, or commas.
4. Each line can contain no more than 2000 characters.

Below is an example:

```text
6034,6035
# 6036 # this line is ignored
6038 6039
```

````{danger}
Using this feature may result in data loss, as `win2sac_32` will exit if data
of any channel doesn't exist in the win32 file.

If you still want to use this feature, you can modify Line 386 of
`s4win2sacm.c` from:

```c
fprintf(stderr, "Data for channel %x not existed\n", sysch);
iRet = 1;
```

to:

```c
fprintf(stderr, "Data for channel %x not existed\n", sysch);
```
````

### Parameter File

win32 system need a parameter file to run. This parameter file has many lines.
However, `win2sac_32` only uses the 2nd and 4th lines, and ignores all other
lines.

An example of a four line parameter file:

```text
.
0101_20100101.ch
.
.
```

The 2nd line is the name of channel table file. `win2sac_32` need to read this
file to extract waveform of specified channels.

The 4th line is the path of pick files. It's useless for most cases.

### Component

The component information is written to SAC header variables `CPMAZ` and
`CMPINC`.

- U/Z: CMPAZ = 0.0, CMPINC = 0.0
- N/X: CMPAZ = 0.0, CMPINC = 90.0
- E/Y: CMPAZ = 90.0, CMPINC = 90.0
- Other: CMPAZ = 0.0, CMPINC = 0.0

```{note}
Azimuths of sensors are **NOT** accurate.

See <https://hinetwww11.bosai.go.jp/auth/direc/?LANG=en> for details.
```
