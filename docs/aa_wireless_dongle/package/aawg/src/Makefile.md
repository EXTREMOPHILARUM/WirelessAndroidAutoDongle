# Makefile

The `Makefile` in this directory is used to build the Android Auto Wireless Gateway (AAWG) package. It defines the build rules and dependencies for the project.

## Targets

- `aawgd`: The main target that builds the AAWG daemon.
- `clean`: Cleans the build artifacts.

## Variables

- `EXTRA_CXXFLAGS`: Additional C++ compiler flags.
- `PROTO_FILES`: List of Protocol Buffer files.
- `PROTO_HEADERS`: List of generated Protocol Buffer header files.
- `ALL_HEADERS`: List of all header files.

## Rules

- `aawgd`: Builds the AAWG daemon by linking the object files.
- `%.o`: Compiles the C++ source files into object files.
- `%.pb.o`: Compiles the Protocol Buffer source files into object files.
- `proto/%.pb.cc proto/%.pb.h`: Generates the Protocol Buffer source and header files from the `.proto` files.
- `clean`: Removes the build artifacts.

## Example Usage

To build the AAWG package, run the following command:

```sh
make
```

To clean the build artifacts, run the following command:

```sh
make clean
```
