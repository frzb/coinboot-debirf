![Logo of Coinboot](https://raw.githubusercontent.com/frzb/coinboot/master/coinboot.png)

***Building  your own Coinboot image***

Coinboot is a framework for diskless computing.

Coinboot uses a heavy adapted version of [debirf](http://cmrg.fifthhorseman.net/wiki/debirf) to build the Coinboot base image which makes it possible to run machines diskless and completely in-memory.

Coinboot is made to be lightweight. Measuring ~85M for the initramfs and ~7M for the kernel archive.

Coinboot is currently based on Ubuntu 16.04 Xenial.

For more information how to boot your machines with Coinboot visit: https://coinboot.io

## Requirements 

Vagrant

## Usage

To build the Coinboot base image consisting of a initramfs archive (`initramfs`) and kernel archive (`vmlinuz`) run:

```
$ vagrant up
```

When the build has finished the resulting archives are written to the `./build` directory.

## License

GNU GPLv3 

## Author

Gunter Miegel 
gm@coinboot.io

## Contribution

Fork this repo. 
Make a pull request to this repo. 
