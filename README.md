## o3de Fedora packages

These packages are intended to simplify the process of getting o3de running on Fedora.
They are a **huge work in progress**. Most of o3de does not work properly on Linux and there are almost certainly major changes that need to be done to these packages.

Please note the following items when diving in here:

- some of the dependencies are proprietary (PVRTexTool, Wwise, PhysX, NVCloth). for these, I can distribute spec files and patches, but not the "source", so please don't even ask. I do not have access to the source code and I cannot redistribute their binaries.
- Most of o3de does not work properly on Linux. I said this before but it bears repeating. Do not tell me that nothing works right on Fedora, I know. Either send me patches or wait. :)
- Most of my patches have not been sent upstream yet. This is because either they are hacks (and I know it), they're messy (and I know it), or I doubt upstream will want to do it (o3de seems really happy with how they handle 3rd party deps). Could also be that I haven't had time.
- You should be able to use the luxcorerender in Fedora, the changes here are only for aarch64 enablement (there is no aarch64 build in Fedora yet)
- You might be asking, what the %@&#! is qt5-qtbase-o3de. A good question. o3de depends on a forked version of qt, but only some parts of it are forked. This builds that fork in a way that can coexist with the system qt5.

License wise, anything copyrightable here is under the same license as the work it is for (or on top of). That means that patches for an MIT licensed software are MIT, specs for an Apache 2.0 licensed software component are Apache 2.0, etc, etc.
