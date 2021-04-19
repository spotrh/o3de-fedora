Oh, this fork is ugly. I made this package the way I did because I was hoping 
not to need to replace the system qt5 bits (because o3de does _NOT_ work with 
them as is) and I thought this might be less evil than having a copy of qt5 
bundled in o3de (which is what upstream o3de wants you to do).

o3de links against this successfully, but the parts of qt5 I didn't replace
with the o3de fork pull in the original qt5 bits too at linking. This means
that the o3de binaries are linked to BOTH... and I honestly don't know if 
that will work. If it doesn't, then I will probably have to make "o3de"
forked versions of _EVERY_ qt5 component o3de uses. Bleh.

This package also has a fork of qtnetwork, because they patched it too, but
those patches seem OSX specific, and I found it was actually easier not to
use it in o3de.

All of the o3de patches are prefixed with a number sequence.
