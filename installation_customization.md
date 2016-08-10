# Installation
1. download zip from kx.com (32bit) or have previous 64bit license
2. unpack archive into `$HOME/q`

## Components of q
- q executable (q or q.exe)
- q.k
- (optional) k4.lic
- (optional) q.q

## Key environment variables
**QHOME**
: directory where kdb process looks for the mandatory startup file `q.k` and for 64 bit systems where kdb looks for `k4.lic` if `QLIC` is not set.  Defaults to `$HOME/q` if not set.

**QLIC**
: directory of `k4.lic` license file.

**QINIT**
: file that gets executed after `q.k` is loaded.  If not set, kdb tries to load `$QHOME/q.q`, and if that doesn't exist no error is generated and kdb finishes initialization.

## File and database loading logic
When kdb loads, the current working directory is where the q executable gets called (e.g. if you called q from `$HOME/myfiles` that is your current working directory).  However, it's important to understand how after initialization kdb tries to load databases and files.  To check where the current working directory is, run `system"cd"`.

**Database**
: When loading a database (either on startup or via `\l`), kdb will change the current directory to the root directory of the database.

**File**
: If the path is an absolute path, kdb will try to load the file from that location.  If the path is a relative path, kdb will search in the following order:

1. current working directory
2. `QHOME` if it is set
3. `HOME`

# Useful customization
If you're using kdb interactively, it's useful to start q with `rlwrap`.  This allows you to look at previous commands, use arrows keys and other readline features.

If you're running kdb as a service, one quick way is to use both `nohup` and `&` to run a q instance in the background.
